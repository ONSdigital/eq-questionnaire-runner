from typing import Union

from flask import url_for

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
    "individual_response_url",
]


def individual_response_url(
    individual_response_for_list: str,
    list_item_id: str,
    questionnaire_store: QuestionnaireStore,
    journey: str = None,
) -> Union[str, None]:
    if individual_response_for_list:

        if (
            list_item_id
            != questionnaire_store.list_store[
                individual_response_for_list
            ].primary_person
        ):
            return url_for(
                "individual_response.request_individual_response",
                list_item_id=list_item_id,
                journey=journey,
            )
    return None
