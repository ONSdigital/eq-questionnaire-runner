import CountryCheckboxPage from "../../../generated_pages/routing_not/country-checkbox.page";
import CountryInterstitialPage from "../../../generated_pages/routing_not/country-interstitial-not-india.page";
import IndiaInterstitialPage from "../../../generated_pages/routing_not/country-interstitial-india.page";
import { click } from "../../../helpers";
describe("Feature: Routing - Not Operator", () => {
  describe("Equals", () => {
    describe("Given I start the not operator routing survey", () => {
      beforeEach(async () => {
        await browser.openQuestionnaire("test_routing_not.json");
      });

      it("When I do not select India, Then I should be routed to the not India interstitial page", async () => {
        await $(CountryCheckboxPage.azerbaijan()).click();
        await click(CountryCheckboxPage.submit());
        await expect(browser).toHaveUrlContaining(CountryInterstitialPage.pageName);
      });

      it("When I select India, Then I should be routed to the India interstitial page", async () => {
        await $(CountryCheckboxPage.india()).click();
        await click(CountryCheckboxPage.submit());
        await expect(browser).toHaveUrlContaining(IndiaInterstitialPage.pageName);
      });
    });
  });
});
