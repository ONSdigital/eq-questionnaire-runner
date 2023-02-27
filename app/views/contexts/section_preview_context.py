from typing import Any, Mapping, Optional, Union

from app.data_models import AnswerStore, ListStore, ProgressStore
from app.data_models.metadata_proxy import MetadataProxy
from app.questionnaire import QuestionnaireSchema
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
        self._section_id = section_id

    def __call__(self) -> Mapping[str, dict]:
        preview = self._build_preview()
        title_for_location = self._title_for_location()

        return {
            "preview": {
                "title": title_for_location,
                **preview,
            }
        }

    def _build_preview(self) -> dict[str, Union[str, dict, Any]]:
        # Type ignore: The section has to exist at this point
        section = self._placeholder_renderer.render(self._schema.get_section(self._section_id), None)  # type: ignore

        groups = [
            PreviewGroup(group_schema=group).serialize() for group in section["groups"]
        ]
        section_dict: dict = {
            "title": self._schema.get_title_for_section(self._section_id),
            "blocks": [],
        }
        for group in groups:
            section_dict["blocks"] += group["blocks"]

        return {"groups": [section_dict]}

    def _title_for_location(self) -> Optional[str]:
        return self._schema.get_title_for_section(self._section_id)
