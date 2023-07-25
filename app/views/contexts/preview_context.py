from typing import Generator, MutableMapping, Optional, Union

from flask_babel import lazy_gettext

from app.data_models import (
    AnswerStore,
    ListStore,
    ProgressStore,
    SupplementaryDataStore,
)
from app.data_models.metadata_proxy import MetadataProxy
from app.questionnaire import QuestionnaireSchema
from app.views.contexts import Context
from app.views.contexts.section_preview_context import SectionPreviewContext


class PreviewNotEnabledException(Exception):
    pass


class PreviewContext(Context):
    def __init__(
        self,
        language: str,
        schema: QuestionnaireSchema,
        answer_store: AnswerStore,
        list_store: ListStore,
        progress_store: ProgressStore,
        metadata: Optional[MetadataProxy],
        response_metadata: MutableMapping[str, Union[str, int, list]],
        supplementary_data_store: SupplementaryDataStore,
    ):
        if not schema.preview_enabled:
            raise PreviewNotEnabledException

        super().__init__(
            language,
            schema,
            answer_store,
            list_store,
            progress_store,
            metadata,
            response_metadata,
            supplementary_data_store,
            placeholder_preview_mode=True,
        )

    def __call__(self) -> dict[str, Union[str, list, bool]]:
        sections = list(self.build_all_sections())
        return {
            "sections": sections,
        }

    def build_all_sections(self) -> Generator[dict, None, None]:
        """NB: Does not support repeating sections"""

        for section in self._schema.get_sections():
            section_id = section["id"]
            section_preview_context = SectionPreviewContext(
                language=self._language,
                schema=self._schema,
                answer_store=self._answer_store,
                list_store=self._list_store,
                progress_store=self._progress_store,
                supplementary_data_store=self._supplementary_data_store,
                metadata=self._metadata,
                response_metadata=self._response_metadata,
                section_id=section_id,
            )

            yield from section_preview_context()["preview"]

    @staticmethod
    def get_page_title() -> str:
        title: str = lazy_gettext("Preview survey questions")
        return title
