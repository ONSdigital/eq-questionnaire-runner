from __future__ import annotations

from typing import Iterable, Iterator

from app.data_models.answer import Answer, AnswerDict

AnswerKeyType = tuple[str, str | None]


class AnswerStore:
    """
    An object that stores and updates a collection of answers, ready for serialisation
    via the Questionnaire Store.

    Internally stores answers in the form:

    {
        (<answer_id>, <list_item_id>): {
            Answer
        }
    }
    """

    def __init__(self, answers: Iterable[AnswerDict] | None = None):
        """Instantiate an answer_store.

        Args:
            answers: If a list of answer dictionaries is provided, this will be used to initialise the store.
        """
        self.answer_map = self._build_map(answers or [])
        self._is_dirty = False

    def __iter__(self) -> Iterator[Answer]:
        return iter(self.answer_map.values())

    def __len__(self) -> int:
        return len(self.answer_map)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AnswerStore):
            return NotImplemented
        return self.answer_map == other.answer_map

    @staticmethod
    def _build_map(
        answers: Iterable[AnswerDict],
    ) -> dict[AnswerKeyType, Answer]:
        """Builds the answer_store's data structure from a list of answer dictionaries"""
        return {
            (answer["answer_id"], answer.get("list_item_id")): Answer.from_dict(answer)
            for answer in answers
        }

    @staticmethod
    def _validate(answer: Answer) -> None:
        if not isinstance(answer, Answer):
            answer_type_error_message = f"Method only supports Answer argument type, found type: {type(answer)}"
            raise TypeError(
                answer_type_error_message
            )

    @property
    def is_dirty(self) -> bool:
        return self._is_dirty

    def add_or_update(self, answer: Answer) -> bool:
        """
        Add a new answer into the answer store, or update if it exists.
        :return: True if answer updated else False
        """
        self._validate(answer)
        key = (answer.answer_id, answer.list_item_id)

        existing_answer = self.answer_map.get(key)

        if existing_answer != answer:
            self._is_dirty = True
            self.answer_map[key] = answer

            return True

        return False

    def get_answer(
        self, answer_id: str, list_item_id: str | None = None
    ) -> Answer | None:
        """Get a single answer from the store

        Args:
            answer_id: The answer id to find
            list_item_id: If not provided (None), will only match an answer with no list_item_id

        Returns:
            A single Answer or None if it doesn't exist
        """
        return self.answer_map.get((answer_id, list_item_id))

    def get_answers_by_answer_id(
        self, answer_ids: Iterable[str], list_item_id: str | None = None
    ) -> list[Answer]:
        """Get multiple answers from the store using the answer_id

        Args:
            answer_ids: list of answer ids to find
            list_item_id: list item id to match
                          If not provided (None), will only match an answer with no list_item_id

        Returns:
            A list of Answer objects
        """
        output_answers = []
        for answer_id in answer_ids:
            answer = self.answer_map.get((answer_id, list_item_id))
            if answer:
                output_answers.append(answer)

        return output_answers

    def clear(self) -> None:
        """
        Clears answers *in place*
        """
        self.answer_map.clear()

    def remove_answer(self, answer_id: str, *, list_item_id: str | None = None) -> bool:
        """
        Removes answer *in place* from the answer store.
        :return: True if answer removed else False
        """

        if self.answer_map.get((answer_id, list_item_id)):
            del self.answer_map[(answer_id, list_item_id)]
            self._is_dirty = True

            return True

        return False

    def remove_all_answers_for_list_item_ids(self, *list_item_ids: str) -> None:
        """Remove all answers associated with any of the list_item_ids passed in.
        This method iterates through the entire list of answers.

        *Not efficient.*
        """
        keys_to_delete = []
        for answer in self:
            if answer.list_item_id and answer.list_item_id in list_item_ids:
                keys_to_delete.append((answer.answer_id, answer.list_item_id))

        for key in keys_to_delete:
            del self.answer_map[key]
            self._is_dirty = True

    def serialize(self) -> list[Answer]:
        return list(self.answer_map.values())
