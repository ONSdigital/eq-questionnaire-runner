from __future__ import annotations

import itertools
import logging
from collections.abc import Callable
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Any, Mapping, MutableMapping, Optional, Sequence, Union

from dateutil.relativedelta import relativedelta
from flask_wtf import FlaskForm
from werkzeug.datastructures import ImmutableMultiDict, MultiDict
from wtforms import validators

from app.data_models import (
    AnswerStore,
    AnswerValueTypes,
    ListStore,
    ProgressStore,
    SupplementaryDataStore,
)
from app.data_models.metadata_proxy import MetadataProxy
from app.forms import error_messages
from app.forms.field_handlers import DateHandler, FieldHandler, get_field_handler
from app.forms.validators import DateRangeCheck, MutuallyExclusiveCheck, SumCheck
from app.questionnaire import Location, QuestionnaireSchema, QuestionSchemaType
from app.questionnaire.dependencies import (
    get_routing_path_block_ids_by_section_for_calculated_summary_dependencies,
)
from app.questionnaire.path_finder import PathFinder
from app.questionnaire.relationship_location import RelationshipLocation
from app.questionnaire.rules.rule_evaluator import RuleEvaluator
from app.questionnaire.value_source_resolver import ValueSourceResolver
from app.utilities.mappings import get_flattened_mapping_values
from app.utilities.types import LocationType, SectionKey

logger = logging.getLogger(__name__)

Calculation = Mapping[str, Any]
QuestionnaireExtraValidators = Mapping[str, Sequence[Callable]]
Period = Mapping[str, int]
PeriodLimits = Mapping[str, Any]
Error = Union[Mapping, Sequence]
Errors = Mapping[str, Error]
ErrorList = Sequence[tuple[str, str]]


