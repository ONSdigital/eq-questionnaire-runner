from typing import Generator, Union

from flask_babel import lazy_gettext

from app.data_models.questionnaire_store import DataStores
from app.questionnaire import QuestionnaireSchema
from app.views.contexts import Context
from app.views.contexts.section_preview_context import SectionPreviewContext


class PreviewNotEnabledException(Exception):
    pass


class PreviewContext(Context):
    def __init__(
        self, language: str, schema: QuestionnaireSchema, data_stores: DataStores
    ):
        if not schema.preview_enabled:
            raise PreviewNotEnabledException

        super().__init__(
            language,
            schema,
            data_stores,
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
                data_stores=self._data_stores,
                section_id=section_id,
            )

            yield from section_preview_context()["preview"]

    @staticmethod
    def get_page_title() -> str:
        title: str = lazy_gettext("Preview survey questions")
        return title
