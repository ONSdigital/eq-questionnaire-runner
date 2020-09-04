import SchemaConfirmationPage from "../generated_pages/confirmation_email/schema-confirmation.page";
import SummaryPage from "../generated_pages/confirmation_email/summary.page";

import ThankYouPage from "../base_pages/thank-you.page";
import ConfirmationEmailPage from "../base_pages/confirmation-email.page";
import ConfirmationEmailSentPage from "../base_pages/confirmation-email-sent.page";

describe("Email confirmation", () => {
  describe("Given I launch the test email confirmation survey", () => {
    before(() => {
      browser.openQuestionnaire("test_confirmation_email.json");
    });

    it("When I complete the survey and am on the thank you page, Then there is option to enter an email address", () => {
      $(SchemaConfirmationPage.submit()).click();
      $(SummaryPage.submit()).click();
      expect(browser.getUrl()).to.contain(ThankYouPage.pageName);
      expect($(ThankYouPage.email()).isExisting()).to.be.true;
    });

    it("When I submit the form without providing an email address, Then I get an error message", () => {
      $(ThankYouPage.submit()).click();
      expect(browser.getUrl()).to.contain(ThankYouPage.pageName);
      expect($(ThankYouPage.errorPanel()).isExisting()).to.be.true;
      expect($(ThankYouPage.errorPanel()).getText()).to.contain("1. Enter an email address");
    });

    it("When I submit the form without providing a correctly formatted email address, Then I get an error message", () => {
      $(ThankYouPage.email()).setValue("incorrect-format");
      $(ThankYouPage.submit()).click();
      expect(browser.getUrl()).to.contain(ThankYouPage.pageName);
      expect($(ThankYouPage.errorPanel()).isExisting()).to.be.true;
      expect($(ThankYouPage.errorPanel()).getText()).to.contain("1. Enter an email in a valid format, for example name@example.com");
    });

    it("When I submit the form with a valid email address, Then I go to the email confirmation sent page", () => {
      $(ThankYouPage.email()).setValue("name@example.com");
      $(ThankYouPage.submit()).click();
      expect(browser.getUrl()).to.contain("confirmation-email/sent");
      expect($(ConfirmationEmailSentPage.confirmationText()).getText()).to.equal("A confirmation email has been sent to name@example.com");
    });

    it("when I go to the confirmation email page and submit without providing an email address, Then I get an error message", () => {
      $(ConfirmationEmailSentPage.sendAnotherEmail()).click();
      $(ConfirmationEmailPage.submit()).click();
      expect(browser.getUrl()).to.contain("confirmation-email/send");
      expect($(ConfirmationEmailPage.errorPanel()).isExisting()).to.be.true;
      expect($(ConfirmationEmailPage.errorPanel()).getText()).to.equal("1. Enter an email address");
    });

    it("when I submit the form without providing a correctly formatted email address, Then I get an error message", () => {
      $(ConfirmationEmailPage.email()).setValue("incorrect-format");
      $(ConfirmationEmailPage.submit()).click();
      expect(browser.getUrl()).to.contain("confirmation-email/send");
      expect($(ConfirmationEmailPage.errorPanel()).isExisting()).to.be.true;
      expect($(ConfirmationEmailPage.errorPanel()).getText()).to.equal("1. Enter an email in a valid format, for example name@example.com");
    });

    it("When I submit the form with a valid email, Then I go to the email confirmation page", () => {
      $(ConfirmationEmailPage.email()).setValue("name@example.com");
      $(ConfirmationEmailPage.submit()).click();
      expect(browser.getUrl()).to.contain("confirmation-email/sent");
      expect($(ConfirmationEmailSentPage.confirmationText()).getText()).to.equal("A confirmation email has been sent to name@example.com");
    });
  });
});
