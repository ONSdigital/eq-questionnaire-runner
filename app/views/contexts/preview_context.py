from typing import Generator, Mapping, Optional, Union

from app.data_models import AnswerStore, ListStore, ProgressStore, QuestionnaireStore
from app.data_models.metadata_proxy import MetadataProxy
from app.questionnaire import Location, QuestionnaireSchema
from app.views.contexts import Context
from app.views.contexts.section_preview_context import SectionPreviewContext


class PreviewContext(Context):
    def __init__(
        self,
        language: str,
        schema: QuestionnaireSchema,
        answer_store: AnswerStore,
        list_store: ListStore,
        progress_store: ProgressStore,
        metadata: Optional[MetadataProxy],
        response_metadata: Mapping[str, Union[str, int, list]],
        questionnaire_store: QuestionnaireStore,
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
        self._routing_path = None
        self.questionnaire_store = questionnaire_store

    def __call__(self) -> dict[str, Union[str, list, bool]]:
        groups = list(self.build_all_groups())
        return {
            "groups": groups,
        }

    def build_all_groups(self) -> Generator[dict, None, None]:
        """NB: Does not support repeating sections"""

        for section in self._schema.get_sections():
            section_id = section["id"]
            location = Location(
                section_id=section_id,
                block_id=self._schema.get_first_block_id_for_section(section_id),
            )
            section_preview_context = SectionPreviewContext(
                language=self._language,
                schema=self._schema,
                answer_store=self._answer_store,
                list_store=self._list_store,
                progress_store=self._progress_store,
                metadata=self._metadata,
                response_metadata=self._response_metadata,
                current_location=location,
            )

            yield from section_preview_context()["preview"]["groups"]
