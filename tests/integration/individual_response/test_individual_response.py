from tests.integration.integration_test_case import IntegrationTestCase


class IndividualResponseTestCase(IntegrationTestCase):
    def setUp(self):
        super().setUp()
        self.launchSurvey("test_individual_response")

    @property
    def individual_section_link(self):
        return self.getHtmlSoup().find(
            "a", {"data-qa": "hub-row-individual-section-1-link"}
        )["href"]

    @property
    def individual_response_link(self):
        return (
            self.getHtmlSoup()
            .find("p", {"data-qa": "individual-response-url"})
            .find_next()["href"]
        )

    def _add_no_household_members(self):
        self.get("questionnaire/primary-person-list-collector/")
        self.post({"you-live-here": "No"})
        self.post({"anyone-else": "No"})
        self.get("questionnaire/")

    def _add_primary(self):
        self.get("questionnaire/primary-person-list-collector/")
        self.post({"you-live-here": "Yes"})
        self.post({"first-name": "Marie", "last-name": "Day"})
        self.post({"anyone-else": "No"})
        self.get("questionnaire/")

    def _add_primary_and_household(self):
        self.get("questionnaire/primary-person-list-collector/")
        self.post({"you-live-here": "Yes"})
        self.post({"first-name": "Marie", "last-name": "Day"})
        self.post({"anyone-else": "Yes"})
        self.post({"first-name": "John", "last-name": "Doe"})
        self.post({"anyone-else": "No"})
        self.get("questionnaire/")

    def _add_household_no_primary(self):
        self.get("questionnaire/primary-person-list-collector/")
        self.post({"you-live-here": "No"})
        self.post({"anyone-else": "Yes"})
        self.post({"first-name": "Marie", "last-name": "Day"})
        self.post({"anyone-else": "No"})
        self.get("questionnaire/")

    def _request_individual_response(self):
        self._add_household_no_primary()
        self.post()
        self.get(self.individual_response_link)
        self.post()
        self.post({"individual-response-how-answer": "Post"})
        self.post(
            {
                "individual-response-post-confirm-answer": "Yes, send the access code by post"
            }
        )
        self.post()


class TestIndividualResponseErrorStatus(IndividualResponseTestCase):
    def test_ir_raises_401_without_session(self):
        # Given the hub is enabled
        # And I add a household member
        self._add_household_no_primary()
        self.post()

        # When I sign out and navigate to the individual response page
        individual_response_link = self.individual_response_link
        self.get(individual_response_link)
        self.post()
        self.sign_out()
        self.get(individual_response_link)

        # Then I should see the 401 page
        self.assertStatusCode(401)

    def test_401_after_signout(self):
        # Given the hub is enabled
        # And I add a household member
        self._add_household_no_primary()

        # When I sign out and navigate to the individual response page
        self.sign_out()
        self.get("/individual-response")

        # Then I should see the 401 page
        self.assertStatusCode(401)

    def test_404_invalid_list_item_id(self):
        # Given I add a household member
        self._add_household_no_primary()

        # When I use an invalid id in an individual response url
        self.get("/individual-response/not-an-id/how")

        # Then I should see the 404 page
        self.assertStatusCode(404)

    def test_404_when_hub_not_accessible(self):
        # Given I try to navigate to the individual response page
        self.get("/individual-response")

        # Then I should see the 404 page
        self.assertStatusCode(404)

    def test_404_how_when_hub_not_accessible(self):
        # Given I try to navigate to the individual response how page
        self.get("/individual-response/fake-id/how")

        # Then I should see the 404 page
        self.assertStatusCode(404)

    def test_404_confirm__when_hub_not_accessible(self):
        # Given I try to navigate to the individual response how page
        self.get("/individual-response/fake-id/post/confirm-address")

        # Then I should see the 404 page
        self.assertStatusCode(404)

    def test_404_post_confirmation_when_hub_not_accessible(self):
        # Given I try to navigate to the individual response how page
        self.get("/individual-response/post/confirmation")

        # Then I should see the 404 page
        self.assertStatusCode(404)

    def test_404_individual_response_page_if_primary_id_used(self):
        # Given I add a primary person
        self._add_primary()

        # When I navigate to the how endpoint using the primary person's
        # list item id
        self.post()

        primary_person_id = self.last_url.split("/")[3]
        self.get(f"individual-response?list_item_id={primary_person_id}")

        # Then I should see the 404 page
        self.assertStatusCode(404)

    def test_404_individual_response_how_page_if_primary_id_used(self):
        # Given I add a primary person
        self._add_primary()

        # When I navigate to the how endpoint using the primary person's
        # list item id
        self.post()
        primary_person_id = self.last_url.split("/")[3]
        self.get(f"individual-response/{primary_person_id}/how")

        # Then I should see the 404 page
        self.assertStatusCode(404)

    def test_404_individual_response_confirm_page_if_primary_id_used(self):
        # Given I add a primary person
        self._add_primary()

        # When I navigate to the how endpoint using the primary person's
        # list item id
        self.post()
        primary_person_id = self.last_url.split("/")[3]
        self.get(f"individual-response/{primary_person_id}/post/confirm-address")

        # Then I should see the 404 page
        self.assertStatusCode(404)

    def test_404_individual_response_no_list_items(self):
        # Given I add no household members
        self._add_no_household_members()

        # When I navigate to the how endpoint using a fake id
        self.get("/individual-response/no-id/how")

        # Then I should see the 404 page
        self.assertStatusCode(404)


