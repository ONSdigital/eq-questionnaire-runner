import DessertBlockPage from "../../../generated_pages/summary_with_submission_text/dessert-block.page.js";
import SubmitPage from "../../../generated_pages/summary_with_submission_text/submit.page.js";

describe("Summary Screen", () => {
  beforeEach("Load the survey", () => {
    browser.openQuestionnaire("test_summary_with_submission_text.json");
  });

  it("Given a survey with summary has been completed, when submission content has been set in the schema, then the correct content should be displayed", () => {
    $(DessertBlockPage.dessert()).setValue("Crème Brûlée");
    $(DessertBlockPage.submit()).click();
    expect($(SubmitPage.heading()).getText()).to.contain("Submission title");
    expect($(SubmitPage.warning()).getText()).to.contain("Submission warning");
    expect($(SubmitPage.guidance()).getText()).to.contain("Submission guidance");
    expect($(SubmitPage.submit()).getText()).to.contain("Submission button");
  });
});
