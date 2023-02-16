import SubmitPage from "../generated_pages/confirmation_email/submit.page";

import ThankYouPage from "../base_pages/thank-you.page";
import ConfirmationEmailPage from "../base_pages/confirmation-email.page";
import ConfirmationEmailSentPage from "../base_pages/confirmation-email-sent.page";
import ConfirmEmailPage from "../base_pages/confirm-email.page";

describe("Email confirmation", () => {
  describe("Given I launch the test email confirmation survey", () => {
    before(async ()=> {
      await browser.openQuestionnaire("test_confirmation_email.json");
    });

    it("When I complete the survey and am on the thank you page, Then there is option to enter an email address", async ()=> {
      await $(await SubmitPage.submit()).click();
      await $(await SubmitPage.submit()).click();
      await expect(browser.getUrl()).to.contain(ThankYouPage.pageName);
      await expect(await $(await ThankYouPage.email()).isExisting()).to.be.true;
    });

    it("When I submit the form without providing an email address, Then I get an error message", async ()=> {
      await $(await ThankYouPage.submit()).click();
      await expect(browser.getUrl()).to.contain(ThankYouPage.pageName);
      await expect(await $(await ThankYouPage.errorPanel()).isExisting()).to.be.true;
      await expect(await $(await ThankYouPage.errorPanel()).getText()).to.contain("Enter an email address");
    });

    it("When I submit the form without providing a correctly formatted email address, Then I get an error message", async ()=> {
      await $(await ThankYouPage.email()).setValue("incorrect-format");
      await $(await ThankYouPage.submit()).click();
      await expect(browser.getUrl()).to.contain(ThankYouPage.pageName);
      await expect(await $(await ThankYouPage.errorPanel()).isExisting()).to.be.true;
      await expect(await $(await ThankYouPage.errorPanel()).getText()).to.contain("Enter an email address in a valid format, for example name@example.com");
    });

    it("When I submit the form with a valid email address, Then I go to the confirm email page", async ()=> {
      await $(await ThankYouPage.email()).setValue("name@example.com");
      await $(await ThankYouPage.submit()).click();
      await expect(browser.getUrl()).to.contain("confirmation-email/confirm");
      await expect(await $(await ConfirmEmailPage.questionTitle()).getText()).to.equal("Is this email address correct?");
    });

    it("When I submit the confirm email page without providing an answer, Then I get an error message", async ()=> {
      await $(await ConfirmEmailPage.submit()).click();
      await expect(browser.getUrl()).to.contain("confirmation-email/confirm");
      await expect(await $(await ConfirmEmailPage.errorPanel()).isExisting()).to.be.true;
      await expect(await $(await ConfirmEmailPage.errorPanel()).getText()).to.contain("Select an answer");
    });

    it("When I answer 'Yes' and submit the confirm email page, Then I go to email sent page", async ()=> {
      await $(await ConfirmEmailPage.yes()).click();
      await $(await ConfirmEmailPage.submit()).click();
      await expect(browser.getUrl()).to.contain("confirmation-email/sent");
      await expect(await $(await ConfirmationEmailSentPage.confirmationText()).getText()).to.equal("A confirmation email has been sent to name@example.com");
    });

    it("When I go to the confirmation email page and submit without providing an email address, Then I get an error message", async ()=> {
      await $(await ConfirmationEmailSentPage.sendAnotherEmail()).click();
      await $(await ConfirmationEmailPage.submit()).click();
      await expect(browser.getUrl()).to.contain("confirmation-email/send");
      await expect(await $(await ConfirmationEmailPage.errorPanel()).isExisting()).to.be.true;
      await expect(await $(await ConfirmationEmailPage.errorPanel()).getText()).to.equal("Enter an email address");
    });

    it("When I submit the form without providing a correctly formatted email address, Then I get an error message", async ()=> {
      await $(await ConfirmationEmailPage.email()).setValue("incorrect-format");
      await $(await ConfirmationEmailPage.submit()).click();
      await expect(browser.getUrl()).to.contain("confirmation-email/send");
      await expect(await $(await ConfirmationEmailPage.errorPanel()).isExisting()).to.be.true;
      await expect(await $(await ConfirmationEmailPage.errorPanel()).getText()).to.equal("Enter an email address in a valid format, for example name@example.com");
    });

    it("When I submit the form with a valid email and confirm it is correct, Then I go to the email confirmation page", async ()=> {
      await $(await ConfirmationEmailPage.email()).setValue("name@example.com");
      await $(await ConfirmationEmailPage.submit()).click();
      await $(await ConfirmEmailPage.yes()).click();
      await $(await ConfirmEmailPage.submit()).click();
      await expect(browser.getUrl()).to.contain("confirmation-email/sent");
      await expect(await $(await ConfirmationEmailSentPage.confirmationText()).getText()).to.equal("A confirmation email has been sent to name@example.com");
    });
  });
  describe("Given I launch the test email confirmation survey", () => {
    before(async ()=> {
      await browser.openQuestionnaire("test_confirmation_email.json");
    });
    it("When I enter an email and answer 'No' on the confirm email page, Then I go the confirmation send page with the email pre-filled", async ()=> {
      await $(await SubmitPage.submit()).click();
      await $(await SubmitPage.submit()).click();
      await $(await ThankYouPage.email()).setValue("name@example.com");
      await $(await ThankYouPage.submit()).click();
      await $(await ConfirmEmailPage.no()).click();
      await $(await ConfirmEmailPage.submit()).click();
      await expect(browser.getUrl()).to.contain("confirmation-email/send");
      await expect(await $(await ConfirmationEmailPage.email()).getValue()).to.equal("name@example.com");
    });
  });
});

describe("Email confirmation", () => {
  describe("Given I launch the test email confirmation survey", () => {
    before(async ()=> {
      await browser.openQuestionnaire("test_confirmation_email.json");
    });
    it("When I view the email confirmation page, Then I should not see the feedback call to action", async ()=> {
      await $(await SubmitPage.submit()).click();
      await $(await SubmitPage.submit()).click();
      await $(await ThankYouPage.email()).setValue("name@example.com");
      await $(await ThankYouPage.submit()).click();
      await expect(await $(await ConfirmationEmailSentPage.feedbackLink()).isExisting()).to.equal(false);
    });
  });
});