class TestIndividualResponseIndividualSection(IndividualResponseTestCase):
    def test_ir_guidance_not_displayed_when_primary(self):
        # Given I add a primary person
        self._add_primary()

        # When I navigate to the individual section
        self.post()

        # Then I should not see the individual response guidance
        self.assertInUrl("questionnaire/household/")
        self.assertInBody("You will need to know personal details")
        self.assertNotInBody("If you can't answer someone else's questions")

    def test_ir_guidance_displayed_when_no_primary_person(self):
        # Given I don't add a primary person
        self._add_household_no_primary()

        # When I navigate to the individual section
        self.post()

        # Then I should see the individual response guidance
        self.assertInBody("You will need to know personal details")
        self.assertInBody("If you can’t answer questions for this person")
        self.assertInBody("Hide")

    def test_ir_guidance_not_displayed_on_primary_page_when_primary_and_other_household_members(
        self,
    ):
        # Given I add a primary person and a household member
        self._add_primary_and_household()

        # When I navigate to the first individual section
        self.post()
        self.post()

        # Then I should not see the individual response guidance
        self.assertInBody("Are you")
        self.assertNotInBody("If you can’t answer someone else’s questions")

    def test_ir_guidance_displayed_on_non_primary_page_when_primary_and_other_household_members(
        self,
    ):
        # Given I add a primary person and a household member
        self._add_primary_and_household()

        # When I navigate to the first non-primary individual section
        self.post()
        self.post()
        self.post({"proxy-answer": "Yes, I am"})
        self.post()

        # Then I should see the individual response guidance
        self.assertInBody("You will need to know personal details such as")
        self.assertInBody("If you can’t answer questions for this person")


class TestIndividualResponseHubViews(IndividualResponseTestCase):
    def test_individual_response_requested(self):
        # Given I request an individual response by post
        self._request_individual_response()

        # When I navigate to the hub
        self.get("/questionnaire")

        # Then I should see "Separate census requested" as
        # the individual section status
        self.assertInBody("Separate census requested")
        self.assertInBody("Change or resend")
        self.assertIn("/change", self.individual_section_link)

    def test_individual_response_not_requested_status_unchanged(self):
        # Given I naviagate to the confirm page of individual response
        # but don't request one
        self._add_household_no_primary()
        self.post()
        self.get(self.individual_response_link)
        self.post()
        self.post({"individual-response-how-answer": "Post"})

        # When I navigate to the hub
        self.get("/questionnaire")

        # Then I should see "Not started" as the individual section status
        self.assertInBody("Not started")


