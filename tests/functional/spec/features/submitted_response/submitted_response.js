import NameBlockPage from "../../../generated_pages/view_submitted_response/name.page.js";
import SubmitPage from "../../../generated_pages/view_submitted_response/submit.page.js";
import SummaryResponsePage from "../../../base_pages/submitted-response.page.js";

describe("Submitted Response", () => {
  beforeEach("Load the survey", () => {
    browser.openQuestionnaire("test_view_submitted_response.json");
  });

  it("Given a questionnaire has view submitted response enabled and has been completed when on the view response page then the summary is displayed correctly", () => {
    $(NameBlockPage.answer()).setValue("John Smith");
    $(NameBlockPage.submit()).click();
    $(SubmitPage.submit()).click();
    browser.url("/submitted/view-response");

    expect(browser.getUrl()).to.contain(SummaryResponsePage.url());
    expect($(SummaryResponsePage.heading()).getText()).to.equal("Your answers were submitted for Apple");
    expect($(SummaryResponsePage.summary()).isExisting()).to.be.true;
    expect($(SummaryResponsePage.summaryRowState("name-question")).getText()).to.equal("What is your name?");
    expect($(SummaryResponsePage.summaryRowState("name-answer")).getText()).to.equal("John Smith");
  });
});
