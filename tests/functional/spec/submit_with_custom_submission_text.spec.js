import BreakfastPage from "../generated_pages/submit_with_custom_submission_text/breakfast.page.js";
import IntroductionPage from "../generated_pages/submit_with_custom_submission_text/introduction.page.js";
import { SubmitPage } from "../base_pages/submit.page.js";
import { click } from "../helpers";
describe("Submit with custom submission text", () => {
  beforeEach("Load the questionnaire", async () => {
    await browser.openQuestionnaire("test_submit_with_custom_submission_text.json");
  });

  it("Given a questionnaire with custom submission content has been started, when it is completed to the submit page, then the correct submission content should be displayed", async () => {
    await $(IntroductionPage.getStarted()).click();
    await $(BreakfastPage.answer()).setValue("Eggs");
    await click(BreakfastPage.submit());
    await expect(await $(SubmitPage.heading()).getText()).toContain("Submit your questionnaire");
    await expect(await $(SubmitPage.warning()).getText()).toContain("You cannot view your answers after submission");
    await expect(await $(SubmitPage.guidance()).getText()).toContain("Thank you for your answers, submit this to complete it");
  });
});