class TestIndividualResponseNavigation(IndividualResponseTestCase):
    def test_introduction_page_previous_goes_to_individual_section(self):
        # Given I navigate to the individual response introduction page from an
        # individual section
        self._add_household_no_primary()
        self.get(self.individual_section_link)
        self.get(self.individual_response_link)

        # When I click the previous link
        self.previous()

        # Then I should be taken back to the individual section
        self.assertInUrl("individual-interstitial")

    def test_how_page_previous_goes_to_introduction_page(self):
        # Given I navigate to the individual response how page from an
        # individual response introduction page
        self._add_household_no_primary()
        self.get(self.individual_section_link)
        self.get(self.individual_response_link)
        self.post()

        # When I click the previous link
        self.previous()

        # Then I should be taken back to the individual response introduction page
        self.assertInBody("If you can't answer questions for others in your household")

    def test_introduction_previous_goes_to_hub(self):
        # Given I add a household member
        # and navigate to the individual response introduction page
        # without a list item id url param
        self._add_household_no_primary()
        self.get("/individual-response/")

        # When I click the previous link
        self.previous()

        # Then I should be taken to the hub
        self.assertInUrl("questionnaire/")


class TestIndividualResponseConfirmationPage(IndividualResponseTestCase):
    def test_display_address_on_confirmation_page(self):
        # Given I navigate to the confirmation page
        self._add_household_no_primary()
        self.get(self.individual_section_link)
        self.get(self.individual_response_link)
        self.post()
        self.post({"individual-response-how-answer": "Post"})

        # When I post "Yes, send the access code by post"
        self.post(
            {
                "individual-response-post-confirm-answer": "Yes, send the access code by post"
            }
        )

        # Then I should see the address
        self.assertInUrl("/confirmation")
        self.assertInBody("68 Abingdon Road, Goathill")

    def test_navigate_back_to_how_page_from_post_page(self):
        # Given I navigate to the individual response confirm post page
        self._add_household_no_primary()
        self.get(self.individual_section_link)
        self.get(self.individual_response_link)
        self.post()
        self.post({"individual-response-how-answer": "Post"})

        # When I click the previous link
        self.previous()

        # Then I should be taken back to the how page
        self.assertInUrl("/how")

    def test_redirect_to_how_page_when_no_send_another_way_selected(self):
        # Given I navigate to the /individual-response/<id>/how url
        # after adding a household member
        self._add_household_no_primary()
        self.get(self.individual_section_link)
        self.get(self.individual_response_link)
        self.post()
        self.post({"individual-response-how-answer": "Post"})

        # When I choose to send the individual response code another way
        self.post(
            {"individual-response-post-confirm-answer": "No, send it another way"}
        )

        # Then I should be redirected to the how page
        self.assertInUrl("/how")

    def test_mandatory_error_rendered_on_confirm_address(self):
        # Given I navigate to the /individual-response/<id>/confirm-address url
        # after adding a household member
        self._add_household_no_primary()
        self.get(self.individual_section_link)
        self.get(self.individual_response_link)
        self.post()
        self.post({"individual-response-how-answer": "Post"})

        # When I post with no data
        self.post()

        # Then I should see errors rendered correctly
        self.assertInUrl("/confirm-address")
        self.assertInBody("There is a problem with your answer")

    def test_default_post_routing(self):
        # Given I navigate to the individual response how page
        # after adding a household member
        self._add_household_no_primary()
        self.get(self.individual_section_link)
        self.get(self.individual_response_link)
        self.post()

        # When I post without selecting a radio button
        self.post()

        # Then I should see the post confirm address page
        self.assertInUrl("post/confirm-address")


