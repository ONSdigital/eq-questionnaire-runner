import HouseholdConfirmationPage from "../base_pages/confirmation.page.js";
import HubPage from "../base_pages/hub.page";

import ThankYouPage from "../base_pages/thank-you.page";

describe("Thank You Census Household", () => {
  describe("Given I launch a census schema without feedback enabled", () => {
    beforeEach(() => {
      browser.openQuestionnaire("test_thank_you_census_household.json");
    });

    it("When I navigate to the thank you page, Then I should not see the feedback call to action", () => {
      $(HouseholdConfirmationPage.submit()).click();
      $(HubPage.submit()).click();
      expect(browser.getUrl()).to.contain(ThankYouPage.pageName);
      expect($(ThankYouPage.feedback()).isExisting()).to.equal(false);
    });
  });
});
