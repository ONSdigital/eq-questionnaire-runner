from flask import url_for
from typing import Mapping, Union

from app.data_model.questionnaire_store import QuestionnaireStore

from .individual_response import (
    IndividualResponseHandler,
    IndividualResponseHowHandler,
    IndividualResponsePostAddressConfirmHandler,
)

__all__ = [
    "IndividualResponseHandler",
    "IndividualResponseHowHandler",
    "IndividualResponsePostAddressConfirmHandler",
    "individual_response_url"
]


def individual_response_url(schema: Mapping, list_item_id: str, questionnaire_store: QuestionnaireStore) -> Union[str, None]:
    if "individual_response" in schema.json:
        for_list = schema.json["individual_response"]["for_list"]

        if list_item_id != questionnaire_store.list_store._lists[for_list].primary_person:
            return url_for(
                "individual_response.request_individual_response",
                list_item_id=list_item_id,
            )
    return None
