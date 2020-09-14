import json

from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaireSameNameItems(IntegrationTestCase):
    def get_link(self, row_index, text):
        selector = f"tbody:nth-child({row_index}) td:last-child a"
        selected = self.getHtmlSoup().select(selector)

        filtered = [html for html in selected if text in html.get_text()]

        return filtered[0].get("href")

    def test_same_name_items(self):
        self.launchSurvey("test_list_collector_same_name_items", roles=["dumper"])

        self.post({"you-live-here": "Yes"})
        self.post({"first-name": "James", "middle-names": "Brian", "last-name": "May"})
        self.post({"anyone-else": "Yes"})
        self.post({"first-name": "James", "middle-names": "Roger", "last-name": "May"})

        self.get("/dump/debug")

        actual = json.loads(self.getResponseData())

        item_id_a = actual["LISTS"][0]["items"][0]
        item_id_b = actual["LISTS"][0]["items"][1]

        assert item_id_a in actual["LISTS"][0]["same_name_items"]
        assert item_id_b in actual["LISTS"][0]["same_name_items"]

    def test_same_name_items_edit_primary(self):
        self.launchSurvey("test_list_collector_same_name_items", roles=["dumper"])

        self.post({"you-live-here": "Yes"})
        self.post({"first-name": "James", "last-name": "May"})
        self.post({"anyone-else": "Yes"})
        self.post({"first-name": "James", "last-name": "May"})

        primary_person_change_link = self.get_link(1, "Change")

        self.get(primary_person_change_link)

        self.post({"first-name": "Joe", "last-name": "May"})

        self.get("/dump/debug")

        actual = json.loads(self.getResponseData())

        assert "same_name_items" not in actual["LISTS"][0]

    def test_same_name_remove_primary(self):
        self.launchSurvey("test_list_collector_same_name_items", roles=["dumper"])

        self.post({"you-live-here": "Yes"})
        self.post({"first-name": "James", "last-name": "May"})
        self.post({"anyone-else": "Yes"})
        self.post({"first-name": "James", "last-name": "May"})

        self.get("/questionnaire/primary-person-list-collector")

        self.post({"you-live-here": "No"})

        self.get("/dump/debug")

        actual = json.loads(self.getResponseData())

        assert "same_name_items" not in actual["LISTS"][0]

    def test_same_name_items_remove_non_primary(self):
        self.launchSurvey("test_list_collector_same_name_items", roles=["dumper"])

        self.post({"you-live-here": "Yes"})
        self.post({"first-name": "James", "last-name": "May"})
        self.post({"anyone-else": "Yes"})
        self.post({"first-name": "James", "last-name": "May"})

        first_person_remove_link = self.get_link(2, "Remove")

        self.get(first_person_remove_link)

        self.post({"remove-confirmation": "Yes"})

        self.get("/dump/debug")

        actual = json.loads(self.getResponseData())

        assert "same_name_items" not in actual["LISTS"][0]

    def test_same_name_items_edit_non_primary(self):
        self.launchSurvey("test_list_collector_same_name_items", roles=["dumper"])

        self.post({"you-live-here": "Yes"})
        self.post({"first-name": "Joe", "last-name": "Smith"})
        self.post({"anyone-else": "Yes"})
        self.post({"first-name": "Barry", "last-name": "Bloggs"})

        first_person_change_link = self.get_link(2, "Change")

        self.get(first_person_change_link)

        self.post({"first-name": "Joe", "last-name": "Smith"})

        self.get("/dump/debug")

        actual = json.loads(self.getResponseData())

        item_id_a = actual["LISTS"][0]["items"][0]
        item_id_b = actual["LISTS"][0]["items"][1]

        assert item_id_a in actual["LISTS"][0]["same_name_items"]
        assert item_id_b in actual["LISTS"][0]["same_name_items"]
