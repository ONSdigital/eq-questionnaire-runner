from app.data_model.answer_store import AnswerStore
from app.forms.handlers.text_area_handler import TextAreaHandler


def test_get_length_validator():
    text_area_handler = TextAreaHandler(
        {},
        {'MAX_LENGTH_EXCEEDED': 'This is the default max length of %(max)d message'},
        AnswerStore(),
        {},
    )
    validate_with = text_area_handler.get_length_validator()

    assert (
        validate_with[0].message == 'This is the default max length of %(max)d message'
    )


def test_get_length_validator_with_message_override():
    answer = {
        'validation': {
            'messages': {
                'MAX_LENGTH_EXCEEDED': 'A message with characters %(max)d placeholder'
            }
        }
    }
    text_area_handler = TextAreaHandler(
        answer,
        {'MAX_LENGTH_EXCEEDED': 'This is the default max length message'},
        AnswerStore(),
        {},
    )

    validate_with = text_area_handler.get_length_validator()

    assert validate_with[0].message == 'A message with characters %(max)d placeholder'


def test_get_length_validator_with_max_length_override():
    answer = {'max_length': 30}

    text_area_handler = TextAreaHandler(
        answer, {'MAX_LENGTH_EXCEEDED': '%(max)d characters'}, AnswerStore(), {}
    )
    validate_with = text_area_handler.get_length_validator()

    assert validate_with[0].max == 30
