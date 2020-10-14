from app.questionnaire.relationship_location import RelationshipLocation
from app.questionnaire.relationship_router import RelationshipRouter
from tests.app.app_context_test_case import AppContextTestCase


class TestRelationshipRouter(AppContextTestCase):
    router = RelationshipRouter(
        section_id="relationships-section",
        block_id="relationships",
        list_name="people",
        list_item_ids=["abc123", "def123", "ghi123"],
    )

    @staticmethod
    def _get_relationship_location(list_item_id, to_list_item_id):
        return RelationshipLocation(
            section_id="relationships-section",
            block_id="relationships",
            list_name="people",
            list_item_id=list_item_id,
            to_list_item_id=to_list_item_id,
        )

    def test_can_access_location(self):
        location = self._get_relationship_location(
            list_item_id="abc123",
            to_list_item_id="def123",
        )
        can_access_location = self.router.can_access_location(location)
        self.assertTrue(can_access_location)

    def test_cant_access_location(self):
        location = self._get_relationship_location(
            list_item_id="def123",
            to_list_item_id="abc123",
        )
        can_access_location = self.router.can_access_location(location)
        self.assertFalse(can_access_location)

    def test_get_first_location_url(self):
        first_location_url = self.router.get_first_location_url()
        expected_location_url = "relationships/people/abc123/to/def123"
        self.assertIn(expected_location_url, first_location_url)

    def test_get_first_location_url_with_resume(self):
        first_location_url = self.router.get_first_location_url(resume=True)
        expected_location_url = "relationships/people/abc123/to/def123/?resume=True"
        self.assertIn(expected_location_url, first_location_url)

    def test_get_last_location_url(self):
        last_location_url = self.router.get_last_location_url()
        expected_location_url = "relationships/people/def123/to/ghi123"
        self.assertIn(expected_location_url, last_location_url)

    def test_next_location_url(self):
        location = self._get_relationship_location(
            list_item_id="abc123",
            to_list_item_id="def123",
        )
        next_location_url = self.router.get_next_location_url(location)
        expected_location_url = "relationships/people/abc123/to/ghi123"
        self.assertIn(expected_location_url, next_location_url)

    def test_get_previous_location_url(self):
        location = self._get_relationship_location(
            list_item_id="abc123",
            to_list_item_id="ghi123",
        )
        previous_location_url = self.router.get_previous_location_url(location)
        expected_location_url = "relationships/people/abc123/to/def123"
        self.assertIn(expected_location_url, previous_location_url)
