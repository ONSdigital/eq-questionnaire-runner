import SchemaConfirmationPage from "../generated_pages/email_confirmation/schema-confirmation.page";
import SummaryPage from "../generated_pages/email_confirmation/summary.page";

import ThankYouPage from "../base_pages/thank-you.page";
import EmailConfirmationPage from "../base_pages/email-confirmation.page";
import EmailConfirmationSentPage from "../base_pages/email-confirmation-sent.page";

describe("Email confirmation", () => {
  describe("Given I complete the test email confirmation survey", () => {
    before(() => {
      browser.openQuestionnaire("test_email_confirmation.json");
    });

    it("When I am on the thank you page, Then there is email confirmation textfield", () => {
      $(SchemaConfirmationPage.submit()).click();
      $(SummaryPage.submit()).click();
      expect(browser.getUrl()).to.contain(ThankYouPage.pageName);
      expect($(ThankYouPage.email()).isExisting()).to.be.true;
    });

    it("When I submit the email form without providing an email, Then I get an error message", () => {
      $(ThankYouPage.submit()).click();
      expect(browser.getUrl()).to.contain(ThankYouPage.pageName);
      expect($(ThankYouPage.errorPanel()).isExisting()).to.be.true;
      expect($(ThankYouPage.errorPanel()).getText()).to.equal("1) Enter an email address to continue");
    });

    it("When I submit the email form without providing a correctly formatted email, Then I get an error message", () => {
      $(ThankYouPage.email()).setValue("incorrect-format");
      $(ThankYouPage.submit()).click();
      expect(browser.getUrl()).to.contain(ThankYouPage.pageName);
      expect($(ThankYouPage.errorPanel()).isExisting()).to.be.true;
      expect($(ThankYouPage.errorPanel()).getText()).to.equal("1) Enter an email in a valid format, for example name@example.com");
    });

    it("When I submit the form with a valid email, Then I go to the email confirmation sent page", () => {
      $(ThankYouPage.email()).setValue("name@example.com");
      $(ThankYouPage.submit()).click();
      expect(browser.getUrl()).to.contain(EmailConfirmationSentPage.pageName);
    });

    it("when I submit from the email confirmation page without providing an email, Then I get an error message", () => {
      $(EmailConfirmationSentPage.sendAnotherEmail()).click();
      $(EmailConfirmationPage.submit()).click();
      expect(browser.getUrl()).to.contain(EmailConfirmationPage.pageName);
      expect($(EmailConfirmationPage.errorPanel()).isExisting()).to.be.true;
      expect($(EmailConfirmationPage.errorPanel()).getText()).to.equal("1) Enter an email address to continue");
    });

    it("when I submit from the email confirmation page without providing an valid email, Then I get an error message", () => {
      $(EmailConfirmationPage.email()).setValue("incorrect-format");
      $(EmailConfirmationPage.submit()).click();
      expect(browser.getUrl()).to.contain(EmailConfirmationPage.pageName);
      expect($(EmailConfirmationPage.errorPanel()).isExisting()).to.be.true;
      expect($(EmailConfirmationPage.errorPanel()).getText()).to.equal("1) Enter an email in a valid format, for example name@example.com");
    });

    it("When I submit the form with a valid email from the email confirmation page , Then I go to the email confirmation sent page", () => {
      $(EmailConfirmationPage.email()).setValue("name@example.com");
      $(EmailConfirmationPage.submit()).click();
      expect(browser.getUrl()).to.contain(EmailConfirmationSentPage.pageName);
    });
  });
});