# pylint: disable=too-many-locals
class QuestionnaireForm(FlaskForm):
    def __init__(
        self,
        schema: QuestionnaireSchema,
        question_schema: QuestionSchemaType,
        answer_store: AnswerStore,
        list_store: ListStore,
        metadata: Optional[MetadataProxy],
        response_metadata: MutableMapping,
        location: Union[None, Location, RelationshipLocation],
        progress_store: ProgressStore,
        supplementary_data_store: SupplementaryDataStore,
        **kwargs: Union[MultiDict, Mapping, None],
    ):
        self.schema = schema
        self.question = question_schema
        self.answer_store = answer_store
        self.list_store = list_store
        self.metadata = metadata
        self.response_metadata = response_metadata
        self.location = location
        self.question_errors: dict[str, str] = {}
        self.options_with_detail_answer: dict = {}
        self.question_title = self.question.get("title", "")
        self.progress_store = progress_store
        self.supplementary_data_store = supplementary_data_store
        self.value_source_resolver = ValueSourceResolver(
            answer_store=self.answer_store,
            schema=self.schema,
            metadata=self.metadata,
            response_metadata=self.response_metadata,
            list_store=self.list_store,
            location=self.location,
            list_item_id=self.location.list_item_id if self.location else None,
            progress_store=self.progress_store,
            supplementary_data_store=self.supplementary_data_store,
        )

        super().__init__(**kwargs)

    def validate(
        self, extra_validators: Optional[QuestionnaireExtraValidators] = None
    ) -> bool:
        """
        Validate this form as usual and check for any form-level validation errors based on question type
        :return: boolean
        """
        super().validate(extra_validators=extra_validators)
        valid_fields = FlaskForm.validate(self)
        valid_date_range_form = True
        valid_calculated_form = True
        valid_mutually_exclusive_form = True

        if self.question:
            if self.question["type"] == "DateRange" and valid_date_range_form:
                valid_date_range_form = self.validate_date_range_question(self.question)
            elif self.question["type"] == "Calculated" and valid_calculated_form:
                valid_calculated_form = self.validate_calculated_question(self.question)
            elif (
                self.question["type"] == "MutuallyExclusive"
                and valid_mutually_exclusive_form
                and valid_fields
            ):
                valid_mutually_exclusive_form = (
                    self.validate_mutually_exclusive_question(self.question)
                )

        return (
            valid_fields
            and valid_date_range_form
            and valid_calculated_form
            and valid_mutually_exclusive_form
        )

    def validate_date_range_question(self, question: QuestionSchemaType) -> bool:
        date_from = question["answers"][0]
        date_to = question["answers"][1]
        if self._has_min_and_max_single_dates(date_from, date_to):
            # Work out the largest possible range, for date range question
            period_range = self._get_period_range_for_single_date(date_from, date_to)
            if "period_limits" in question:
                self.validate_date_range_with_period_limits_and_single_date_limits(
                    question["id"], question["period_limits"], period_range
                )
            else:
                # Check every field on each form has populated data
                if self.is_date_form_populated(
                    getattr(self, date_from["id"]), getattr(self, date_to["id"])
                ):
                    self.validate_date_range_with_single_date_limits(
                        question["id"], period_range
                    )

        period_from_id = date_from["id"]
        period_to_id = date_to["id"]

        messages = question.get("validation", {}).get("messages")

        if not (
            self.answers_all_valid([period_from_id, period_to_id])
            and self._validate_date_range_question(
                question["id"],
                period_from_id,
                period_to_id,
                messages,
                question.get("period_limits"),
            )
        ):
            return False

        return True

    def validate_calculated_question(self, question: QuestionSchemaType) -> bool:
        for calculation in question["calculations"]:
            result = self._get_target_total_and_currency(calculation, question)
            if result:
                target_total, currency = result
                if self.answers_all_valid(
                    calculation["answers_to_calculate"]
                ) and self._validate_calculated_question(
                    calculation, question, target_total, currency
                ):
                    # Remove any previous question errors if it passes this OR before returning True
                    if question["id"] in self.question_errors:
                        self.question_errors.pop(question["id"])
                    return True

        return False

    def validate_mutually_exclusive_question(
        self, question: QuestionSchemaType
    ) -> bool:
        is_mandatory: bool = question["mandatory"]
        messages = (
            question["validation"].get("messages") if "validation" in question else None
        )
        answers = (getattr(self, answer["id"]).data for answer in question["answers"])
        is_only_checkboxes_or_radios = all(
            answer["type"] in {"Checkbox", "Radio"} for answer in question["answers"]
        )
        validator = MutuallyExclusiveCheck(
            messages=messages,
            question_title=self.question_title,
        )

        try:
            validator(answers, is_mandatory, is_only_checkboxes_or_radios)
        except validators.ValidationError as e:
            self.question_errors[question["id"]] = str(e)

            return False
        return True

    def _get_target_total_and_currency(
        self,
        calculation: Calculation,
        question: QuestionSchemaType,
    ) -> Optional[tuple[Union[Calculation, AnswerValueTypes], Optional[str]]]:
        calculation_value: Union[Calculation, AnswerValueTypes]
        currency: Optional[str]

        if "value" in calculation:
            if isinstance(calculation["value"], dict):
                calculation_value = self.value_source_resolver.resolve(calculation["value"])  # type: ignore
            else:
                calculation_value = calculation["value"]
            currency = question.get("currency")
            return calculation_value, currency

        target_answer = self.schema.get_answers_by_answer_id(calculation["answer_id"])[
            0
        ]
        calculation_value = self.answer_store.get_answer(
            calculation["answer_id"]
        ).value  # type: ignore # expect not None
        currency = target_answer.get("currency")

        return calculation_value, currency

    def validate_date_range_with_period_limits_and_single_date_limits(
        self,
        question_id: Union[str, Sequence[Mapping]],
        period_limits: PeriodLimits,
        period_range: timedelta,
    ) -> None:
        # Get period_limits from question
        period_limits_item = self._get_period_limits(period_limits)
        period_min = period_limits_item[0]

        # Exception to be raised if range available is smaller than minimum range allowed
        if period_min and period_range < self._get_offset_value(period_min):
            exception = f"The schema has invalid period_limits for {question_id}"

            raise ValueError(exception)

    @staticmethod
    def validate_date_range_with_single_date_limits(
        question_id: str, period_range: timedelta
    ) -> None:
        # Exception to be raised if range from answers are smaller than
        # minimum or larger than maximum period_limits
        exception = f"The schema has invalid date answer limits for {question_id}"

        if period_range < timedelta(0):
            raise ValueError(exception)

    def _validate_date_range_question(
        self,
        question_id: str,
        period_from_id: str,
        period_to_id: str,
        messages: Mapping[str, str],
        period_limits: Optional[PeriodLimits],
    ) -> bool:
        period_from = getattr(self, period_from_id)
        period_to = getattr(self, period_to_id)
        period_min, period_max = self._get_period_limits(period_limits)
        validator = DateRangeCheck(
            messages=messages, period_min=period_min, period_max=period_max
        )

        # Check every field on each form has populated data
        if self.is_date_form_populated(period_from, period_to):
            try:
                validator(self, period_from, period_to)
            except validators.ValidationError as e:
                self.question_errors[question_id] = str(e)
                return False

        return True

    def _validate_calculated_question(
        self,
        calculation: Calculation,
        question: QuestionSchemaType,
        target_total: Any,
        currency: Optional[str],
    ) -> bool:
        messages = None
        if "validation" in question:
            messages = question["validation"].get("messages")

        validator = SumCheck(messages=messages, currency=currency)

        calculation_type = ValueSourceResolver.get_calculation_operator(
            calculation["calculation_type"]
        )

        formatted_values = self._get_formatted_calculation_values(
            calculation["answers_to_calculate"]
        )

        calculation_total = self._get_calculation_total(
            calculation_type, formatted_values
        )

        # Validate grouped answers meet calculation_type criteria
        try:
            validator(self, calculation["conditions"], calculation_total, target_total)
        except validators.ValidationError as e:
            self.question_errors[question["id"]] = str(e)
            return False

        return True

    def _get_period_range_for_single_date(
        self,
        date_from: Mapping[str, dict],
        date_to: Mapping[str, dict],
    ) -> timedelta:
        list_item_id = self.location.list_item_id if self.location else None
        value_source_resolver = ValueSourceResolver(
            answer_store=self.answer_store,
            list_store=self.list_store,
            metadata=self.metadata,
            response_metadata=self.response_metadata,
            schema=self.schema,
            location=self.location,
            list_item_id=list_item_id,
            escape_answer_values=False,
            progress_store=self.progress_store,
            supplementary_data_store=self.supplementary_data_store,
        )

        rule_evaluator = RuleEvaluator(
            schema=self.schema,
            answer_store=self.answer_store,
            list_store=self.list_store,
            metadata=self.metadata,
            response_metadata=self.response_metadata,
            location=self.location,
            progress_store=self.progress_store,
            supplementary_data_store=self.supplementary_data_store,
        )

        handler = DateHandler(
            date_from, value_source_resolver, rule_evaluator, error_messages
        )

        min_period_date = handler.get_date_value("minimum") or handler.get_date_value(
            "maximum"
        )
        handler.answer_schema = date_to
        max_period_date = handler.get_date_value("maximum") or handler.get_date_value(
            "minimum"
        )

        if not min_period_date or not max_period_date:
            raise ValueError("Period range must have a start and end date")

        # Work out the largest possible range, for date range question
        period_range = max_period_date - min_period_date

        return period_range

    @staticmethod
    def is_date_form_populated(date_from: Sequence, date_to: Sequence) -> bool:
        return all(field.data for field in itertools.chain(date_from, date_to))

    @staticmethod
    def _has_min_and_max_single_dates(
        date_from: Mapping[str, Mapping],
        date_to: Mapping[str, Mapping],
    ) -> bool:
        return ("minimum" in date_from or "maximum" in date_from) and (
            "minimum" in date_to or "maximum" in date_to
        )

    @staticmethod
    def _get_offset_value(period_object: Mapping[str, int]) -> timedelta:
        now = datetime.now(tz=timezone.utc)
        delta = relativedelta(
            years=period_object.get("years", 0),
            months=period_object.get("months", 0),
            days=period_object.get("days", 0),
        )

        return now + delta - now

    @staticmethod
    def _get_period_limits(
        limits: Optional[PeriodLimits],
    ) -> tuple[Optional[dict[str, Any]], Optional[dict[str, Any]]]:
        minimum, maximum = None, None
        if limits:
            if "minimum" in limits:
                minimum = limits["minimum"]
            if "maximum" in limits:
                maximum = limits["maximum"]
        return minimum, maximum

    def _get_formatted_calculation_values(
        self, answers_sequence: Sequence[str]
    ) -> list[str]:
        answers_list: list[str] = []
        block_id = self.location.block_id if self.location else None
        if block_id and block_id in self.schema.dynamic_answers_parent_block_ids:
            list_name = self.schema.get_list_name_for_dynamic_answer(block_id)
            list_item_ids = self.list_store[list_name]
            for answer_id in answers_sequence:
                if self.schema.is_answer_dynamic(answer_id):
                    answers_list.extend(
                        f"{answer_id}-{list_item_id}" for list_item_id in list_item_ids
                    )
                else:
                    answers_list.append(answer_id)
        else:
            answers_list = list(answers_sequence)

        return [
            self.get_data(answer_id).replace(" ", "").replace(",", "")
            for answer_id in answers_list
        ]

    @staticmethod
    def _get_calculation_total(
        calculation_type: Callable, values: Sequence[Union[float, int, Decimal, str]]
    ) -> Decimal:
        result: Decimal = calculation_type(Decimal(value or 0) for value in values)
        return result

    def answers_all_valid(self, answer_id_list: Sequence[str]) -> bool:
        # pylint: disable=no-member
        # wtforms Form parents are not discoverable in the 2.3.3 implementation
        return not set(answer_id_list) & set(self.errors)

    def map_errors(self) -> list[tuple[str, str]]:
        ordered_errors = []

        if self.question["id"] in self.question_errors:
            ordered_errors += [
                (
                    _get_error_id(self.question["id"]),
                    self.question_errors[self.question["id"]],
                )
            ]
        # pylint: disable=no-member
        # wtforms Form parents are not discoverable in the 2.3.3 implementation
        for answer in self.question["answers"]:
            if answer["id"] in self.errors:
                ordered_errors += map_subfield_errors(self.errors, answer["id"])
            if "options" in answer:
                ordered_errors += map_detail_answer_errors(self.errors, answer)

        return ordered_errors

    def answer_errors(self, input_id: str) -> list[str]:
        error_id = _get_error_id(input_id)
        return [error[1] for error in self.map_errors() if error_id == error[0]]

    def get_data(self, answer_id: str) -> str:
        attr = getattr(self, answer_id)
        if attr.raw_data:
            result: str = attr.raw_data[0]
        else:
            result = ""
        return result


