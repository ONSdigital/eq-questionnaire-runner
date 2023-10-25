import SubmitPage from "../generated_pages/confirmation_email/submit.page";

import ThankYouPage from "../base_pages/thank-you.page";
import ConfirmationEmailPage from "../base_pages/confirmation-email.page";
import ConfirmationEmailSentPage from "../base_pages/confirmation-email-sent.page";
import ConfirmEmailPage from "../base_pages/confirm-email.page";
import { click } from "../helpers";

describe("Email confirmation", () => {
  describe("Given I launch the test email confirmation survey", () => {
    before(async () => {
      await browser.openQuestionnaire("test_confirmation_email.json");
    });

    it("When I complete the survey and am on the thank you page, Then there is option to enter an email address", async () => {
      await click(SubmitPage.submit());
      await click(SubmitPage.submit());
      await expect(browser).toHaveUrlContaining(ThankYouPage.pageName);
      await expect(await $(ThankYouPage.email()).isExisting()).toBe(true);
    });

    it("When I submit the form without providing an email address, Then I get an error message", async () => {
      await click(ThankYouPage.submit());
      await expect(browser).toHaveUrlContaining(ThankYouPage.pageName);
      await expect(await $(ThankYouPage.errorPanel()).isExisting()).toBe(true);
      await expect(await $(ThankYouPage.errorPanel()).getText()).toContain("Enter an email address");
    });

    it("When I submit the form without providing a correctly formatted email address, Then I get an error message", async () => {
      await $(ThankYouPage.email()).setValue("incorrect-format");
      await click(ThankYouPage.submit());
      await expect(browser).toHaveUrlContaining(ThankYouPage.pageName);
      await expect(await $(ThankYouPage.errorPanel()).isExisting()).toBe(true);
      await expect(await $(ThankYouPage.errorPanel()).getText()).toContain("Enter an email address in a valid format, for example name@example.com");
    });

    it("When I submit the form with a valid email address, Then I go to the confirm email page", async () => {
      await $(ThankYouPage.email()).setValue("name@example.com");
      await click(ThankYouPage.submit());
      await expect(browser).toHaveUrlContaining("confirmation-email/confirm");
      await expect(await $(ConfirmEmailPage.questionTitle()).getText()).toBe("Is this email address correct?");
    });

    it("When I submit the confirm email page without providing an answer, Then I get an error message", async () => {
      await click(ConfirmEmailPage.submit());
      await expect(browser).toHaveUrlContaining("confirmation-email/confirm");
      await expect(await $(ConfirmEmailPage.errorPanel()).isExisting()).toBe(true);
      await expect(await $(ConfirmEmailPage.errorPanel()).getText()).toContain("Select an answer");
    });

    it("When I answer 'Yes' and submit the confirm email page, Then I go to email sent page", async () => {
      await $(ConfirmEmailPage.yes()).click();
      await click(ConfirmEmailPage.submit());
      await expect(browser).toHaveUrlContaining("confirmation-email/sent");
      await expect(await $(ConfirmationEmailSentPage.confirmationText()).getText()).toBe("A confirmation email has been sent to name@example.com");
    });

    it("When I go to the confirmation email page and submit without providing an email address, Then I get an error message", async () => {
      await $(ConfirmationEmailSentPage.sendAnotherEmail()).click();
      await click(ConfirmationEmailPage.submit());
      await expect(browser).toHaveUrlContaining("confirmation-email/send");
      await expect(await $(ConfirmationEmailPage.errorPanel()).isExisting()).toBe(true);
      await expect(await $(ConfirmationEmailPage.errorPanel()).getText()).toBe("Enter an email address");
    });

    it("When I submit the form without providing a correctly formatted email address, Then I get an error message", async () => {
      await $(ConfirmationEmailPage.email()).setValue("incorrect-format");
      await click(ConfirmationEmailPage.submit());
      await expect(browser).toHaveUrlContaining("confirmation-email/send");
      await expect(await $(ConfirmationEmailPage.errorPanel()).isExisting()).toBe(true);
      await expect(await $(ConfirmationEmailPage.errorPanel()).getText()).toBe("Enter an email address in a valid format, for example name@example.com");
    });

    it("When I submit the form with a valid email and confirm it is correct, Then I go to the email confirmation page", async () => {
      await $(ConfirmationEmailPage.email()).setValue("name@example.com");
      await click(ConfirmationEmailPage.submit());
      await $(ConfirmEmailPage.yes()).click();
      await click(ConfirmEmailPage.submit());
      await expect(browser).toHaveUrlContaining("confirmation-email/sent");
      await expect(await $(ConfirmationEmailSentPage.confirmationText()).getText()).toBe("A confirmation email has been sent to name@example.com");
    });
  });
  describe("Given I launch the test email confirmation survey", () => {
    before(async () => {
      await browser.openQuestionnaire("test_confirmation_email.json");
    });
    it("When I enter an email and answer 'No' on the confirm email page, Then I go the confirmation send page with the email pre-filled", async () => {
      await click(SubmitPage.submit());
      await click(SubmitPage.submit());
      await $(ThankYouPage.email()).setValue("name@example.com");
      await click(ThankYouPage.submit());
      await $(ConfirmEmailPage.no()).click();
      await click(ConfirmEmailPage.submit());
      await expect(browser).toHaveUrlContaining("confirmation-email/send");
      await expect(await $(ConfirmationEmailPage.email()).getValue()).toBe("name@example.com");
    });
  });
});

describe("Email confirmation", () => {
  describe("Given I launch the test email confirmation survey", () => {
    before(async () => {
      await browser.openQuestionnaire("test_confirmation_email.json");
    });
    it("When I view the email confirmation page, Then I should not see the feedback call to action", async () => {
      await click(SubmitPage.submit());
      await click(SubmitPage.submit());
      await $(ThankYouPage.email()).setValue("name@example.com");
      await click(ThankYouPage.submit());
      await expect(await $(ConfirmationEmailSentPage.feedbackLink()).isExisting()).toBe(false);
    });
  });
});
