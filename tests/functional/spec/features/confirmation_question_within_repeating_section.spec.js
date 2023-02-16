import DoesAnyoneLiveHerePage from "../../generated_pages/confirmation_question_within_repeating_section/list-collector.page";
import AddPersonPage from "../../generated_pages/confirmation_question_within_repeating_section/list-collector-add.page";
import CarerPage from "../../generated_pages/confirmation_question_within_repeating_section/carer-block.page";
import DateOfBirthPage from "../../generated_pages/confirmation_question_within_repeating_section/dob-block.page";
import ConfirmDateOfBirthPage from "../../generated_pages/confirmation_question_within_repeating_section/confirm-dob-block.page";
import DefaultSectionSummary from "../../generated_pages/confirmation_question_within_repeating_section/default-section-summary.page";

describe("Feature: Confirmation Question Within A Repeating Section", () => {
  describe("Given I am in a repeating section", () => {
    beforeEach("Add a person", async ()=> {
      await browser.openQuestionnaire("test_confirmation_question_within_repeating_section.json");
      await $(DoesAnyoneLiveHerePage.yes()).click();
      await $(DoesAnyoneLiveHerePage.submit()).click();
      await $(AddPersonPage.firstName()).setValue("John");
      await $(AddPersonPage.lastName()).setValue("Doe");
      await $(AddPersonPage.submit()).click();
      await $(DoesAnyoneLiveHerePage.no()).click();
      await $(DoesAnyoneLiveHerePage.submit()).click();
      await expect(browser.getUrl()).to.contain(DateOfBirthPage.url().split("/").slice(-1)[0]);
    });

    describe("Given a confirmation question", () => {
      it("When I answer 'No' to the confirmation question, Then I should be routed back to the source question", async ()=> {
        // Answer question preceding confirmation question
        await $(DateOfBirthPage.day()).setValue("01");
        await $(DateOfBirthPage.month()).setValue("01");
        await $(DateOfBirthPage.year()).setValue("2015");
        await $(DateOfBirthPage.submit()).click();

        // Answer 'No' to confirmation question
        await $(ConfirmDateOfBirthPage.noINeedToChangeTheirDateOfBirth()).click();
        await $(ConfirmDateOfBirthPage.submit()).click();
        await expect(browser.getUrl()).to.contain(DateOfBirthPage.pageName);
      });
    });

    describe("Given I have answered a confirmation question", () => {
      it("When I view the summary, Then the confirmation question should not be displayed", async ()=> {
        await $(DateOfBirthPage.day()).setValue("01");
        await $(DateOfBirthPage.month()).setValue("01");
        await $(DateOfBirthPage.year()).setValue("2015");
        await $(DateOfBirthPage.submit()).click();

        await $(ConfirmDateOfBirthPage.yesPersonNameIsAgeOld()).click();
        await $(ConfirmDateOfBirthPage.submit()).click();

        await expect(browser.getUrl()).to.contain("sections/default-section/");
        await expect(await $(DefaultSectionSummary.confirmDateOfBirth()).isExisting()).to.be.false;
      });
    });

    describe("Given a confirmation question with a skip condition", () => {
      it("When I submit an a date of birth where the age is at least '16', Then I should be skipped past the confirmation question and directed to the carer question", async ()=> {
        await $(DateOfBirthPage.day()).setValue("01");
        await $(DateOfBirthPage.month()).setValue("01");
        await $(DateOfBirthPage.year()).setValue("2000");
        await $(DateOfBirthPage.submit()).click();

        await expect(browser.getUrl()).to.contain(CarerPage.pageName);
        await expect(await $(CarerPage.questionText()).getText()).to.contain("Does John Doe look");
      });
    });
  });
});
