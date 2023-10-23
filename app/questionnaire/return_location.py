from dataclasses import asdict, dataclass


@dataclass(kw_only=True, frozen=True)
class ReturnLocation:
    """
    Used to store return locations in the questionnaire.

    return_to: The name of the type of summary page to return to
    return_to_block_id: The block_id of the block to return to
    return_to_answer_id: The answer_id of the answer to return to
    return_to_list_item_id: The list_item_id to return to if the location is associated with a list
    """

    return_to: str | None = None
    return_to_block_id: str | None = None
    return_to_answer_id: str | None = None
    return_to_list_item_id: str | None = None

    def to_dict(self, answer_id_is_anchor: bool = False) -> dict:
        attributes = asdict(self)
        if answer_id_is_anchor:
            attributes["_anchor"] = attributes["return_to_answer_id"]
            del attributes["return_to_answer_id"]
        return {k: v for k, v in attributes.items() if v is not None}
