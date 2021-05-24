import BreakfastPage from "../generated_pages/submit_page/breakfast.page.js";
import { SubmitPage } from "../base_pages/submit.page";
import { IntroductionPage } from "../base_pages/introduction.page";

describe("Given I launch a linear flow questionnaire without summary", () => {
  beforeEach("Load the survey", () => {
    browser.openQuestionnaire("test_submit_page.json");
    $(IntroductionPage.getStarted()).click();
  });

  it("When I complete the questionnaire, then I should be taken to the submit page without a summary", () => {
    $(BreakfastPage.answer()).setValue("Bacon");
    $(BreakfastPage.submit()).click();
    expect(browser.getUrl()).to.contain(SubmitPage.url());
    expect($(SubmitPage.summary()).isExisting()).to.be.false;
  });

  it("When I complete the questionnaire and submit the questionnaire, then the submission is successful", () => {
    $(BreakfastPage.submit()).click();
    expect(browser.getUrl()).to.contain(SubmitPage.url());
    $(SubmitPage.submit()).click();
  });
});
