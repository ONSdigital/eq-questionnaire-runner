import AddressBlockPage from "../../../generated_pages/view_submitted_response/address.page.js";
import NameBlockPage from "../../../generated_pages/view_submitted_response/name.page.js";
import SubmitPage from "../../../generated_pages/view_submitted_response/submit.page.js";
import ThankYouPage from "../../../base_pages/thank-you.page";
import ViewSubmittedResponsePage from "../../../generated_pages/view_submitted_response/view-submitted-response.page.js";

describe("View Submitted Response", () => {
  beforeEach("Load the questionnaire", async ()=> {
    await browser.openQuestionnaire("test_view_submitted_response.json");
    await $(await NameBlockPage.answer()).setValue("John Smith");
    await $(await NameBlockPage.submit()).click();
    await $(await AddressBlockPage.answer()).setValue("NP10 8XG");
    await $(await AddressBlockPage.submit()).click();
    await $(await SubmitPage.submit()).click();
    await expect(browser.getUrl()).to.contain(ThankYouPage.pageName);
    await expect(await $(await ThankYouPage.title()).getHTML()).to.contain("Thank you for completing the Test");
    await $(await ThankYouPage.savePrintAnswersLink()).click();
    await expect(browser.getUrl()).to.contain(ViewSubmittedResponsePage.pageName);
  });

  it("Given I have completed a questionnaire with view submitted response enabled, When I am on the view submitted response page within 45 minutes of submission, Then the summary is displayed correctly", async ()=> {
    await expect(await $(await ViewSubmittedResponsePage.informationPanel()).isDisplayed()).to.be.false;
    await expect(await $(await ViewSubmittedResponsePage.printButton()).isDisplayed()).to.be.true;
    await expect(await $(await ViewSubmittedResponsePage.heading()).getText()).to.equal("Answers submitted for Apple");
    await expect(await $(await ViewSubmittedResponsePage.metadataTerm(1)).getText()).to.equal("Submitted on:");
    await expect(await $(await ViewSubmittedResponsePage.metadataTerm(2)).getText()).to.equal("Submission reference:");
    await expect(await $(await ViewSubmittedResponsePage.personalDetailsGroupTitle()).getText()).to.equal("Personal Details");
    await expect(await $(await ViewSubmittedResponsePage.nameQuestion()).getText()).to.equal("What is your name?");
    await expect(await $(await ViewSubmittedResponsePage.nameAnswer()).getText()).to.equal("John Smith");
    await expect(await $(await ViewSubmittedResponsePage.addressDetailsGroupTitle()).getText()).to.equal("Address Details");
    await expect(await $(await ViewSubmittedResponsePage.addressQuestion()).getText()).to.equal("What is your address?");
    await expect(await $(await ViewSubmittedResponsePage.addressAnswer()).getText()).to.equal("NP10 8XG");
  });

  describe("Given I am on the view submitted response page and I submitted over 45 minutes ago", () => {
    it("When I click the Download as PDF button, Then I should be redirected to a page informing me that I can no longer view or get a copy of my answers", async ()=> {
      browser.pause(40000); // Waiting 40 seconds for the timeout to expire (45 minute timeout changed to 35 seconds by overriding VIEW_SUBMITTED_RESPONSE_EXPIRATION_IN_SECONDS for the purpose of the functional test)
      await $(await ViewSubmittedResponsePage.downloadButton()).click();
      await expect(await $(await ViewSubmittedResponsePage.informationPanel()).isDisplayed()).to.be.true;
      await expect(await $(await ViewSubmittedResponsePage.informationPanel()).getHTML()).to.contain("For security, you can no longer view or get a copy of your answers");
    });
  });
});
