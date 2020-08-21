import pytest
from mock import Mock, MagicMock, patch

from app.views.handlers.list_action import ListAction
from app.questionnaire.location import InvalidLocationException
from tests.app.app_context_test_case import AppContextTestCase


class TestListAction(AppContextTestCase):
    def setUp(self):
        super().setUp()
        self.questionnaire_store = Mock()
        self.schema = MagicMock()
        self.request_args = MagicMock()
        self.form_data = {}
        self.current_location = Mock()
        self._return_to = "section-summary"
        self.router = Mock()
        self.parent_location = Mock()
        self._routing_path = Mock()
        self.router.can_display_summary_for_section = Mock(return_value=False)

    def test_list_action(self):
        with patch(
            "app.views.handlers.list_action.ListAction.parent_location"
        ), pytest.raises(InvalidLocationException):
            ListAction(
                self.schema,
                self.questionnaire_store,
                self.schema,
                self.current_location,
                self.request_args,
                self.form_data,
            )
        self.assertNotEqual(self, None, ListAction.get_next_location_url(self))
