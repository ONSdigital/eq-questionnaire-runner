from functools import cached_property
from typing import Any, Mapping, Optional, Union

from werkzeug.datastructures import ImmutableDict

from app.data_models import AnswerStore, ListStore, ProgressStore
from app.data_models.metadata_proxy import MetadataProxy
from app.questionnaire import Location, QuestionnaireSchema
from app.questionnaire.placeholder_renderer import PlaceholderRenderer
from app.views.contexts.context import Context
from app.views.contexts.preview import PreviewGroup


class SectionPreviewContext(Context):
    def __init__(
        self,
        *,
        language: str,
        schema: QuestionnaireSchema,
        answer_store: AnswerStore,
        list_store: ListStore,
        progress_store: ProgressStore,
        metadata: Optional[MetadataProxy],
        response_metadata: Mapping[str, Union[str, int, list]],
        section_id: str,
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
        self._placeholder_preview_mode = self._schema.preview_enabled
        self._location = Location(
            section_id=section_id,
            block_id=self._schema.get_first_block_id_for_section(section_id),
        )
        self._placeholder_renderer = PlaceholderRenderer(
            language=self._language,
            answer_store=self._answer_store,
            list_store=self._list_store,
            metadata=self._metadata,
            response_metadata=self._response_metadata,
            schema=self._schema,
            location=self._location,
            placeholder_preview_mode=self._placeholder_preview_mode,
        )

    def __call__(self) -> Mapping[str, dict]:
        preview = self._build_preview()
        title_for_location = self._title_for_location()

        return {
            "preview": {
                "title": title_for_location,
                **preview,
            }
        }

    @cached_property
    def section(self) -> ImmutableDict:
        # Type ignore: The section has to exist at this point
        section: ImmutableDict = self._schema.get_section(self._location.section_id)  # type: ignore
        return section

    def _build_preview(self) -> dict[str, Union[str, dict, Any]]:
        section = self._placeholder_renderer.render(self.section, None)

        return {
            "groups": [
                PreviewGroup(
                    group_schema=group,
                    section_title=self._schema.get_title_for_section(
                        self._location.section_id
                    ),  # this gets the title of a section for a group since we have 1 to 1 relationship between section and its group(s),
                    # group title is not always present/missing in business schemas hence using the section title
                    # base for this was the code we use for summaries generation, that is how summaries are generated in runner
                    # (they use group titles of sections for twisties)
                ).serialize()
                for group in section["groups"]
            ],
        }

    def _title_for_location(self) -> Optional[str]:
        return self._schema.get_title_for_section(self._location.section_id)
