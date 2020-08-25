import EmailConfirmationPage from "../generated_pages/email/email-confirmation.page";
import SummaryPage from "../generated_pages/email/summary.page";
import ThankYouPage from "../base_pages/thank-you.page";

describe("Error Messages", () => {
  beforeEach(() => {
    browser.openQuestionnaire("test_email.json");
  });

  it("Given a survey has an error when errors are displayed then page error messages are correct", () => {
    $(EmailConfirmationPage.yes()).click();
    $(EmailConfirmationPage.submit()).click();
    $(SummaryPage.submit()).click();
    $(ThankYouPage.email()).setValue("test@test.com");
    $(ThankYouPage.submit()).click();
  });
});
