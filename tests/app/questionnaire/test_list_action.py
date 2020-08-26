import pytest
from mock import Mock, MagicMock, patch

from app.views.handlers.list_action import ListAction
from app.questionnaire.location import InvalidLocationException
from app.questionnaire.routing_path import RoutingPath
from app.questionnaire.location import Location
from app.questionnaire.router import Router
from app.data_model.answer_store import AnswerStore
from app.data_model.list_store import ListStore
from app.data_model.progress_store import ProgressStore, CompletionStatus
from tests.app.app_context_test_case import AppContextTestCase


class TestListAction(AppContextTestCase):
    def setUp(self):
        super().setUp()
        self.answer_store = AnswerStore()
        self.list_store = ListStore()
        self.metadata = {}
        self.questionnaire_store = Mock()
        self.schema = MagicMock()
        self.request_args = MagicMock()
        self.form_data = {}
        self.parent_location = Mock()
        self._routing_path = RoutingPath(
            ["block-1", "block-2", "block-1"], section_id="section-1"
        )
        self._return_to = "section-summary"
        self.current_location = Location(section_id="section-1", block_id="block-1")
        self.progress_store = ProgressStore(
            [
                {
                    "section_id": "section-1",
                    "list_item_id": None,
                    "status": CompletionStatus.IN_PROGRESS,
                    "block_ids": ["block-1"],
                }
            ]
        )
        self.router = Router(
            self.schema,
            self.answer_store,
            self.list_store,
            self.progress_store,
            self.metadata,
        )
        self.router.can_display_section_summary = Mock(return_value=False)

    def test_last_block_no_section_summary_next_location_url(self):

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
        next_location = ListAction.get_next_location_url(self)
        self.assertIn("/questionnaire/block-2/", next_location)
