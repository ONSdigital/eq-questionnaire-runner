from mock import MagicMock

from app.data_models import Answer, ListStore
from app.data_models.answer_store import AnswerStore
from app.questionnaire.rules.rule_evaluator import RuleEvaluator
from app.views.contexts.summary.question import Question
from tests.app.app_context_test_case import AppContextTestCase


class TestQuestion(AppContextTestCase):  # pylint: disable=too-many-public-methods
    def setUp(self):
        super().setUp()
        self.answer_schema = MagicMock()
        self.answer_store = AnswerStore()
        self.list_store = ListStore()
        self.schema = MagicMock()
        self.metadata = {}
        self.response_metadata = {}

    def get_rule_evaluator(self):
        return RuleEvaluator(
            schema=self.schema,
            answer_store=self.answer_store,
            list_store=self.list_store,
            metadata=self.metadata,
            response_metadata=self.response_metadata,
            location=None,
        )

    @staticmethod
    def dynamic_answer_options_schema():
        return {
            "dynamic_options": {
                "values": {
                    "map": [
                        {"format-date": ["self", "yyyy-MM-dd"]},
                        {
                            "date-range": [
                                {
                                    "date": [
                                        {
                                            "source": "response_metadata",
                                            "identifier": "started_at",
                                        },
                                        {"day_of_week": "MONDAY"},
                                    ]
                                },
                                3,
                            ]
                        },
                    ]
                },
                "transform": {"format-date": [{"date": ["self"]}, "EEEE d MMMM yyyy"]},
            },
        }

    @staticmethod
    def get_question_schema(answer_schema):
        return {
            "id": "question_id",
            "title": "question_title",
            "type": "General",
            "answers": [answer_schema],
        }

    def test_create_question(self):
        # Given
        question_title = "question_title"
        question_schema = {
            "id": "question_id",
            "title": question_title,
            "type": "GENERAL",
            "answers": [self.answer_schema],
        }

        # When
        question = Question(
            question_schema,
            answer_store=self.answer_store,
            schema=self.schema,
            list_item_id=None,
            rule_evaluator=self.get_rule_evaluator(),
        )

        # Then
        self.assertEqual(question.id, "question_id")
        self.assertEqual(question.title, question_title)
        self.assertEqual(len(question.answers), 1)

    def test_create_question_with_no_answers(self):
        # Given
        question_title = "question_title"
        question_schema = {
            "id": "question_id",
            "title": question_title,
            "type": "GENERAL",
            "answers": [],
        }

        # When
        question = Question(
            question_schema,
            answer_store=self.answer_store,
            schema=self.schema,
            list_item_id=None,
            rule_evaluator=self.get_rule_evaluator(),
        )

        # Then
        self.assertEqual(question.id, "question_id")
        self.assertEqual(question.title, question_title)
        self.assertEqual(len(question.answers), 0)

    def test_create_question_with_answer_label_when_empty_title(self):
        # Given
        answer_schema = {
            "type": "Number",
            "id": "age-answer",
            "mandatory": True,
            "label": "Age",
        }
        question_schema = {
            "id": "question_id",
            "title": "",
            "type": "GENERAL",
            "answers": [answer_schema],
        }

        # When
        question = Question(
            question_schema,
            answer_store=self.answer_store,
            schema=self.schema,
            list_item_id=None,
            rule_evaluator=self.get_rule_evaluator(),
        )

        # Then
        self.assertEqual(question.title, "Age")
        self.assertEqual(len(question.answers), 1)

    def test_concatenate_textfield_answers(self):
        answer_separators = {"Newline": "<br>", "Space": " "}

        for concatenation_type, concatenation_character in answer_separators.items():
            with self.subTest(
                concatenation_type=concatenation_type,
                concatenation_character=concatenation_character,
            ):
                # Given
                self.answer_store.add_or_update(
                    Answer(answer_id="address-line-1", value="Cardiff Rd")
                )
                self.answer_store.add_or_update(
                    Answer(answer_id="town-city", value="Newport")
                )
                self.answer_store.add_or_update(
                    Answer(answer_id="postcode", value="NP10 8XG")
                )

                address_line_1 = {
                    "id": "address-line-1",
                    "label": "Address line 1",
                    "mandatory": False,
                    "type": "TextField",
                }
                address_line_2 = {
                    "id": "address-line-2",
                    "label": "Address line 2",
                    "mandatory": False,
                    "type": "TextField",
                }
                town_city = {
                    "id": "town-city",
                    "label": "Town or City",
                    "mandatory": False,
                    "type": "TextField",
                }
                county = {
                    "id": "county",
                    "label": "County",
                    "mandatory": False,
                    "type": "TextField",
                }
                postcode = {
                    "id": "postcode",
                    "label": "Postcode",
                    "mandatory": False,
                    "type": "TextField",
                }

                question_schema = {
                    "id": "question_id",
                    "title": "question_title",
                    "type": "General",
                    "answers": [
                        address_line_1,
                        address_line_2,
                        town_city,
                        county,
                        postcode,
                    ],
                    "summary": {"concatenation_type": concatenation_type},
                }

                # When
                question = Question(
                    question_schema,
                    answer_store=self.answer_store,
                    schema=self.schema,
                    list_item_id=None,
                    rule_evaluator=self.get_rule_evaluator(),
                )

                # Then
                self.assertEqual(
                    question.answers[0]["value"],
                    f"Cardiff Rd{concatenation_character}Newport{concatenation_character}NP10 8XG",
                )
                self.assertEqual(len(question.answers), 1)

    def test_concatenate_number_and_checkbox_answers(self):
        answer_separators = {"Newline": "<br>", "Space": " "}

        for concatenation_type, concatenation_character in answer_separators.items():
            with self.subTest(
                concatenation_type=concatenation_type,
                concatenation_character=concatenation_character,
            ):
                # Given
                self.answer_store.add_or_update(Answer(answer_id="age", value=7))
                self.answer_store.add_or_update(
                    Answer(answer_id="estimate", value=["This age is an estimate"])
                )

                age_answer_schema = {
                    "id": "age",
                    "label": "Enter your age",
                    "mandatory": False,
                    "type": "Number",
                }
                checkbox_answer_schema = {
                    "id": "estimate",
                    "mandatory": False,
                    "options": [
                        {
                            "label": "This age is an estimate",
                            "value": "This age is an estimate",
                        }
                    ],
                    "type": "Checkbox",
                }

                question_schema = {
                    "id": "question_id",
                    "title": "question_title",
                    "type": "General",
                    "answers": [age_answer_schema, checkbox_answer_schema],
                    "summary": {"concatenation_type": concatenation_type},
                }

                # When
                question = Question(
                    question_schema,
                    answer_store=self.answer_store,
                    schema=self.schema,
                    list_item_id=None,
                    rule_evaluator=self.get_rule_evaluator(),
                )

                # Then
                self.assertEqual(
                    question.answers[0]["value"],
                    f"7{concatenation_character}This age is an estimate",
                )
                self.assertEqual(len(question.answers), 1)

    def test_create_question_with_multiple_answers(self):
        # Given
        self.answer_store.add_or_update(Answer(answer_id="answer_1", value="Han"))
        self.answer_store.add_or_update(Answer(answer_id="answer_2", value="Solo"))
        first_answer_schema = {"id": "answer_1", "label": "First name", "type": "text"}
        second_answer_schema = {"id": "answer_2", "label": "Surname", "type": "text"}
        question_schema = {
            "id": "question_id",
            "title": "question_title",
            "type": "GENERAL",
            "answers": [first_answer_schema, second_answer_schema],
        }

        # When
        question = Question(
            question_schema,
            answer_store=self.answer_store,
            schema=self.schema,
            list_item_id=None,
            rule_evaluator=self.get_rule_evaluator(),
        )

        # Then
        self.assertEqual(len(question.answers), 2)
        self.assertEqual(question.answers[0]["value"], "Han")
        self.assertEqual(question.answers[1]["value"], "Solo")

    def test_merge_date_range_answers(self):
        # Given
        self.answer_store.add_or_update(
            Answer(answer_id="answer_1", value="13/02/2016")
        )
        self.answer_store.add_or_update(
            Answer(answer_id="answer_2", value="13/09/2016")
        )
        first_date_answer_schema = {"id": "answer_1", "label": "From", "type": "date"}
        second_date_answer_schema = {"id": "answer_2", "label": "To", "type": "date"}
        question_schema = {
            "id": "question_id",
            "title": "question_title",
            "type": "DateRange",
            "answers": [first_date_answer_schema, second_date_answer_schema],
        }

        # When
        question = Question(
            question_schema,
            answer_store=self.answer_store,
            schema=self.schema,
            list_item_id=None,
            rule_evaluator=self.get_rule_evaluator(),
        )

        # Then
        self.assertEqual(len(question.answers), 1)
        self.assertEqual(question.answers[0]["value"]["from"], "13/02/2016")
        self.assertEqual(question.answers[0]["value"]["to"], "13/09/2016", "%d/%m/%Y")

    def test_merge_multiple_date_range_answers(self):
        # Given
        self.answer_store.add_or_update(
            Answer(answer_id="answer_1", value="13/02/2016")
        )
        self.answer_store.add_or_update(
            Answer(answer_id="answer_2", value="13/09/2016")
        )
        self.answer_store.add_or_update(
            Answer(answer_id="answer_3", value="13/03/2016")
        )
        self.answer_store.add_or_update(
            Answer(answer_id="answer_4", value="13/10/2016")
        )

        first_date_answer_schema = {"id": "answer_1", "label": "From", "type": "date"}
        second_date_answer_schema = {"id": "answer_2", "label": "To", "type": "date"}
        third_date_answer_schema = {
            "id": "answer_3",
            "label": "First period",
            "type": "date",
        }
        fourth_date_answer_schema = {
            "id": "answer_4",
            "label": "Second period",
            "type": "date",
        }
        question_schema = {
            "id": "question_id",
            "title": "question_title",
            "type": "DateRange",
            "answers": [
                first_date_answer_schema,
                second_date_answer_schema,
                third_date_answer_schema,
                fourth_date_answer_schema,
            ],
        }

        # When
        question = Question(
            question_schema,
            answer_store=self.answer_store,
            schema=self.schema,
            list_item_id=None,
            rule_evaluator=self.get_rule_evaluator(),
        )

        # Then
        self.assertEqual(len(question.answers), 2)
        self.assertEqual(question.answers[0]["value"]["from"], "13/02/2016")
        self.assertEqual(question.answers[0]["value"]["to"], "13/09/2016", "%d/%m/%Y")
        self.assertEqual(question.answers[1]["value"]["from"], "13/03/2016", "%d/%m/%Y")
        self.assertEqual(question.answers[1]["value"]["to"], "13/10/2016", "%d/%m/%Y")

    def test_checkbox_button_options(self):
        # Given
        self.answer_store.add_or_update(
            Answer(answer_id="answer_1", value=["Light Side", "Dark Side"])
        )

        options = [
            {"label": "Light Side label", "value": "Light Side"},
            {"label": "Dark Side label", "value": "Dark Side"},
        ]
        answer_schema = {
            "id": "answer_1",
            "label": "Which side?",
            "type": "Checkbox",
            "options": options,
        }
        question_schema = {
            "id": "question_id",
            "title": "question_title",
            "type": "GENERAL",
            "answers": [answer_schema],
        }

        # When
        question = Question(
            question_schema,
            answer_store=self.answer_store,
            schema=self.schema,
            list_item_id=None,
            rule_evaluator=self.get_rule_evaluator(),
        )

        # Then
        self.assertEqual(len(question.answers[0]["value"]), 2)
        self.assertEqual(question.answers[0]["value"][0]["label"], "Light Side label")
        self.assertEqual(question.answers[0]["value"][1]["label"], "Dark Side label")

    def test_checkbox_button_detail_answer_empty(self):
        # Given
        self.answer_store.add_or_update(
            Answer(answer_id="answer_1", value=["other", ""])
        )

        options = [
            {"label": "Light Side", "value": "Light Side"},
            {
                "label": "Other option label",
                "value": "other",
                "other": {"label": "Please specify other"},
            },
        ]
        answer_schema = {
            "id": "answer_1",
            "label": "Which side?",
            "type": "Checkbox",
            "options": options,
        }
        question_schema = {
            "id": "question_id",
            "title": "question_title",
            "type": "GENERAL",
            "answers": [answer_schema],
        }

        # When
        question = Question(
            question_schema,
            answer_store=self.answer_store,
            schema=self.schema,
            list_item_id=None,
            rule_evaluator=self.get_rule_evaluator(),
        )

        # Then
        self.assertEqual(len(question.answers[0]["value"]), 1)
        self.assertEqual(question.answers[0]["value"][0]["label"], "Other option label")
        self.assertEqual(question.answers[0]["value"][0]["detail_answer_value"], None)

    def test_checkbox_answer_with_detail_answer_returns_the_value(self):
        # Given
        self.answer_store.add_or_update(
            Answer(answer_id="answer_1", value=["Light Side", "Other"])
        )
        self.answer_store.add_or_update(Answer(answer_id="child_answer", value="Test"))

        options = [
            {"label": "Light Side", "value": "Light Side"},
            {
                "label": "Other",
                "value": "Other",
                "detail_answer": {"id": "child_answer", "type": "TextField"},
            },
        ]
        answer_schema = [
            {
                "id": "answer_1",
                "label": "Which side?",
                "type": "Checkbox",
                "options": options,
            }
        ]
        question_schema = {
            "id": "question_id",
            "title": "question_title",
            "type": "GENERAL",
            "answers": answer_schema,
        }

        # When
        question = Question(
            question_schema,
            answer_store=self.answer_store,
            schema=self.schema,
            list_item_id=None,
            rule_evaluator=self.get_rule_evaluator(),
        )

        # Then
        self.assertEqual(len(question.answers[0]["value"]), 2)
        self.assertEqual(question.answers[0]["value"][1]["detail_answer_value"], "Test")

    def test_checkbox_answer_with_numeric_detail_answer_returns_number(self):
        # Given
        self.answer_store.add_or_update(
            Answer(answer_id="answer_1", value=["1", "Other"])
        )
        self.answer_store.add_or_update(Answer(answer_id="child_answer", value=2))

        options = [
            {"label": "1", "value": "1"},
            {
                "label": "Other",
                "value": "Other",
                "detail_answer": {"id": "child_answer", "type": "Number"},
            },
        ]
        answer_schema = [
            {
                "id": "answer_1",
                "label": "How many cakes have you had today?",
                "type": "Checkbox",
                "options": options,
            }
        ]
        question_schema = {
            "id": "question_id",
            "title": "question_title",
            "type": "GENERAL",
            "answers": answer_schema,
        }

        # When
        question = Question(
            question_schema,
            answer_store=self.answer_store,
            schema=self.schema,
            list_item_id=None,
            rule_evaluator=self.get_rule_evaluator(),
        )

        # Then
        self.assertEqual(len(question.answers[0]["value"]), 2)
        self.assertEqual(question.answers[0]["value"][1]["detail_answer_value"], 2)

    def test_checkbox_button_other_option_text(self):
        # Given
        self.answer_store.add_or_update(
            Answer(answer_id="answer_1", value=["Light Side", "other"])
        )
        self.answer_store.add_or_update(
            Answer(answer_id="child_answer", value="Neither")
        )
        options = [
            {"label": "Light Side", "value": "Light Side"},
            {
                "label": "other",
                "value": "other",
                "detail_answer": {"id": "child_answer"},
            },
        ]
        answer_schema = {
            "id": "answer_1",
            "label": "Which side?",
            "type": "Checkbox",
            "options": options,
        }
        question_schema = {
            "id": "question_id",
            "title": "question_title",
            "type": "GENERAL",
            "answers": [answer_schema],
        }

        # When
        question = Question(
            question_schema,
            answer_store=self.answer_store,
            schema=self.schema,
            list_item_id=None,
            rule_evaluator=self.get_rule_evaluator(),
        )

        # Then
        self.assertEqual(len(question.answers[0]["value"]), 2)
        self.assertEqual(question.answers[0]["value"][0]["label"], "Light Side")
        self.assertEqual(
            question.answers[0]["value"][1]["detail_answer_value"], "Neither"
        )

    def test_checkbox_button_none_selected_should_be_none(self):
        # Given
        self.answer_store.add_or_update(Answer(answer_id="answer_1", value=[]))
        options = [{"label": "Light Side", "value": "Light Side"}]
        answer_schema = {
            "id": "answer_1",
            "label": "Which side?",
            "type": "Checkbox",
            "options": options,
        }
        question_schema = {
            "id": "question_id",
            "title": "question_title",
            "type": "GENERAL",
            "answers": [answer_schema],
        }

        # When
        question = Question(
            question_schema,
            answer_store=self.answer_store,
            schema=self.schema,
            list_item_id=None,
            rule_evaluator=self.get_rule_evaluator(),
        )

        # Then
        self.assertEqual(question.answers[0]["value"], None)

    def test_radio_button_none_selected_should_be_none(self):
        # Given
        options = [{"label": "Light Side", "value": "Light Side"}]
        answer_schema = {
            "id": "answer_1",
            "label": "Which side?",
            "type": "Radio",
            "options": options,
        }
        question_schema = {
            "id": "question_id",
            "title": "question_title",
            "type": "GENERAL",
            "answers": [answer_schema],
        }

        # When
        question = Question(
            question_schema,
            answer_store=self.answer_store,
            schema=self.schema,
            list_item_id=None,
            rule_evaluator=self.get_rule_evaluator(),
        )

        # Then
        self.assertEqual(question.answers[0]["value"], None)

    def test_radio_answer_with_detail_answer_returns_the_value(self):
        # Given
        self.answer_store.add_or_update(Answer(answer_id="answer_1", value="Other"))
        self.answer_store.add_or_update(Answer(answer_id="child_answer", value="Test"))
        options = [
            {
                "label": "Other",
                "value": "Other",
                "detail_answer": {"id": "child_answer", "type": "TextField"},
            }
        ]
        answer_schema = [
            {
                "id": "answer_1",
                "label": "Which side?",
                "type": "Radio",
                "options": options,
            }
        ]
        question_schema = {
            "id": "question_id",
            "title": "question_title",
            "type": "GENERAL",
            "answers": answer_schema,
        }

        # When
        question = Question(
            question_schema,
            answer_store=self.answer_store,
            schema=self.schema,
            list_item_id=None,
            rule_evaluator=self.get_rule_evaluator(),
        )

        # Then
        self.assertEqual(question.answers[0]["value"]["detail_answer_value"], "Test")

    def test_radio_answer_with_numeric_detail_answer_returns_number(self):
        # Given
        self.answer_store.add_or_update(Answer(answer_id="answer_1", value="Other"))
        self.answer_store.add_or_update(Answer(answer_id="child_answer", value=1))
        options = [
            {"label": 1, "value": 1},
            {
                "label": "Other",
                "value": "Other",
                "detail_answer": {"id": "child_answer", "type": "Number"},
            },
        ]
        answer_schema = [
            {
                "id": "answer_1",
                "label": "How many cakes have you had today?",
                "type": "Radio",
                "options": options,
            }
        ]
        question_schema = {
            "id": "question_id",
            "title": "question_title",
            "type": "GENERAL",
            "answers": answer_schema,
        }

        # When
        question = Question(
            question_schema,
            answer_store=self.answer_store,
            schema=self.schema,
            list_item_id=None,
            rule_evaluator=self.get_rule_evaluator(),
        )

        # Then
        self.assertEqual(question.answers[0]["value"]["detail_answer_value"], 1)

    def test_dropdown_none_selected_should_be_none(self):
        # Given
        options = [{"label": "Light Side", "value": "Light Side"}]
        answer_schema = {
            "id": "answer_1",
            "label": "Which side?",
            "type": "Dropdown",
            "options": options,
        }
        question_schema = {
            "id": "question_id",
            "title": "question_title",
            "type": "GENERAL",
            "answers": [answer_schema],
        }

        # When
        question = Question(
            question_schema,
            answer_store=self.answer_store,
            schema=self.schema,
            list_item_id=None,
            rule_evaluator=self.get_rule_evaluator(),
        )

        # Then
        self.assertEqual(question.answers[0]["value"], None)

    def test_dropdown_selected_option_label(self):
        # Given
        options = [
            {"label": "Light Side label", "value": "Light Side"},
            {"label": "Dark Side label", "value": "Dark Side"},
        ]
        answer_schema = {
            "id": "answer_1",
            "label": "Which side?",
            "type": "Dropdown",
            "options": options,
        }
        question_schema = {
            "id": "question_id",
            "title": "question_title",
            "type": "GENERAL",
            "answers": [answer_schema],
        }

        self.answer_store.add_or_update(Answer(answer_id="answer_1", value="Dark Side"))

        # When
        question = Question(
            question_schema,
            answer_store=self.answer_store,
            schema=self.schema,
            list_item_id=None,
            rule_evaluator=self.get_rule_evaluator(),
        )

        # Then
        self.assertEqual(question.answers[0]["value"], "Dark Side label")

    def test_dynamic_checkbox_answer_options(self):
        # Given
        answer_schema = {
            "id": "dynamic-checkbox-answer",
            "label": "Which side?",
            "type": "Checkbox",
            **self.dynamic_answer_options_schema(),
        }
        question_schema = self.get_question_schema(answer_schema)

        self.answer_store = AnswerStore(
            [
                {
                    "answer_id": "dynamic-checkbox-answer",
                    "value": ["2020-12-29", "2020-12-30", "2020-12-31"],
                }
            ]
        )
        self.response_metadata = {"started_at": "2021-01-01T09:00:00.220038+00:00"}

        # When
        question = Question(
            question_schema,
            answer_store=self.answer_store,
            schema=self.schema,
            list_item_id=None,
            rule_evaluator=self.get_rule_evaluator(),
        )

        # Then
        self.assertEqual(
            question.answers[0]["value"],
            [
                {
                    "label": "Tuesday 29 December 2020",
                    "detail_answer_value": None,
                },
                {"detail_answer_value": None, "label": "Wednesday 30 December 2020"},
            ],
        )

    def test_dynamic_answer_options(self):
        data_set = [
            # answer_type, answer_store_value, expected_output
            (
                "Radio",
                "2020-12-29",
                {"detail_answer_value": None, "label": "Tuesday 29 December 2020"},
            ),
            (
                "Checkbox",
                ["2020-12-29", "2020-12-30"],
                [
                    {
                        "label": "Tuesday 29 December 2020",
                        "detail_answer_value": None,
                    },
                    {
                        "detail_answer_value": None,
                        "label": "Wednesday 30 December 2020",
                    },
                ],
            ),
            ("Dropdown", "2020-12-30", "Wednesday 30 December 2020"),
        ]

        for answer_type, answer_store_value, expected_output in data_set:
            with self.subTest(
                answer_type=answer_type,
                answer_store_value=answer_store_value,
                expected_output=expected_output,
            ):
                # Given
                answer_id = (f"dynamic-{answer_type.lower()}-answer",)
                answer_schema = {
                    "id": answer_id,
                    "label": "Some label",
                    "type": answer_type,
                    **self.dynamic_answer_options_schema(),
                }
                question_schema = self.get_question_schema(answer_schema)

                self.answer_store = AnswerStore(
                    [{"answer_id": answer_id, "value": answer_store_value}]
                )
                self.response_metadata = {
                    "started_at": "2021-01-01T09:00:00.220038+00:00"
                }

                # When
                question = Question(
                    question_schema,
                    answer_store=self.answer_store,
                    schema=self.schema,
                    list_item_id=None,
                    rule_evaluator=self.get_rule_evaluator(),
                )

                # Then
                self.assertEqual(question.answers[0]["value"], expected_output)
