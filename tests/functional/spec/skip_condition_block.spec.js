import QuestionPage from "../generated_pages/skip_condition_block/do-you-want-to-skip.page";
import SkipPage from "../generated_pages/skip_condition_block/should-skip.page";
import SubmitPage from "../generated_pages/skip_condition_block/submit.page";

describe("Skip Conditions - Block", () => {
  const schema = "test_skip_condition_block.json";

  describe("Given I am completing the test skip condition block survey,", () => {
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
