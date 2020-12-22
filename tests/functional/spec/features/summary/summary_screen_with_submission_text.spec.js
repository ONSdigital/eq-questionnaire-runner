import DessertBlockPage from "../../../generated_pages/summary_with_submission_text/dessert-block.page.js";
import SummaryPage from "../../../generated_pages/summary_with_submission_text/summary.page.js";

describe("Summary Screen", () => {
  beforeEach("Load the survey", () => {
    browser.openQuestionnaire("test_summary_with_submission_text.json");
  });

  it("Given a survey has been completed, when submission content has been set in the schema, then the correct content should be displayed", () => {
    $(DessertBlockPage.dessert()).setValue("Crème Brûlée");
    $(DessertBlockPage.submit()).click();
    expect($(SummaryPage.questionText()).getText()).to.contain("Submission title");
    expect($(SummaryPage.warning()).getText()).to.contain("Submission warning");
    expect($(SummaryPage.guidance()).getText()).to.contain("Submission guidance");
    expect($(SummaryPage.submit()).getText()).to.contain("Submission button");
  });
});
