import CountryCheckboxPage from "../../../generated_pages/routing_checkbox_contains_all/country-checkbox.page";
import CountryInterstitialPage from "../../../generated_pages/routing_checkbox_contains_all/country-interstitial-india-and-malta.page";
import CountryInterstitialOtherPage from "../../../generated_pages/routing_checkbox_contains_all/country-interstitial-not-india-and-malta.page";
import { click, verifyUrlContains } from "../../../helpers";

describe("Feature: Routing - ALL-IN Operator", () => {
  describe("Equals", () => {
    describe("Given I start the ALL-IN operator routing survey", () => {
      beforeEach(async () => {
        await browser.openQuestionnaire("test_routing_checkbox_contains_all.json");
      });

      it("When I do select India and Malta, Then I should be routed to the correct answer interstitial page", async () => {
        await $(CountryCheckboxPage.india()).click();
        await $(CountryCheckboxPage.malta()).click();
        await click(CountryCheckboxPage.submit());
        await verifyUrlContains(CountryInterstitialPage.pageName);
      });
      it("When I do select India only, Then I should be routed to the correct answer interstitial page", async () => {
        await $(CountryCheckboxPage.india()).click();
        await click(CountryCheckboxPage.submit());
        await verifyUrlContains(CountryInterstitialOtherPage.pageName);
      });

      it("When I do not select India or Malta, Then I should be routed to the incorrect answer interstitial page", async () => {
        await $(CountryCheckboxPage.liechtenstein()).click();
        await click(CountryCheckboxPage.submit());
        await verifyUrlContains(CountryInterstitialOtherPage.pageName);
      });
    });
  });
});
