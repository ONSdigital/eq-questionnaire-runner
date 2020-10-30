import HouseholdConfirmationPage from "../generated_pages/thank_you_census_household/household-confirmation.page";
import Summary from "../generated_pages/thank_you_census_household/summary.page";

import ThankYouPage from "../base_pages/thank-you.page";

describe("Thank You Census Household", () => {
  describe("Given I launch a census schema without feedback enabled", () => {
    beforeEach(() => {
      browser.openQuestionnaire("test_thank_you_census_household.json");
    });

    it("When I navigate to the thank you page, Then I should not see the feedback call to action", () => {
      $(HouseholdConfirmationPage.submit()).click();
      $(Summary.submit()).click();
      expect(browser.getUrl()).to.contain(ThankYouPage.pageName);
      expect($(ThankYouPage.feedback()).isExisting()).to.equal(false);
    });
  });
});
