from functools import cached_property
from typing import Any, Mapping, Optional


from app.data_models import AnswerStore, ListStore, ProgressStore
from app.questionnaire import QuestionnaireSchema
from app.questionnaire.location import Location
from app.utilities import safe_content

from .context import Context
from .summary import PreviewGroup


class SectionPreviewContext(Context):
    def __init__(
        self,
        language: str,
        schema: QuestionnaireSchema,
        answer_store: AnswerStore,
        list_store: ListStore,
        progress_store: ProgressStore,
        metadata: Mapping[str, Any],
        response_metadata: Mapping,
        current_location: Location,
    ):
        super().__init__(
            language,
            schema,
            answer_store,
            list_store,
            progress_store,
            metadata,
            response_metadata,
        )
        self.current_location = current_location

    def __call__(self, return_to: Optional[str] = "section-summary") -> Mapping:
        summary = self._build_summary()
        title_for_location = self._title_for_location()
        title = (
            self._placeholder_renderer.render_placeholder(
                title_for_location, self.current_location.list_item_id
            )
            if isinstance(title_for_location, dict)
            else title_for_location
        )

        page_title = self.get_page_title(title_for_location)

        return {
            "summary": {
                "title": title,
                "page_title": page_title,
                "summary_type": "SectionSummary",
                "answers_are_editable": True,
                **summary,
            }
        }

    @cached_property
    def section(self):
        return self._schema.get_section(self.current_location.section_id)

    def get_page_title(self, title_for_location: str) -> str:

        section_repeating_page_title = (
            self._schema.get_repeating_page_title_for_section(
                self.current_location.section_id
            )
        )
        page_title = self._schema.get_custom_page_title_for_section(
            self.current_location.section_id
        ) or self._get_safe_page_title(title_for_location)

        if section_repeating_page_title:
            page_title = f"{page_title}: {section_repeating_page_title}"

        if self.current_location.list_item_id and self.current_location.list_name:
            list_item_position = self._list_store.list_item_position(
                self.current_location.list_name, self.current_location.list_item_id
            )
            page_title = page_title.format(list_item_position=list_item_position)
        return page_title

    def _build_summary(self):
        """
        Build a summary context for a particular location.

        Does not support generating multiple sections at a time (i.e. passing no list_item_id for repeating section).
        """
        summary = self.section.get("summary", {})
        collapsible = {"collapsible": summary.get("collapsible", False)}

        return {
            **collapsible,
            "groups": [
                PreviewGroup(
                    group,
                    self._answer_store,
                    self._list_store,
                    self._metadata,
                    self._response_metadata,
                    self._schema,
                    self.current_location,
                    self._language,
                    self._schema.get_title_for_section(
                        self.current_location.section_id
                    ),  # this gets the title of a section for a group since we have 1 to 1 relationship between section and its group(s),
                    # group title is not always present/missing in business schemas hence using the section title
                    # base for this was the code we use for summaries generation, that is how summaries are generated in runner
                    # (they use group titles of sections for twisties)
                ).serialize()
                for group in self.section["groups"]
            ],
        }

    def _title_for_location(self):
        section_id = self.current_location.section_id
        return (
            self._schema.get_repeating_title_for_section(section_id)
            or self._schema.get_summary_title_for_section(section_id)
            or self._schema.get_title_for_section(section_id)
        )

    def _get_safe_page_title(self, title):
        return (
            safe_content(self._schema.get_single_string_value(title)) if title else ""
        )
