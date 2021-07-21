import unittest
from unittest.mock import Mock, patch

from wtforms.validators import ValidationError

from app.data_models.answer_store import Answer, AnswerStore
from app.forms import error_messages
from app.forms.validators import NumberRange
from app.jinja_filters import format_number


# pylint: disable=no-member
@patch("app.jinja_filters.flask_babel.get_locale", Mock(return_value="en_GB"))
class TestNumberRangeValidator(unittest.TestCase):
    """
    Number range validator uses the data, which is already known as integer
    """

    def setUp(self):
        self.store = AnswerStore()

        answer1 = Answer(answer_id="set-minimum", value=10)
        answer2 = Answer(answer_id="set-maximum", value=20)
        answer3 = Answer(answer_id="set-maximum-cat", value="cat")

        self.store.add_or_update(answer1)
        self.store.add_or_update(answer2)
        self.store.add_or_update(answer3)

    def tearDown(self):
        self.store.clear()

    def test_too_small_when_min_set_is_invalid(self):
        validator = NumberRange(minimum=0)

        mock_form = Mock()
        mock_field = Mock()
        mock_field.data = -10

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(
            error_messages["NUMBER_TOO_SMALL"] % {"min": 0}, str(ite.exception)
        )

    def test_too_big_when_max_set_is_invalid(self):
        validator = NumberRange(maximum=9999999999)

        mock_form = Mock()
        mock_field = Mock()
        mock_field.data = 10000000000

        with self.assertRaises(ValidationError) as ite:
            validator(mock_form, mock_field)

        self.assertEqual(
            error_messages["NUMBER_TOO_LARGE"] % {"max": format_number(9999999999)},
            str(ite.exception),
        )

    def test_within_range(self):
        validator = NumberRange(minimum=0, maximum=10)

        mock_form = Mock()
        mock_field = Mock()
        mock_field.data = 10

        try:
            validator(mock_form, mock_field)
        except ValidationError:
            self.fail("Valid integer raised ValidationError")

    def test_within_range_at_min(self):
        validator = NumberRange(minimum=0, maximum=9999999999)

        mock_form = Mock()
        mock_field = Mock()
        mock_field.data = 0

        try:
            validator(mock_form, mock_field)
        except ValidationError:
            self.fail("Valid integer raised ValidationError")

    def test_within_range_at_max(self):
        validator = NumberRange(minimum=0, maximum=9999999999)

        mock_form = Mock()
        mock_field = Mock()
        mock_field.data = 9999999999

        try:
            validator(mock_form, mock_field)
        except ValidationError:
            self.fail("Valid integer raised ValidationError")
