import BaseSummaryPage from "../base_pages/summary.page.js";
import BreakfastPage from "../generated_pages/final_confirmation/breakfast.page.js";
import ConfirmationPage from "../base_pages/confirmation.page";
import IntroductionPage from "../base_pages/introduction.page";
const introductionPage = new IntroductionPage("introduction");

describe("Confirmation Page", () => {
  beforeEach("Load the survey", () => {
    browser.openQuestionnaire("test_final_confirmation.json");
    $(introductionPage.getStarted()).click();
  });

  it("Given I successfully complete a questionnaire, when I submit the page, then I should be prompted for confirmation to submit.", () => {
    $(BreakfastPage.answer()).setValue("Bacon");
    $(BreakfastPage.submit()).click();
    expect(browser.getUrl()).to.contain(ConfirmationPage.url());
    expect($(BaseSummaryPage.summary()).isExisting()).to.be.false;
  });

  it("Given I successfully complete a questionnaire, when I confirm submit, then the submission is successful", () => {
    $(BreakfastPage.submit()).click();
    expect(browser.getUrl()).to.contain(ConfirmationPage.url());
    $(ConfirmationPage.submit()).click();
  });
});
