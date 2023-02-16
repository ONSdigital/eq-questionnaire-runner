import DessertBlockPage from "../../../generated_pages/submit_with_summary_custom_submission_text/dessert-block.page.js";
import SubmitPage from "../../../generated_pages/submit_with_summary_custom_submission_text/submit.page.js";

describe("Summary Screen", () => {
  beforeEach("Load the questionnaire", async ()=> {
    await browser.openQuestionnaire("test_submit_with_summary_custom_submission_text.json");
  });

  it("Given a questionnaire with a summary and custom submission content has been completed, then the correct submission content should be displayed", async ()=> {
    await $(await DessertBlockPage.dessert()).setValue("Crème Brûlée");
    await $(await DessertBlockPage.submit()).click();
    await expect(await $(await SubmitPage.heading()).getText()).to.contain("Submission title");
    await expect(await $(await SubmitPage.warning()).getText()).to.contain("Submission warning");
    await expect(await $(await SubmitPage.guidance()).getText()).to.contain("Submission guidance");
    await expect(await $(await SubmitPage.submit()).getText()).to.contain("Submission button");
  });
});
