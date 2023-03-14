import CountryCheckboxPage from "../../../generated_pages/routing_checkbox_contains_in/country-checkbox.page";
import CountryInterstitialPage from "../../../generated_pages/routing_checkbox_contains_in/country-interstitial-india.page";
import CountryInterstitialOtherPage from "../../../generated_pages/routing_checkbox_contains_in/country-interstitial-not-india.page";

describe("Feature: Routing - IN Operator", () => {
  describe("Equals", () => {
    describe("Given I start the IN operator routing survey", () => {
      beforeEach(async () => {
        await browser.openQuestionnaire("test_routing_checkbox_contains_in.json");
      });

      it("When I do select India, Then I should be routed to the the correct answer interstitial page", async () => {
        await $(CountryCheckboxPage.india()).click();
        await $(CountryCheckboxPage.submit()).click();
        await expect(await browser.getUrl()).to.contain(CountryInterstitialPage.pageName);
      });

      it("When I do not select India, Then I should be routed to the the incorrect answer interstitial page", async () => {
        await $(CountryCheckboxPage.liechtenstein()).click();
        await $(CountryCheckboxPage.submit()).click();
        await expect(await browser.getUrl()).to.contain(CountryInterstitialOtherPage.pageName);
      });
    });
  });
});