def _option_value_in_data(
    answer: Mapping[str, str],
    option: Mapping[str, Any],
    data: Union[MultiDict[str, Any], Mapping[str, Any]],
) -> bool:
    data_to_inspect = data.to_dict(flat=False) if isinstance(data, MultiDict) else data

    return option["value"] in data_to_inspect.get(answer["id"], [])


def get_answer_fields(
    question: QuestionSchemaType,
    data: MultiDict[str, Any] | Mapping[str, Any] | None,
    schema: QuestionnaireSchema,
    answer_store: AnswerStore,
    list_store: ListStore,
    metadata: MetadataProxy | None,
    response_metadata: MutableMapping,
    location: LocationType | None,
    progress_store: ProgressStore,
    supplementary_data_store: SupplementaryDataStore,
) -> dict[str, FieldHandler]:
    list_item_id = location.list_item_id if location else None

    block_ids_by_section: dict[SectionKey, tuple[str, ...]] = {}

    if location and progress_store:
        block_ids_by_section = (
            get_routing_path_block_ids_by_section_for_calculated_summary_dependencies(
                location=location,
                progress_store=progress_store,
                path_finder=PathFinder(
                    schema=schema,
                    answer_store=answer_store,
                    list_store=list_store,
                    progress_store=progress_store,
                    metadata=metadata,
                    response_metadata=response_metadata,
                    supplementary_data_store=supplementary_data_store,
                ),
                data=question,
                ignore_keys=["when"],
                schema=schema,
            )
        )
    block_ids = None
    if block_ids_by_section:
        block_ids = get_flattened_mapping_values(block_ids_by_section)

    def _get_value_source_resolver(list_item: str | None = None) -> ValueSourceResolver:
        return ValueSourceResolver(
            answer_store=answer_store,
            list_store=list_store,
            metadata=metadata,
            schema=schema,
            location=location,
            list_item_id=list_item,
            escape_answer_values=False,
            response_metadata=response_metadata,
            routing_path_block_ids=block_ids,
            assess_routing_path=False,
            progress_store=progress_store,
            supplementary_data_store=supplementary_data_store,
        )

    rule_evaluator = RuleEvaluator(
        schema=schema,
        answer_store=answer_store,
        list_store=list_store,
        metadata=metadata,
        response_metadata=response_metadata,
        location=location,
        progress_store=progress_store,
        supplementary_data_store=supplementary_data_store,
    )

    answer_fields = {}
    question_title = question.get("title")

    value_source_resolved_for_location = _get_value_source_resolver(list_item_id)
    for answer in question.get("answers", []):
        if "list_item_id" in answer:
            value_source_resolver = _get_value_source_resolver(answer["list_item_id"])
        else:
            value_source_resolver = value_source_resolved_for_location

        for option in answer.get("options", []):
            if "detail_answer" in option:
                if data:
                    disable_validation = not _option_value_in_data(answer, option, data)
                else:
                    disable_validation = True

                detail_answer = option["detail_answer"]

                answer_fields[option["detail_answer"]["id"]] = get_field_handler(
                    answer_schema=detail_answer,
                    value_source_resolver=value_source_resolver,
                    rule_evaluator=rule_evaluator,
                    error_messages=schema.error_messages,
                    disable_validation=disable_validation,
                    question_title=question_title,
                ).get_field()
        answer_fields[answer["id"]] = get_field_handler(
            answer_schema=answer,
            value_source_resolver=value_source_resolver,
            rule_evaluator=rule_evaluator,
            error_messages=schema.error_messages,
            question_title=question_title,
        ).get_field()

    return answer_fields


