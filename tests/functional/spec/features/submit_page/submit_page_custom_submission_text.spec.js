import DessertBlockPage from "../../../generated_pages/submit_with_summary_custom_submission_text/dessert-block.page.js";
import SubmitPage from "../../../generated_pages/submit_with_summary_custom_submission_text/submit.page.js";

describe("Summary Screen", () => {
  beforeEach("Load the questionnaire", () => {
    browser.openQuestionnaire("test_submit_with_summary_custom_submission_text.json");
  });

  it("Given a questionnaire with summary has been completed, when submission content has been set in the schema, then the correct content should be displayed", () => {
    $(DessertBlockPage.dessert()).setValue("Crème Brûlée");
    $(DessertBlockPage.submit()).click();
    expect($(SubmitPage.heading()).getText()).to.contain("Submission title");
    expect($(SubmitPage.warning()).getText()).to.contain("Submission warning");
    expect($(SubmitPage.guidance()).getText()).to.contain("Submission guidance");
    expect($(SubmitPage.submit()).getText()).to.contain("Submission button");
  });
});