class TestIndividualResponseChange(IndividualResponseTestCase):
    def test_hub_change_link_goes_to_change_page(self):
        # Given I request an individual response by post
        self._request_individual_response()

        # When I navigate to the hub and click on the change individual response link
        self.get("/questionnaire")
        self.get(self.individual_section_link)

        # Then I should see the change individual response page
        self.assertInBody("How would you like to answer")

    def test_change_page_previous_goes_to_hub(self):
        # Given I navigate to the individual response change page
        self._request_individual_response()
        self.get("/questionnaire")
        self.get(self.individual_section_link)

        # When I click the previous link
        self.previous()

        # Then I should be taken to the hub
        self.assertInUrl("questionnaire/")

    def test_request_separate_census_option_is_preselected(self):
        # Given I request an individual response
        self._request_individual_response()

        # When I navigate to the individual response change page
        self.get("/questionnaire")
        self.get(self.individual_section_link)

        # Then the "I would like to request a separate census" option is preselected
        checked_radio_input = self.getHtmlSoup().select(
            "#individual-response-change-answer-0[checked]"
        )
        self.assertIsNotNone(checked_radio_input)

    def test_request_separate_census_option_goes_to_how_page(self):
        # Given I navigate to the individual response change page
        self._request_individual_response()
        self.get("/questionnaire")
        self.get(self.individual_section_link)

        # When I choose the "I would like to request a separate census" option
        self.post(
            {
                "individual-response-change-answer": "I would like to request a separate census for them to complete"
            }
        )

        # Then I should be taken to the how page
        self.assertInUrl("/how")

        # And the section status should not be updated
        self.get("/questionnaire")
        self.assertInBody("Change or resend")

    def test_answer_own_questions_option_goes_to_hub(self):
        # Given I navigate to the individual response change page
        self._request_individual_response()
        self.get("/questionnaire")
        self.get(self.individual_section_link)

        # When I choose the "I will ask them to answer" option
        self.post(
            {
                "individual-response-change-answer": "I will ask them to answer their own questions"
            }
        )

        # Then I should be taken to the hub
        self.assertInUrl("/questionnaire")

    def test_answer_own_questions_option_updates_section_status(self):
        # Given I navigate to the individual response change page
        self._request_individual_response()
        self.get("/questionnaire")
        self.get(self.individual_section_link)

        # When I choose the "I will ask them to answer" option
        self.post(
            {
                "individual-response-change-answer": "I will ask them to answer their own questions"
            }
        )

        # Then the section status should be updated
        self.assertNotInBody("Change or resend")
        self.assertInBody("Not started")
        self.assertInBody("Start section")

    def test_answer_own_questions_option_after_starting_section_updates_section_status(
        self
    ):
        # Given start a section and then request an individual response
        self._add_household_no_primary()
        self.post()
        self.post()
        self.previous()
        self.get(self.individual_response_link)
        self.post()
        self.post({"individual-response-how-answer": "Post"})
        self.post(
            {
                "individual-response-post-confirm-answer": "Yes, send the access code by post"
            }
        )
        self.post()

        # When I navigate to the individual response change page and choose the "I will ask them to answer" option
        self.get("/questionnaire")
        self.get(self.individual_section_link)
        self.post(
            {
                "individual-response-change-answer": "I will ask them to answer their own questions"
            }
        )

        # Then the section status should be updated
        self.assertNotInBody("Change or resend")
        self.assertInBody("Partially completed")
        self.assertInBody("Continue with section")

    def test_i_will_answer_option_goes_to_individual_section(self):
        # Given I navigate to the individual response change page
        self._request_individual_response()
        self.get("/questionnaire")
        self.get(self.individual_section_link)

        # When I choose the "I will answer" option
        self.post(
            {"individual-response-change-answer": "I will answer for {person_name}"}
        )

        # Then I should be taken to the individual section introduction page
        self.assertInBody("You will need to know personal details such as")

        # And the section status should be updated
        self.assertInUrl("/questionnaire")
        self.assertNotInBody("Change or resend")

    def test_how_page_previous_goes_to_change_page(self):
        # Given I navigate to the individual response how page
        self._request_individual_response()
        self.get("/questionnaire")
        self.get(self.individual_section_link)
        self.post(
            {
                "individual-response-change-answer": "I would like to request a separate census for them to complete"
            }
        )

        # When I click the previous link
        self.previous()

        # Then I should be taken to the change page
        self.assertInUrl("/change")

    def test_post_confirm_previous_previous_goes_to_change_page(self):
        # Given I navigate to the individual response post confirm page
        self._request_individual_response()
        self.get("/questionnaire")
        self.get(self.individual_section_link)
        self.post(
            {
                "individual-response-change-answer": "I would like to request a separate census for them to complete"
            }
        )
        self.post({"individual-response-how-answer": "Post"})

        # When I click the previous link twice
        self.previous()
        self.previous()

        # Then I should be taken to the change page
        self.assertInUrl("/change")
