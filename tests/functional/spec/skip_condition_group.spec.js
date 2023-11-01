import QuestionPage from "../generated_pages/skip_condition_group/do-you-want-to-skip.page";
import SkipPage from "../generated_pages/skip_condition_group/should-skip.page";
import SubmitPage from "../generated_pages/skip_condition_group/submit.page";
import { click } from "../helpers";
describe("Skip Conditions - Group", () => {
  const schema = "test_skip_condition_group.json";

  describe("Given I am completing the test skip condition group survey,", () => {
    beforeEach("load the survey", async () => {
      await browser.openQuestionnaire(schema);
    });

    it("When I choose to skip on the first page, Then I should see the summary page", async () => {
      await $(QuestionPage.yes()).click();
      await click(QuestionPage.submit());
      await expect(browser).toHaveUrlContaining(SubmitPage.pageName);
    });

    it("When I choose not to skip on the first page, Then I should see the should-skip page", async () => {
      await $(QuestionPage.no()).click();
      await click(QuestionPage.submit());
      await expect(browser).toHaveUrlContaining(SkipPage.pageName);
    });
  });
});
