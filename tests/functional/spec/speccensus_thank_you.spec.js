import { SubmitPage } from "../base_pages/submit.page.js";
import HubPage from "../base_pages/hub.page";

import ThankYouPage from "../base_pages/thank-you.page";

describe("Thank You Census Household", () => {
  describe("Given I launch a census schema without feedback enabled", () => {
    beforeEach(async ()=> {
      await browser.openQuestionnaire("test_thank_you_census_household.json");
    });

    it("When I navigate to the thank you page, Then I should not see the feedback call to action", async ()=> {
      await $(await SubmitPage.submit()).click();
      await $(await HubPage.submit()).click();
      await expect(browser.getUrl()).to.contain(ThankYouPage.pageName);
      await expect(await $(await ThankYouPage.feedback()).isExisting()).to.equal(false);
    });
  });
});
