from typing import Union
from flask import url_for

from app.data_model.questionnaire_store import QuestionnaireStore
from app.questionnaire import QuestionnaireSchema

from .individual_response import (
    IndividualResponseHandler,
    IndividualResponseHowHandler,
    IndividualResponsePostAddressConfirmHandler,
)

__all__ = [
    "IndividualResponseHandler",
    "IndividualResponseHowHandler",
    "IndividualResponsePostAddressConfirmHandler",
    "individual_response_url",
]


def individual_response_url(
    schema: QuestionnaireSchema,
    list_item_id: str,
    questionnaire_store: QuestionnaireStore,
    journey: str,
) -> Union[str, None]:
    if "individual_response" in schema.json:
        for_list = schema.json["individual_response"]["for_list"]

        if list_item_id != questionnaire_store.list_store[for_list].primary_person:
            return url_for(
                "individual_response.request_individual_response",
                list_item_id=list_item_id,
                journey=journey,
            )
    return None
