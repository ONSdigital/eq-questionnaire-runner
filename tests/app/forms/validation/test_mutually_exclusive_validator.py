import unittest

from wtforms.validators import ValidationError

from app.forms import error_messages
from app.forms.validators import MutuallyExclusiveCheck, format_message_with_title


class TestMutuallyExclusive(unittest.TestCase):
    def setUp(self):
        self.question_title = ""
        self.validator = MutuallyExclusiveCheck(question_title=self.question_title)

    def test_mutually_exclusive_mandatory_checkbox_exception(self):
        answer_permutations = [[[], []], [None, []], ["", []]]

        for values in answer_permutations:
            with self.assertRaises(ValidationError) as ite:
                self.validator(
                    answer_values=iter(values),
                    is_mandatory=True,
                    is_only_checkboxes=True,
                )

            self.assertEqual(
                format_message_with_title(
                    error_messages["MANDATORY_CHECKBOX"], self.question_title
                ),
                str(ite.exception),
            )

    def test_mutually_exclusive_mandatory_exception(self):
        answer_permutations = [[[], []], [None, []], ["", []]]

        for values in answer_permutations:
            with self.assertRaises(ValidationError) as ite:
                self.validator(
                    answer_values=iter(values),
                    is_mandatory=True,
                    is_only_checkboxes=False,
                )

            self.assertEqual(
                format_message_with_title(
                    error_messages["MANDATORY_QUESTION"], self.question_title
                ),
                str(ite.exception),
            )

    def test_mutually_exclusive_passes_when_optional(self):
        answer_permutations = [[[], []], [None, []], ["", []]]

        for values in answer_permutations:
            self.validator(
                answer_values=iter(values), is_mandatory=False, is_only_checkboxes=True
            )

    def test_mutually_exclusive_exception(self):
        answer_permutations = [
            [["British, Irish"], ["I prefer not to say"]],
            ["123", ["I prefer not to say"]],
            ["2018-09-01", ["I prefer not to say"]],
        ]

        for values in answer_permutations:
            with self.assertRaises(ValidationError) as ite:
                self.validator(
                    answer_values=iter(values),
                    is_mandatory=True,
                    is_only_checkboxes=True,
                )

            self.assertEqual(error_messages["MUTUALLY_EXCLUSIVE"], str(ite.exception))

    def test_mutually_exclusive_pass(self):
        answer_permutations = [
            [["British, Irish"], []],
            ["123", []],
            ["2018-09-01", []],
            [[], ["Exclusive option"]],
            [None, ["I prefer not to say"]],
            ["", ["I prefer not to say"]],
        ]

        for values in answer_permutations:
            self.validator(
                answer_values=iter(values), is_mandatory=True, is_only_checkboxes=True
            )
