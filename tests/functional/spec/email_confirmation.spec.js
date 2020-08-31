import SchemaConfirmationPage from "../generated_pages/email_confirmation/schema-confirmation.page";
import SummaryPage from "../generated_pages/email_confirmation/summary.page";

import ThankYouPage from "../base_pages/thank-you.page";
import AdditionalEmailPage from "../base_pages/another-email.page";
import EmailConfirmationPage from "../base_pages/email-confirmation.page";

describe("Email confirmation", () => {
  describe("Given I complete the test email confirmation survey", () => {
    before(() => {
      browser.openQuestionnaire("test_email_confirmation.json");
    });

    it("When I am on the thank you page, Then there is option to enter an email address", () => {
      $(SchemaConfirmationPage.submit()).click();
      $(SummaryPage.submit()).click();
      expect(browser.getUrl()).to.contain(ThankYouPage.pageName);
      expect($(ThankYouPage.email()).isExisting()).to.be.true;
    });

    it("When I submit the email form without providing an email address, Then I get an error message", () => {
      $(ThankYouPage.submit()).click();
      expect(browser.getUrl()).to.contain(ThankYouPage.pageName);
      expect($(ThankYouPage.errorPanel()).isExisting()).to.be.true;
      expect($(ThankYouPage.errorPanel()).getText()).to.equal("1. Enter an email address to continue");
    });

    it("When I submit the email form without providing a correctly formatted email address, Then I get an error message", () => {
      $(ThankYouPage.email()).setValue("incorrect-format");
      $(ThankYouPage.submit()).click();
      expect(browser.getUrl()).to.contain(ThankYouPage.pageName);
      expect($(ThankYouPage.errorPanel()).isExisting()).to.be.true;
      expect($(ThankYouPage.errorPanel()).getText()).to.equal("1. Enter an email in a valid format, for example name@example.com");
    });

    it("When I submit the email form with a valid email address, Then I go to the email confirmation page", () => {
      $(ThankYouPage.email()).setValue("name@example.com");
      $(ThankYouPage.submit()).click();
      expect(browser.getUrl()).to.contain(EmailConfirmationPage.pageName);
      expect(EmailConfirmationPage.confirmationText()).to.equal("A confirmation email has been sent to name@example.com");
    });

    it("when I submit from the additional email page without providing an email address, Then I get an error message", () => {
      $(EmailConfirmationPage.sendAnotherEmail()).click();
      $(AdditionalEmailPage.submit()).click();
      expect(browser.getUrl()).to.contain(AdditionalEmailPage.pageName);
      expect($(AdditionalEmailPage.errorPanel()).isExisting()).to.be.true;
      expect($(AdditionalEmailPage.errorPanel()).getText()).to.equal("1. Enter an email address to continue");
    });

    it("when I submit the form without providing a correctly formatted email address, Then I get an error message", () => {
      $(AdditionalEmailPage.email()).setValue("incorrect-format");
      $(AdditionalEmailPage.submit()).click();
      expect(browser.getUrl()).to.contain(EmailConfirmationPage.pageName);
      expect($(AdditionalEmailPage.errorPanel()).isExisting()).to.be.true;
      expect($(AdditionalEmailPage.errorPanel()).getText()).to.equal("1. Enter an email in a valid format, for example name@example.com");
    });

    it("When I submit the form with a valid email from the additional email page , Then I go to the email confirmation page", () => {
      $(AdditionalEmailPage.email()).setValue("name@example.com");
      $(AdditionalEmailPage.submit()).click();
      expect(browser.getUrl()).to.contain(EmailConfirmationPage.pageName);
      expect(EmailConfirmationPage.confirmationText()).to.equal("A confirmation email has been sent to name@example.com");
    });
  });
});
