import NameBlockPage from "../../../generated_pages/view_submitted_response/name.page.js";
import SubmitPage from "../../../generated_pages/view_submitted_response/submit.page.js";
import ViewSubmittedResponsePage from "../../../generated_pages/view_submitted_response/view-submitted-response.page.js";

describe("View Submitted Response", () => {
  beforeEach("Load the survey", () => {
    browser.openQuestionnaire("test_view_submitted_response.json");
  });

  it("Given a questionnaire has view submitted response enabled and has been completed when on the view response page then the summary is displayed correctly", () => {
    $(NameBlockPage.answer()).setValue("John Smith");
    $(NameBlockPage.submit()).click();
    $(SubmitPage.submit()).click();
    browser.url("/submitted/view-response");

    expect($(ViewSubmittedResponsePage.heading()).getText()).to.equal("Your answers were submitted for Apple");
    expect($(ViewSubmittedResponsePage.nameGroupTitle()).getText()).to.equal("Name");
    expect($(ViewSubmittedResponsePage.nameQuestion()).getText()).to.equal("What is your name?");
    expect($(ViewSubmittedResponsePage.nameAnswer()).getText()).to.equal("John Smith");
  });
});
