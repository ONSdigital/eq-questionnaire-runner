import AddressBlockPage from "../../../generated_pages/view_submitted_response/address.page.js";
import NameBlockPage from "../../../generated_pages/view_submitted_response/name.page.js";
import SubmitPage from "../../../generated_pages/view_submitted_response/submit.page.js";
import ViewSubmittedResponsePage from "../../../generated_pages/view_submitted_response/view-submitted-response.page.js";

describe("View Submitted Response", () => {
  beforeEach("Load the questionnaire", () => {
    browser.openQuestionnaire("test_view_submitted_response.json");
  });

  it("Given a questionnaire has view submitted response enabled and has been completed, when on the view response page, then the summary is displayed correctly", () => {
    $(NameBlockPage.answer()).setValue("John Smith");
    $(NameBlockPage.submit()).click();
    $(AddressBlockPage.answer()).setValue("NP10 8XG");
    $(AddressBlockPage.submit()).click();
    $(SubmitPage.submit()).click();
    browser.url("/submitted/view-response");
    expect($(ViewSubmittedResponsePage.printButton()).getText()).to.equal("Print answers");
    expect($(ViewSubmittedResponsePage.heading()).getText()).to.equal("Answers submitted for Apple.");
    expect($(ViewSubmittedResponsePage.metadataTerm(1)).getText()).to.equal("Submitted on:");
    expect($(ViewSubmittedResponsePage.metadataTerm(2)).getText()).to.equal("Submission reference:");
    expect($(ViewSubmittedResponsePage.personalDetailsGroupTitle()).getText()).to.equal("Personal Details");
    expect($(ViewSubmittedResponsePage.nameQuestion()).getText()).to.equal("What is your name?");
    expect($(ViewSubmittedResponsePage.nameAnswer()).getText()).to.equal("John Smith");
    expect($(ViewSubmittedResponsePage.addressDetailsGroupTitle()).getText()).to.equal("Address Details");
    expect($(ViewSubmittedResponsePage.addressQuestion()).getText()).to.equal("What is your address?");
    expect($(ViewSubmittedResponsePage.addressAnswer()).getText()).to.equal("NP10 8XG");
  });
});
