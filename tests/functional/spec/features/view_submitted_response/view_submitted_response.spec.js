import AddressBlockPage from "../../../generated_pages/view_submitted_response/address.page.js";
import NameBlockPage from "../../../generated_pages/view_submitted_response/name.page.js";
import SubmitPage from "../../../generated_pages/view_submitted_response/submit.page.js";
import ThankYouPage from "../../../base_pages/thank-you.page";
import ViewSubmittedResponsePage from "../../../generated_pages/view_submitted_response/view-submitted-response.page.js";

describe("View Submitted Response", () => {
  beforeEach("Load the questionnaire", async () => {
    await browser.openQuestionnaire("test_view_submitted_response.json");
    await $(NameBlockPage.answer()).setValue("John Smith");
    await $(NameBlockPage.submit()).click();
    await $(AddressBlockPage.answer()).setValue("NP10 8XG");
    await $(AddressBlockPage.submit()).click();
    await $(SubmitPage.submit()).click();
    await expect(browser.getUrl()).to.contain(ThankYouPage.pageName);
    await expect(await $(ThankYouPage.title()).getHTML()).to.contain("Thank you for completing the Test");
    await $(ThankYouPage.savePrintAnswersLink()).click();
    await expect(browser.getUrl()).to.contain(ViewSubmittedResponsePage.pageName);
  });

  it("Given I have completed a questionnaire with view submitted response enabled, When I am on the view submitted response page within 45 minutes of submission, Then the summary is displayed correctly", async () => {
    await expect(await $(ViewSubmittedResponsePage.informationPanel()).isDisplayed()).to.be.false;
    await expect(await $(ViewSubmittedResponsePage.printButton()).isDisplayed()).to.be.true;
    await expect(await $(ViewSubmittedResponsePage.heading()).getText()).to.equal("Answers submitted for Apple");
    await expect(await $(ViewSubmittedResponsePage.metadataTerm(1)).getText()).to.equal("Submitted on:");
    await expect(await $(ViewSubmittedResponsePage.metadataTerm(2)).getText()).to.equal("Submission reference:");
    await expect(await $(ViewSubmittedResponsePage.personalDetailsGroupTitle()).getText()).to.equal("Personal Details");
    await expect(await $(ViewSubmittedResponsePage.nameQuestion()).getText()).to.equal("What is your name?");
    await expect(await $(ViewSubmittedResponsePage.nameAnswer()).getText()).to.equal("John Smith");
    await expect(await $(ViewSubmittedResponsePage.addressDetailsGroupTitle()).getText()).to.equal("Address Details");
    await expect(await $(ViewSubmittedResponsePage.addressQuestion()).getText()).to.equal("What is your address?");
    await expect(await $(ViewSubmittedResponsePage.addressAnswer()).getText()).to.equal("NP10 8XG");
  });

  describe("Given I am on the view submitted response page and I submitted over 45 minutes ago", () => {
    it("When I click the Download as PDF button, Then I should be redirected to a page informing me that I can no longer view or get a copy of my answers", async () => {
      browser.pause(40000); // Waiting 40 seconds for the timeout to expire (45 minute timeout changed to 35 seconds by overriding VIEW_SUBMITTED_RESPONSE_EXPIRATION_IN_SECONDS for the purpose of the functional test)
      await $(ViewSubmittedResponsePage.downloadButton()).click();
      await expect(await $(ViewSubmittedResponsePage.informationPanel()).isDisplayed()).to.be.true;
      await expect(await $(ViewSubmittedResponsePage.informationPanel()).getHTML()).to.contain(
        "For security, you can no longer view or get a copy of your answers"
      );
    });
  });
});
