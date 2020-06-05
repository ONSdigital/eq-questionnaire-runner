import DoesAnyoneLiveHerePage from "../../generated_pages/confirmation_question_within_repeating_section/list-collector.page";
import AddPersonPage from "../../generated_pages/confirmation_question_within_repeating_section/list-collector-add.page";
import CarerPage from "../../generated_pages/confirmation_question_within_repeating_section/carer-block.page";
import DateOfBirthPage from "../../generated_pages/confirmation_question_within_repeating_section/dob-block.page";
import ConfirmDateOfBirthPage from "../../generated_pages/confirmation_question_within_repeating_section/confirm-dob-block.page";
import DefaultSectionSummary from "../../generated_pages/confirmation_question_within_repeating_section/default-section-summary.page";

describe("Feature: Confirmation Question Within A Repeating Section", () => {
  describe("Given I am in a repeating section", () => {
    beforeEach("Add a person", () => {
      browser.openQuestionnaire("test_confirmation_question_within_repeating_section.json");
      $(DoesAnyoneLiveHerePage.yes()).click();
      $(DoesAnyoneLiveHerePage.submit()).click();
      $(AddPersonPage.firstName()).setValue("John");
      $(AddPersonPage.lastName()).setValue("Doe");
      $(AddPersonPage.submit()).click();
      $(DoesAnyoneLiveHerePage.no()).click();
      $(DoesAnyoneLiveHerePage.submit()).click();
      expect(browser.getUrl()).to.contain(DateOfBirthPage.url().split("/").slice(-1)[0]);
    });

    describe("Given a confirmation question", () => {
      it("When I answer 'No' to the confirmation question, Then I should be routed back to the source question", () => {
        // Answer question preceding confirmation question
        $(DateOfBirthPage.day()).setValue("01");
        $(DateOfBirthPage.month()).setValue("01");
        $(DateOfBirthPage.year()).setValue("2007");
        $(DateOfBirthPage.submit()).click();

        // Answer 'No' to confirmation question
        $(ConfirmDateOfBirthPage.noINeedToChangeTheirDateOfBirth()).click();
        $(ConfirmDateOfBirthPage.submit()).click();
        expect(browser.getUrl()).to.contain(DateOfBirthPage.pageName);
      });
    });

    describe("Given I have answered a confirmation question", () => {
      it("When I view the summary, Then the confirmation question should not be displayed", () => {
        $(DateOfBirthPage.day()).setValue("01");
        $(DateOfBirthPage.month()).setValue("01");
        $(DateOfBirthPage.year()).setValue("2007");
        $(DateOfBirthPage.submit()).click();

        $(ConfirmDateOfBirthPage.yesPersonNameIsAgeOld()).click();
        $(ConfirmDateOfBirthPage.submit()).click();

        expect(browser.getUrl()).to.contain("sections/default-section/");
        expect($(DefaultSectionSummary.confirmDateOfBirth()).isExisting()).to.be.false;
      });
    });

    describe("Given a confirmation question with a skip condition", () => {
      it("When I submit an a date of birth where the age is at least '16', Then I should be skipped past the confirmation question and directed to the carer question", () => {
        $(DateOfBirthPage.day()).setValue("01");
        $(DateOfBirthPage.month()).setValue("01");
        $(DateOfBirthPage.year()).setValue("2000");
        $(DateOfBirthPage.submit()).click();

        expect(browser.getUrl()).to.contain(CarerPage.pageName);
        expect($(CarerPage.questionText()).getText()).to.contain("Does John Doe look");
      });
    });
  });
});
