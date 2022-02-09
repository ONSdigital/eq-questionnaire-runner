import BreakfastPage from "../generated_pages/submit_with_custom_submission_text/breakfast.page.js";
import IntroductionPage from "../generated_pages/submit_with_custom_submission_text/introduction.page.js";
import { SubmitPage } from "../base_pages/submit.page.js";

describe("Submit with custom submission text", () => {
  beforeEach("Load the questionnaire", () => {
    browser.openQuestionnaire("test_submit_with_custom_submission_text.json");
  });

  it("Given a questionnaire with custom submission content has been started, when it is completed to the submit page, then the correct submission content should be displayed", () => {
    $(IntroductionPage.getStarted()).click();
    $(BreakfastPage.answer()).setValue("Eggs");
    $(BreakfastPage.submit()).click();
    expect($(SubmitPage.heading()).getText()).to.contain("Submit your questionnaire");
    expect($(SubmitPage.warning()).getText()).to.contain("You cannot view your answers after submission");
    expect($(SubmitPage.guidance()).getText()).to.contain("Thank you for your answers, submit this to complete it");
  });
});
