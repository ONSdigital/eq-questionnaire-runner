import unittest

from app.questionnaire.placeholder_transforms import PlaceholderTransforms


class TestPlaceholderParser(unittest.TestCase):
    def setUp(self):
        self.transforms = PlaceholderTransforms(language="en")

    def test_format_currency(self):
        assert self.transforms.format_currency("11", "GBP") == "£11.00"
        assert self.transforms.format_currency("11.99", "GBP") == "£11.99"
        assert self.transforms.format_currency("11000", "USD") == "US$11,000.00"
        assert self.transforms.format_currency(0) == "£0.00"
        assert self.transforms.format_currency(0.00) == "£0.00"

    def test_format_number(self):
        assert self.transforms.format_number(123) == "123"
        assert self.transforms.format_number("123.4") == "123.4"
        assert self.transforms.format_number("123.40") == "123.4"
        assert self.transforms.format_number("1000") == "1,000"
        assert self.transforms.format_number("10000") == "10,000"
        assert self.transforms.format_number("100000000") == "100,000,000"
        assert self.transforms.format_number(0) == "0"
        assert self.transforms.format_number(0.00) == "0"
        assert self.transforms.format_number("") == ""
        assert self.transforms.format_number(None) == ""

    def test_format_list(self):
        names = ["Alice Aardvark", "Bob Berty Brown", "Dave Dixon Davies"]

        format_value = self.transforms.format_list(names)

        expected_result = (
            "<ul>"
            "<li>Alice Aardvark</li>"
            "<li>Bob Berty Brown</li>"
            "<li>Dave Dixon Davies</li>"
            "</ul>"
        )

        assert expected_result == format_value

    def test_format_possessive(self):
        assert self.transforms.format_possessive("Alice Aardvark") == "Alice Aardvark’s"
        assert (
            self.transforms.format_possessive("Dave Dixon Davies")
            == "Dave Dixon Davies’"
        )
        assert (
            self.transforms.format_possessive("Alice Aardvark's") == "Alice Aardvark’s"
        )
        assert (
            self.transforms.format_possessive("Alice Aardvark’s") == "Alice Aardvark’s"
        )

    @staticmethod
    def test_format_possessive_non_english_does_nothing():
        welsh_transforms = PlaceholderTransforms(language="cy")
        assert welsh_transforms.format_possessive("Alice Aardvark") == "Alice Aardvark"
        assert (
            welsh_transforms.format_possessive("Dave Dixon Davies")
            == "Dave Dixon Davies"
        )
        assert (
            welsh_transforms.format_possessive("Alice Aardvark's") == "Alice Aardvark's"
        )
        assert (
            welsh_transforms.format_possessive("Alice Aardvark’s") == "Alice Aardvark’s"
        )

    def test_calculate_difference(self):
        assert (
            PlaceholderTransforms.calculate_date_difference("2016-06-10", "2019-06-10")
            == "3 years"
        )
        assert (
            PlaceholderTransforms.calculate_date_difference("2018-06-10", "2019-06-10")
            == "1 year"
        )
        assert (
            PlaceholderTransforms.calculate_date_difference("2010-01-01", "2018-12-31")
            == "8 years"
        )
        assert (
            PlaceholderTransforms.calculate_date_difference("2011-01", "2015-04")
            == "4 years"
        )
        assert (
            PlaceholderTransforms.calculate_date_difference("2019-06-10", "2019-08-11")
            == "2 months"
        )
        assert (
            PlaceholderTransforms.calculate_date_difference("2019-07-10", "2019-08-11")
            == "1 month"
        )
        assert (
            PlaceholderTransforms.calculate_date_difference("2019-07-10", "2019-07-11")
            == "1 day"
        )
        assert PlaceholderTransforms.calculate_date_difference("now", "now") == "0 days"
        with self.assertRaises(ValueError):
            PlaceholderTransforms.calculate_date_difference("2018", "now")

    def test_concatenate_list(self):
        list_to_concatenate = ["Milk", "Eggs", "Flour", "Water"]

        assert (
            self.transforms.concatenate_list(list_to_concatenate, "")
            == "MilkEggsFlourWater"
        )
        assert (
            self.transforms.concatenate_list(list_to_concatenate, " ")
            == "Milk Eggs Flour Water"
        )
        assert (
            self.transforms.concatenate_list(list_to_concatenate, ", ")
            == "Milk, Eggs, Flour, Water"
        )

    def test_add(self):
        assert self.transforms.add(1, 2) == 3

    def test_format_ordinal_with_determiner(self):
        assert self.transforms.format_ordinal(1, "a_or_an") == "a 1st"
        assert self.transforms.format_ordinal(2, "a_or_an") == "a 2nd"
        assert self.transforms.format_ordinal(3, "a_or_an") == "a 3rd"
        assert self.transforms.format_ordinal(4, "a_or_an") == "a 4th"
        assert self.transforms.format_ordinal(8, "a_or_an") == "an 8th"
        assert self.transforms.format_ordinal(11, "a_or_an") == "an 11th"
        assert self.transforms.format_ordinal(12, "a_or_an") == "a 12th"
        assert self.transforms.format_ordinal(13, "a_or_an") == "a 13th"
        assert self.transforms.format_ordinal(18, "a_or_an") == "an 18th"
        assert self.transforms.format_ordinal(21, "a_or_an") == "a 21st"
        assert self.transforms.format_ordinal(22, "a_or_an") == "a 22nd"
        assert self.transforms.format_ordinal(23, "a_or_an") == "a 23rd"
        assert self.transforms.format_ordinal(111, "a_or_an") == "a 111th"
        assert self.transforms.format_ordinal(112, "a_or_an") == "a 112th"
        assert self.transforms.format_ordinal(113, "a_or_an") == "a 113th"

    def test_format_ordinal_without_determiner(self):
        assert self.transforms.format_ordinal(1) == "1st"
        assert self.transforms.format_ordinal(2) == "2nd"
        assert self.transforms.format_ordinal(3) == "3rd"
        assert self.transforms.format_ordinal(4) == "4th"
        assert self.transforms.format_ordinal(21) == "21st"

    @staticmethod
    def test_format_ordinal_with_determiner_ulster_scots():
        ulster_scots_transforms = PlaceholderTransforms(language="eo")
        assert ulster_scots_transforms.format_ordinal(1, "a_or_an") == "a 1st"
        assert ulster_scots_transforms.format_ordinal(2, "a_or_an") == "a 2nd"
        assert ulster_scots_transforms.format_ordinal(3, "a_or_an") == "a 3rd"
        assert ulster_scots_transforms.format_ordinal(4, "a_or_an") == "a 4th"
        assert ulster_scots_transforms.format_ordinal(8, "a_or_an") == "an 8th"
        assert ulster_scots_transforms.format_ordinal(11, "a_or_an") == "an 11th"

    @staticmethod
    def test_format_ordinal_without_determiner_ulster_scots():
        ulster_scots_transforms = PlaceholderTransforms(language="eo")
        assert ulster_scots_transforms.format_ordinal(1) == "1st"
        assert ulster_scots_transforms.format_ordinal(2) == "2nd"
        assert ulster_scots_transforms.format_ordinal(3) == "3rd"
        assert ulster_scots_transforms.format_ordinal(4) == "4th"
        assert ulster_scots_transforms.format_ordinal(21) == "21st"

    @staticmethod
    def test_format_ordinal_gaelic():
        gaelic_transforms = PlaceholderTransforms(language="ga")
        assert gaelic_transforms.format_ordinal(1) == "1ú"
        assert gaelic_transforms.format_ordinal(2) == "2ú"
        assert gaelic_transforms.format_ordinal(5) == "5ú"
        assert gaelic_transforms.format_ordinal(7) == "7ú"
        assert gaelic_transforms.format_ordinal(21) == "21ú"

    @staticmethod
    def test_format_ordinal_welsh():
        welsh_transforms = PlaceholderTransforms(language="cy")
        assert welsh_transforms.format_ordinal(1) == "1af"
        assert welsh_transforms.format_ordinal(2) == "2il"
        assert welsh_transforms.format_ordinal(3) == "3ydd"
        assert welsh_transforms.format_ordinal(7) == "7fed"
        assert welsh_transforms.format_ordinal(13) == "13eg"
        assert welsh_transforms.format_ordinal(18) == "18fed"
        assert welsh_transforms.format_ordinal(21) == "21ain"
        assert welsh_transforms.format_ordinal(40) == "40ain"

    def test_remove_empty_from_list(self):
        list_to_filter = [None, 0, False, "", "String"]

        assert self.transforms.remove_empty_from_list(list_to_filter) == [
            0,
            False,
            "String",
        ]

    def test_first_non_empty_item(self):
        list_to_filter = [None, 0, False, "", "String"]

        assert self.transforms.first_non_empty_item(list_to_filter) == 0

    def test_first_non_empty_item_no_valid(self):
        list_to_filter = [None, None]

        assert self.transforms.first_non_empty_item(list_to_filter) == ""

    def test_contains(self):
        list_to_check = ["abc123", "fgh789"]

        assert self.transforms.contains(list_to_check, "abc123")
        assert not self.transforms.contains(list_to_check, "def456")

    def test_list_has_items(self):
        assert self.transforms.list_has_items(["abc123", "fgh789"])
        assert not self.transforms.list_has_items([])

    def test_format_name(self):
        assert self.transforms.format_name("Joe", None, "Bloggs") == "Joe Bloggs"
        assert (
            self.transforms.format_name(
                "Joe", None, "Bloggs", include_middle_names=True
            )
            == "Joe Bloggs"
        )
        assert self.transforms.format_name("Joe", "Michael", "Bloggs") == "Joe Bloggs"
        assert (
            self.transforms.format_name(
                "Joe", "Michael", "Bloggs", include_middle_names=True
            )
            == "Joe Michael Bloggs"
        )

    def test_email_link(self):

        assert (
            self.transforms.email_link("test@email.com")
            == '<a href="mailto:test@email.com">test@email.com</a>'
        )

    def test_email_link_with_subject(self):

        assert (
            self.transforms.email_link("test@email.com", "test subject")
            == '<a href="mailto:test@email.com?subject=test%20subject">test@email.com</a>'
        )

    def test_email_link_with_subject_and_reference(self):
        assert (
            self.transforms.email_link("test@email.com", "test subject", "12345")
            == '<a href="mailto:test@email.com?subject=test%20subject%2012345">test@email.com</a>'
        )

    def test_telephone_number_link(self):

        assert (
            self.transforms.telephone_number_link("012345 67890")
            == '<a href="tel:01234567890">012345 67890</a>'
        )