def map_subfield_errors(errors: Mapping[str, Any], answer_id: str) -> ErrorList:
    subfield_errors = []

    if isinstance(errors[answer_id], dict):
        errors_dict = errors[answer_id]
        for error_list in errors_dict.values():
            for error in error_list:
                error_id = _get_error_id(answer_id)
                subfield_errors.append((error_id, error))
    else:
        errors_list = errors[answer_id]
        for error in errors_list:
            error_id = _get_error_id(answer_id)
            subfield_errors.append((error_id, error))

    return subfield_errors


def map_detail_answer_errors(
    errors: Errors,
    answer_json: Mapping[str, Any],
) -> ErrorList:
    detail_answer_errors = []

    for option in answer_json["options"]:
        if "detail_answer" in option and option["detail_answer"]["id"] in errors:
            for error in errors[option["detail_answer"]["id"]]:
                error_id = _get_error_id(answer_json["id"])
                detail_answer_errors.append((error_id, error))

    return detail_answer_errors


def _get_error_id(id_: str) -> str:
    return f"{id_}-error"


def _clear_detail_answer_field(
    form_data: ImmutableMultiDict | MultiDict, question_schema: QuestionSchemaType
) -> MultiDict[str, Any]:
    """
    Clears the detail answer field if the parent option is not selected
    """
    mutable_form_data = (
        MultiDict(form_data) if isinstance(form_data, ImmutableMultiDict) else form_data
    )

    for answer in question_schema.get("answers", []):
        for option in answer.get("options", []):
            if "detail_answer" in option and option["value"] not in form_data.getlist(
                answer["id"]
            ):
                mutable_form_data[option["detail_answer"]["id"]] = ""

    return mutable_form_data


