# pylint: disable=redefined-outer-name
import pytest
import simplejson as json

from app.data_models.answer_store import Answer, AnswerStore


@pytest.fixture()
def empty_answer_store():
    answer_store = AnswerStore()
    return answer_store


@pytest.fixture()
def basic_answer_store():
    answer_store = AnswerStore()

    answer_store.add_or_update(
        Answer(answer_id="answer1", value=10, list_item_id="abc123")
    )
    answer_store.add_or_update(
        Answer(answer_id="answer2", value=20, list_item_id="xyz987")
    )
    answer_store.add_or_update(
        Answer(answer_id="another-answer2", value=25, list_item_id="xyz987")
    )

    answer_store.add_or_update(Answer(answer_id="answer3", value=30))
    answer_store.add_or_update(Answer(answer_id="another-answer3", value=35))

    answer_store.add_or_update(Answer(answer_id="to-escape", value="'Twenty Five'"))
    return answer_store


@pytest.fixture
def relationship_answer_store():
    answer_store = AnswerStore()

    answer_store.add_or_update(
        Answer(
            answer_id="relationship-answer",
            value=[
                {
                    "list_item_id": "abc123",
                    "to_list_item_id": "xyz987",
                    "relationship": "Husband or Wife",
                },
                {
                    "list_item_id": "abc123",
                    "to_list_item_id": "123abc",
                    "relationship": "Son or Daughter",
                },
                {
                    "list_item_id": "xyz987",
                    "to_list_item_id": "123abc",
                    "relationship": "Son or Daughter",
                },
            ],
        )
    )

    return answer_store


@pytest.fixture()
def store_to_serialize():
    answer_store = AnswerStore()

    answer_store.add_or_update(
        Answer(answer_id="answer1", value=10, list_item_id="abc123")
    )
    answer_store.add_or_update(
        Answer(answer_id="answer2", value=20, list_item_id="xyz987")
    )
    answer_store.add_or_update(Answer(answer_id="answer3", value=30))

    return answer_store


def test_adding_new_answer(empty_answer_store):
    answer = Answer(answer_id="4", value=25)

    empty_answer_store.add_or_update(answer)

    assert len(empty_answer_store) == 1


def test_raises_error_on_invalid_answer(empty_answer_store):

    with pytest.raises(TypeError) as e:
        empty_answer_store.add_or_update({"answer_id": "4", "value": 25})

    assert "Method only supports Answer argument type" in str(e.value)


def test_updates_answer_no_list_id(basic_answer_store):

    store_length = len(basic_answer_store)

    duplicate_answer = Answer(answer_id="answer3", value=300)

    basic_answer_store.add_or_update(duplicate_answer)

    assert len(basic_answer_store) == store_length

    assert basic_answer_store.get_answer("answer3").value == 300


def test_updates_answer_with_list_id(basic_answer_store):
    store_length = len(basic_answer_store)

    duplicate_answer = Answer(answer_id="answer1", list_item_id="abc123", value=100)

    basic_answer_store.add_or_update(duplicate_answer)

    assert len(basic_answer_store) == store_length

    assert basic_answer_store.get_answer("answer1", list_item_id="abc123").value == 100


def test_get_answer_no_list(basic_answer_store):
    assert basic_answer_store.get_answer("answer3") == Answer.from_dict(
        {"answer_id": "answer3", "list_item_id": None, "value": 30}
    )


def test_get_answer_with_list(basic_answer_store):
    assert basic_answer_store.get_answer("answer1", "abc123") == Answer.from_dict(
        {"answer_id": "answer1", "list_item_id": "abc123", "value": 10}
    )


def test_get_answer_does_not_escape_values(basic_answer_store):
    normal_answer = basic_answer_store.get_answer("answer3")
    answer_needs_escaping = basic_answer_store.get_answer("to-escape")

    assert normal_answer.value == 30
    assert answer_needs_escaping.value == "'Twenty Five'"


def test_get_answers_with_list_item_id(basic_answer_store):
    ids_to_get = ["answer2", "another-answer2"]
    answers = basic_answer_store.get_answers_by_answer_id(ids_to_get, "xyz987")

    assert len(answers) == len(ids_to_get)


def test_get_answers_no_list(basic_answer_store):
    ids_to_get = ["answer3", "another-answer3"]
    answers = basic_answer_store.get_answers_by_answer_id(ids_to_get)

    assert len(answers) == len(ids_to_get)


def test_remove_all_answers(basic_answer_store):
    assert basic_answer_store
    basic_answer_store.clear()
    assert not basic_answer_store


def test_remove_answer(basic_answer_store):
    len_before_remove = len(basic_answer_store)
    basic_answer_store.remove_answer("answer1", "abc123")
    assert len(basic_answer_store) == len_before_remove - 1


def test_remove_all_answers_for_list_item_id(relationship_answer_store):
    relationship_answer_store.remove_all_answers_for_list_item_id("abc123")
    assert relationship_answer_store.get_answer("answer1") is None


def test_remove_all_answers_for_list_item_id_doesnt_exist(relationship_answer_store):
    len_before = len(relationship_answer_store)
    relationship_answer_store.remove_all_answers_for_list_item_id("not-an-id")
    assert len(relationship_answer_store) == len_before


def test_list_serialisation(store_to_serialize):
    serialized_store = list(store_to_serialize)

    assert serialized_store == [
        Answer.from_dict(
            {"answer_id": "answer1", "value": 10, "list_item_id": "abc123"}
        ),
        Answer.from_dict(
            {"answer_id": "answer2", "value": 20, "list_item_id": "xyz987"}
        ),
        Answer.from_dict({"answer_id": "answer3", "value": 30, "list_item_id": None}),
    ]


def test_serialize_and_deserialize(basic_answer_store):
    json_serialized = json.dumps(basic_answer_store.serialize(), for_json=True)
    deserialized = AnswerStore(json.loads(json_serialized))

    assert deserialized == basic_answer_store


def test_bad_answer_type(basic_answer_store):
    with pytest.raises(TypeError):
        basic_answer_store.add_or_update({"answer_id": "test", "value": 20})
