from typing import Generator, Mapping, Optional, Union

from flask_babel import lazy_gettext

from app.data_models import AnswerStore, ListStore, ProgressStore
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
        response_metadata: Mapping[str, Union[str, int, list]],
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
        )

    def __call__(self) -> dict[str, Union[str, list, bool]]:
        groups = list(self.build_all_groups())
        return {
            "groups": groups,
        }

    def build_all_groups(self) -> Generator[dict, None, None]:
        """NB: Does not support repeating sections"""

        for section in self._schema.get_sections():
            section_id = section["id"]
            section_preview_context = SectionPreviewContext(
                language=self._language,
                schema=self._schema,
                answer_store=self._answer_store,
                list_store=self._list_store,
                progress_store=self._progress_store,
                metadata=self._metadata,
                response_metadata=self._response_metadata,
                section_id=section_id,
            )

            yield from section_preview_context()["preview"]["groups"]

    @staticmethod
    def get_page_title() -> str:
        title: str = lazy_gettext("Preview survey questions")
        return title
