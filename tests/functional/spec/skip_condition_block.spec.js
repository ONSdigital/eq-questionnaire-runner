import QuestionPage from "../generated_pages/skip_condition_block/do-you-want-to-skip.page";
import SkipPage from "../generated_pages/skip_condition_block/should-skip.page";
import SubmitPage from "../generated_pages/skip_condition_block/submit.page";

describe("Skip Conditions - Block", () => {
  beforeEach("Load the survey", () => {
    browser.openQuestionnaire("test_new_skip_condition_block.json");
  });

  it("Given I choose to skip on the first page, Then I should see the summary page", () => {
    $(QuestionPage.yes()).click();
    $(QuestionPage.submit()).click();
    expect(browser.getUrl()).to.contain(SubmitPage.pageName);
  });

  it("Given I choose not to skip on the first page, Then I should see the should-skip page", () => {
    $(QuestionPage.no()).click();
    $(QuestionPage.submit()).click();
    expect(browser.getUrl()).to.contain(SkipPage.pageName);
  });
});
