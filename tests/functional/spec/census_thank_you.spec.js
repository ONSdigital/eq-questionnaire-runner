import HouseholdConfirmationPage from "../generated_pages/thank_you_census_household/household-confirmation.page";
import HubPage from "../base_pages/hub.page";

import ThankYouPage from "../base_pages/thank-you.page";
import { waitForPage } from "../helpers";

describe("Thank You Census Household", () => {
  describe("Given I launch a census schema without feedback enabled", () => {
    beforeEach(async () => {
      await browser.openQuestionnaire("test_thank_you_census_household.json");
    });

    it("When I navigate to the thank you page, Then I should not see the feedback call to action", async () => {
      await $(HouseholdConfirmationPage.submit()).click();
      await $(HubPage.submit()).click();
      await waitForPage(ThankYouPage.pageName);
      expect(await $(ThankYouPage.feedback()).isExisting()).to.equal(false);
    });
  });
});
