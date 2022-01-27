import AddressBlockPage from "../../../generated_pages/view_submitted_response/address.page.js";
import NameBlockPage from "../../../generated_pages/view_submitted_response/name.page.js";
import SubmitPage from "../../../generated_pages/view_submitted_response/submit.page.js";
import ThankYouPage from "../../../base_pages/thank-you.page";
import ViewSubmittedResponsePage from "../../../generated_pages/view_submitted_response/view-submitted-response.page.js";

describe("View Submitted Response", () => {
  beforeEach("Load the questionnaire", () => {
    browser.openQuestionnaire("test_view_submitted_response.json");
    $(NameBlockPage.answer()).setValue("John Smith");
    $(NameBlockPage.submit()).click();
    $(AddressBlockPage.answer()).setValue("NP10 8XG");
    $(AddressBlockPage.submit()).click();
    $(SubmitPage.submit()).click();
    expect(browser.getUrl()).to.contain(ThankYouPage.pageName);
    expect($(ThankYouPage.title()).getHTML()).to.contain("Thank you for completing the Test");
    $(ThankYouPage.savePrintAnswersLink()).click();
    expect(browser.getUrl()).to.contain(ViewSubmittedResponsePage.pageName);
  });

  it("Given a questionnaire has view submitted response enabled and has been completed, when on the view response page, then the summary is displayed correctly", () => {
    expect($(ViewSubmittedResponsePage.informationPanel()).isDisplayed()).to.be.false;
    expect($(ViewSubmittedResponsePage.printButton()).isDisplayed()).to.be.true;
    expect($(ViewSubmittedResponsePage.heading()).getText()).to.equal("Answers submitted for Apple");
    expect($(ViewSubmittedResponsePage.metadataTerm(1)).getText()).to.equal("Submitted on:");
    expect($(ViewSubmittedResponsePage.metadataTerm(2)).getText()).to.equal("Submission reference:");
    expect($(ViewSubmittedResponsePage.personalDetailsGroupTitle()).getText()).to.equal("Personal Details");
    expect($(ViewSubmittedResponsePage.nameQuestion()).getText()).to.equal("What is your name?");
    expect($(ViewSubmittedResponsePage.nameAnswer()).getText()).to.equal("John Smith");
    expect($(ViewSubmittedResponsePage.addressDetailsGroupTitle()).getText()).to.equal("Address Details");
    expect($(ViewSubmittedResponsePage.addressQuestion()).getText()).to.equal("What is your address?");
    expect($(ViewSubmittedResponsePage.addressAnswer()).getText()).to.equal("NP10 8XG");
  });

  describe("Given I am on the view submitted response page and I submitted over 45 minutes ago", () => {
    it("When I click the Download as PDF button, Then I should be redirected to a page informing me that I can no longer view or get a copy of my answers", () => {
      browser.pause(45000); // Waiting 45 seconds for the timeout to expire (45 minute timeout changed to 45 seconds by overriding VIEW_SUBMITTED_RESPONSE_EXPIRATION_IN_SECONDS for the purpose of the functional test)
      $(ViewSubmittedResponsePage.downloadButton()).click();
      expect($(ViewSubmittedResponsePage.informationPanel()).isDisplayed()).to.be.true;
      expect($(ViewSubmittedResponsePage.informationPanel()).getHTML()).to.contain("For security, you can no longer view or get a copy of your answers");
    });
  });
});
