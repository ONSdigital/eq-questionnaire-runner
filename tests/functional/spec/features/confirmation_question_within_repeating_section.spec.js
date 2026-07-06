import DoesAnyoneLiveHerePage from "../../generated_pages/confirmation_question_within_repeating_section/list-collector.page";
import AddPersonPage from "../../generated_pages/confirmation_question_within_repeating_section/list-collector-add.page";
import CarerPage from "../../generated_pages/confirmation_question_within_repeating_section/carer-block.page";
import DateOfBirthPage from "../../generated_pages/confirmation_question_within_repeating_section/dob-block.page";
import ConfirmDateOfBirthPage from "../../generated_pages/confirmation_question_within_repeating_section/confirm-dob-block.page";
import DefaultSectionSummary from "../../generated_pages/confirmation_question_within_repeating_section/default-section-summary.page";
import ConfirmCarerPage from "../../generated_pages/confirmation_question_within_repeating_section/confirm-carer-block.page.js";
import StudentPage from "../../generated_pages/confirmation_question_within_repeating_section/student-block.page.js";
import { click, verifyUrlContains } from "../../helpers";
describe("Feature: Confirmation Question Within A Repeating Section", () => {
  describe("Given I am in a repeating section", () => {
    beforeEach("Add a person", async () => {
      await browser.openQuestionnaire("test_confirmation_question_within_repeating_section.json");
      await $(DoesAnyoneLiveHerePage.yes()).click();
      await click(DoesAnyoneLiveHerePage.submit());
      await $(AddPersonPage.firstName()).setValue("John");
      await $(AddPersonPage.lastName()).setValue("Doe");
      await click(AddPersonPage.submit());
      await $(DoesAnyoneLiveHerePage.no()).click();
      await click(DoesAnyoneLiveHerePage.submit());
      await verifyUrlContains(DateOfBirthPage.url().split("/").slice(-1)[0]);
    });

    describe("Given a confirmation question", () => {
      it("When I answer 'No' to the confirmation question, Then I should be routed back to the source question", async () => {
        // Answer question preceding confirmation question
        await $(DateOfBirthPage.day()).setValue("01");
        await $(DateOfBirthPage.month()).setValue("01");
        await $(DateOfBirthPage.year()).setValue("2015");
        await click(DateOfBirthPage.submit());

        // Answer 'No' to confirmation question
        await $(ConfirmDateOfBirthPage.noINeedToChangeTheirDateOfBirth()).click();
        await click(ConfirmDateOfBirthPage.submit());
        await verifyUrlContains(DateOfBirthPage.pageName);
      });
    });

    describe("Given I have answered a confirmation question", () => {
      it("When I view the summary, Then the confirmation question should not be displayed", async () => {
        await $(DateOfBirthPage.day()).setValue("01");
        await $(DateOfBirthPage.month()).setValue("01");
        await $(DateOfBirthPage.year()).setValue("2015");
        await click(DateOfBirthPage.submit());

        await $(ConfirmDateOfBirthPage.yesPersonNameIsAgeOld()).click();
        await click(ConfirmDateOfBirthPage.submit());

        await verifyUrlContains("sections/default-section/");
        await expect(await $(DefaultSectionSummary.confirmDateOfBirth()).isExisting()).toBe(false);
      });
    });

    describe("Given a confirmation question with a skip condition", () => {
      it("When I submit an a date of birth where the age is at least '16', Then I should be skipped past the confirmation question and directed to the carer question", async () => {
        await $(DateOfBirthPage.day()).setValue("01");
        await $(DateOfBirthPage.month()).setValue("01");
        await $(DateOfBirthPage.year()).setValue("2000");
        await click(DateOfBirthPage.submit());

        await verifyUrlContains(CarerPage.pageName);
        await expect(await $(CarerPage.questionText()).getText()).toContain("Does John Doe look");
      });
    });
    describe("Given a confirmation question", () => {
      it("When I go back to change my answer and return to the confirmation question, then the confirmation answer is cleared and I am routed to the next question", async () => {
        await $(DateOfBirthPage.day()).setValue("01");
        await $(DateOfBirthPage.month()).setValue("01");
        await $(DateOfBirthPage.year()).setValue("1990");
        await click(DateOfBirthPage.submit());
        await $(CarerPage.no()).click();
        await click(CarerPage.submit());
        await $(ConfirmCarerPage.noINeedToChangeTheCarerAnswer()).click();
        await click(ConfirmCarerPage.submit());
        await $(CarerPage.yes()).click();
        await click(CarerPage.submit());
        // Assert that neither confirmation radio is selected
        expect(await $(ConfirmCarerPage.yesTheCarerAnswerIsCorrect()).isSelected()).toBe(false);
        expect(await $(ConfirmCarerPage.noINeedToChangeTheCarerAnswer()).isSelected()).toBe(false);
        // Assert routed to next question
        await $(ConfirmCarerPage.yesTheCarerAnswerIsCorrect()).click();
        await click(ConfirmCarerPage.submit());
        await verifyUrlContains(StudentPage.pageName);
      });
    });
  });
});
