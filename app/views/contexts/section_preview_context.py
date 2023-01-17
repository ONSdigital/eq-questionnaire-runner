from functools import cached_property
from typing import Mapping, Optional

from app.data_models import AnswerStore, ListStore, ProgressStore
from app.data_models.metadata_proxy import MetadataProxy
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
        metadata: Optional[MetadataProxy],
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

        return self._schema.get_custom_page_title_for_section(
            self.current_location.section_id
        ) or self._get_safe_page_title(title_for_location)

    def _build_summary(self):

        return {
            "groups": [
                PreviewGroup(
                    group,
                    self._metadata,
                    self._schema,
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
        return self._schema.get_title_for_section(self.current_location.section_id)

    def _get_safe_page_title(self, title):
        return (
            safe_content(self._schema.get_single_string_value(title)) if title else ""
        )
