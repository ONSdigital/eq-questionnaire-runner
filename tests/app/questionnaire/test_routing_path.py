from unittest import TestCase

from app.questionnaire.routing_path import RoutingPath


class TestRouter(TestCase):
    def setUp(self):
        self.block_ids = ["block-a", "block-b", "block-c", "block-b", "block-c"]
        self.section_id = "section-1"
        self.list_item_id = "list_item_id"
        self.list_name = "list_name"
        self.routing_path = RoutingPath(
            self.block_ids,
            section_id=self.section_id,
            list_item_id=self.list_item_id,
            list_name=self.list_name,
        )
        super().setUp()

    def test_eq_to_routing_path(self):
        self.assertEqual(self.routing_path, self.routing_path)

    def test_eq_to_list(self):
        self.assertEqual(self.block_ids, self.routing_path)

    def test_eq_to_tuple(self):
        self.assertEqual(tuple(self.block_ids), self.routing_path)

    def test_len(self):
        self.assertEqual(len(self.block_ids), len(self.routing_path))

    def test_reversed(self):
        self.assertEqual(
            list(reversed(self.block_ids)), list(reversed(self.routing_path))
        )

    def test_contains_true(self):
        self.assertIn(self.block_ids[0], self.routing_path)
        self.assertNotIn("block-z", self.routing_path)

    def test_iter(self):
        self.assertEqual(self.block_ids[0], next(iter(self.routing_path)))

    def test_getitem(self):
        self.assertEqual(self.block_ids[0], self.routing_path[0])

    def test_properties(self):
        self.assertEqual(self.block_ids, self.routing_path)
        self.assertEqual(self.section_id, self.routing_path.section_id)
        self.assertEqual(self.list_item_id, self.routing_path.list_item_id)
        self.assertEqual(self.list_name, self.routing_path.list_name)
