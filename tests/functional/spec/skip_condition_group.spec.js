import QuestionPage from "../generated_pages/skip_condition_group/do-you-want-to-skip.page";
import SkipPage from "../generated_pages/skip_condition_group/should-skip.page";
import SubmitPage from "../generated_pages/skip_condition_group/submit.page";

describe("Skip Conditions - Group", () => {
  const schema = "test_new_skip_condition_group.json";

  describe("Given I am completing the test skip condition group survey,", () => {
    beforeEach("load the survey", () => {
      browser.openQuestionnaire(schema);
    });

    it("When I choose to skip on the first page, Then I should see the summary page", () => {
      $(QuestionPage.yes()).click();
      $(QuestionPage.submit()).click();
      expect(browser.getUrl()).to.contain(SubmitPage.pageName);
    });

    it("When I choose not to skip on the first page, Then I should see the should-skip page", () => {
      $(QuestionPage.no()).click();
      $(QuestionPage.submit()).click();
      expect(browser.getUrl()).to.contain(SkipPage.pageName);
    });
  });
});