def generate_form(
    *,
    schema: QuestionnaireSchema,
    question_schema: QuestionSchemaType,
    answer_store: AnswerStore,
    list_store: ListStore,
    metadata: MetadataProxy | None,
    response_metadata: MutableMapping,
    progress_store: ProgressStore,
    supplementary_data_store: SupplementaryDataStore,
    location: LocationType | None = None,
    data: dict[str, Any] | None = None,
    form_data: MultiDict | None = None,
) -> QuestionnaireForm:
    class DynamicForm(QuestionnaireForm):
        pass

    if form_data:
        form_data = _clear_detail_answer_field(form_data, question_schema)

    input_data = form_data if form_data is not None else data
    answer_fields = get_answer_fields(
        question_schema,
        input_data,
        schema,
        answer_store,
        list_store,
        metadata,
        response_metadata,
        location,
        progress_store=progress_store,
        supplementary_data_store=supplementary_data_store,
    )

    for answer_id, field in answer_fields.items():
        setattr(DynamicForm, answer_id, field)

    return DynamicForm(
        schema,
        question_schema,
        answer_store,
        list_store,
        metadata,
        response_metadata,
        location,
        data=data,
        formdata=form_data,
        progress_store=progress_store,
        supplementary_data_store=supplementary_data_store,
    )
