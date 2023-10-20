import BreakfastPage from "../../../generated_pages/submit_with_custom_submission_text/breakfast.page.js";
import { SubmitPage } from "../../../base_pages/submit.page";
import { IntroductionPage } from "../../../base_pages/introduction.page";
import { click } from "../../../helpers";

describe("Given I launch a linear flow questionnaire without summary", () => {
  beforeEach("Load the questionnaire", async () => {
    await browser.openQuestionnaire("test_submit_with_custom_submission_text.json");
    await $(IntroductionPage.getStarted()).click();
  });

  it("When I complete the questionnaire, then I should be taken to the submit page without a summary", async () => {
    await $(BreakfastPage.answer()).setValue("Bacon");
    await click(BreakfastPage.submit());
    await expect(await browser.getUrl()).toContain(SubmitPage.url());
    await expect(await $(SubmitPage.summary()).isExisting()).toBe(false);
  });

  it("When I complete the questionnaire and submit the questionnaire, then the submission is successful", async () => {
    await click(BreakfastPage.submit());
    await expect(await browser.getUrl()).toContain(SubmitPage.url());
    await click(SubmitPage.submit());
  });
});
