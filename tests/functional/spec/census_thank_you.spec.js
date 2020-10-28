import HouseholdConfirmationPage from "../generated_pages/thank_you_census_household/household-confirmation.page";
import Summary from "../generated_pages/thank_you_census_household/summary.page";

import ThankYouPage from "../base_pages/thank-you.page";

describe("Thank You Census Household", () => {
  describe("Given I launch the Thank You Census Household schema", () => {
    beforeEach(() => {
      browser.openQuestionnaire("test_thank_you_census_household.json");
    });

    it("When I navigate to the thank you page I should not see the, Then I should not see the feedback call to action", () => {
      $(HouseholdConfirmationPage.submit()).click();
      $(Summary.submit()).click();
      expect(browser.getUrl()).to.contain(ThankYouPage.pageName);
      expect($(ThankYouPage.feedback()).isExisting()).to.equal(false);
    });
  });
});
