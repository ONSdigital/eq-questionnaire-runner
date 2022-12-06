from decimal import Decimal

import pytest
from wtforms.validators import ValidationError

from app.forms import error_messages
from app.forms.validators import MutuallyExclusiveCheck, format_message_with_title


@pytest.mark.parametrize(
    "answer_permutations, is_mandatory, is_only_checkboxes_or_radios, error_type",
    (
        ([[], []], True, True, "MANDATORY_CHECKBOX"),
        ([None, []], True, True, "MANDATORY_CHECKBOX"),
        (["", []], True, True, "MANDATORY_CHECKBOX"),
        ([[], []], True, False, "MANDATORY_QUESTION"),
        ([None, []], True, False, "MANDATORY_QUESTION"),
        (["", []], True, False, "MANDATORY_QUESTION"),
        (
            [["British, Irish"], ["I prefer not to say"]],
            True,
            True,
            "MUTUALLY_EXCLUSIVE",
        ),
        (["123", ["I prefer not to say"]], True, True, "MUTUALLY_EXCLUSIVE"),
        (["2018-09-01", ["I prefer not to say"]], True, True, "MUTUALLY_EXCLUSIVE"),
        (["", None], True, True, "MANDATORY_CHECKBOX"),
        (
            [["British, Irish"], "I prefer not to say"],
            True,
            True,
            "MUTUALLY_EXCLUSIVE",
        ),
        (
            ["British, Irish", "I prefer not to say"],
            True,
            True,
            "MUTUALLY_EXCLUSIVE",
        ),
        (["123", "I prefer not to say"], True, True, "MUTUALLY_EXCLUSIVE"),
        (["2018-09-01", "I prefer not to say"], True, True, "MUTUALLY_EXCLUSIVE"),
    ),
)
def test_mutually_exclusive_mandatory_answers_raise_validation_error(
    answer_permutations, is_mandatory, is_only_checkboxes_or_radios, error_type
):
    validator = MutuallyExclusiveCheck(question_title="")
    with pytest.raises(ValidationError) as exc:
        validator(
            answer_values=iter(answer_permutations),
            is_mandatory=is_mandatory,
            is_only_checkboxes_or_radios=is_only_checkboxes_or_radios,
        )

    assert format_message_with_title(error_messages[error_type], "") == str(exc.value)


@pytest.mark.parametrize(
    "answer_permutations, is_mandatory",
    (
        ([["British, Irish"], []], True),
        (["123", []], True),
        (["2018-09-01", []], True),
        ([[], ["Exclusive option"]], True),
        ([None, ["I prefer not to say"]], True),
        (["", ["I prefer not to say"]], True),
        ([[], []], False),
        ([None, []], False),
        (["", []], False),
        (["", None], False),
        ([None, None], False),
        ([None, ""], False),
        ([["British, Irish"], None], True),
        (["British, Irish", None], True),
        ([None, "I prefer not to say"], True),
        (["", "I prefer not to say"], True),
        ([0, []], True),
        ([Decimal(0), []], True),
    ),
)
def test_mutually_exclusive_mandatory_answers(answer_permutations, is_mandatory):
    validator = MutuallyExclusiveCheck(question_title="")
    validator(
        answer_values=iter(answer_permutations),
        is_mandatory=is_mandatory,
        is_only_checkboxes_or_radios=True,
    )
