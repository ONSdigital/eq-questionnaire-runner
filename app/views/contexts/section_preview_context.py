from typing import MutableMapping, Optional

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
        response_metadata: MutableMapping,
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
            placeholder_preview_mode=True,
        )
        self._section_id = section_id

    def __call__(self) -> dict:
        return {"preview": self._build_preview()}

    def _build_preview(self) -> list[dict]:
        # Type ignore: The section has to exist at this point
        section = self._placeholder_renderer.render(data_to_render=self._schema.get_section(self._section_id), list_item_id=None)  # type: ignore

        groups = [
            PreviewGroup(group_schema=group).serialize() for group in section["groups"]
        ]
        section_dict: dict = {
            "title": section["title"],
            "id": section["id"],
            "blocks": [block for group in groups for block in group["blocks"]],
        }

        return [section_dict]
