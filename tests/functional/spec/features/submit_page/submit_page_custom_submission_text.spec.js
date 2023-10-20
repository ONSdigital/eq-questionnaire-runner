import DessertBlockPage from "../../../generated_pages/submit_with_summary_custom_submission_text/dessert-block.page.js";
import SubmitPage from "../../../generated_pages/submit_with_summary_custom_submission_text/submit.page.js";
import { click } from "../../../helpers";
describe("Summary Screen", () => {
  beforeEach("Load the questionnaire", async () => {
    await browser.openQuestionnaire("test_submit_with_summary_custom_submission_text.json");
  });

  it("Given a questionnaire with a summary and custom submission content has been completed, then the correct submission content should be displayed", async () => {
    await $(DessertBlockPage.dessert()).setValue("Crème Brûlée");
    await click(DessertBlockPage.submit());
    await expect(await $(SubmitPage.heading()).getText()).toContain("Submission title");
    await expect(await $(SubmitPage.warning()).getText()).toContain("Submission warning");
    await expect(await $(SubmitPage.guidance()).getText()).toContain("Submission guidance");
    await expect(await $(SubmitPage.submit()).getText()).toContain("Submission button");
  });
});
