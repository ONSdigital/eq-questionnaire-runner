import pytest

from app.questionnaire.rules.operations import Operations
from app.questionnaire.rules.operations_helper import OperationHelper
from app.questionnaire.rules.operator import Operator

DEFAULT_LANGUAGE = "en"


@pytest.fixture
def get_operator(mock_renderer, mock_schema):
    def _operators(operator_name):
        return Operator(
            operator_name,
            operations=Operations(
                language=DEFAULT_LANGUAGE, schema=mock_schema, renderer=mock_renderer
            ),
        )

    return _operators


@pytest.fixture
def operation_helper(schema_placeholder_renderer):
    schema, renderer = schema_placeholder_renderer
    ops_helper = OperationHelper(
        language=DEFAULT_LANGUAGE, schema=schema, renderer=renderer
    )
    return ops_helper
