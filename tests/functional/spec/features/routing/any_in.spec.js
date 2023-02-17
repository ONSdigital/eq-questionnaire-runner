import CountryCheckboxPage from "../../../generated_pages/new_routing_checkbox_contains_any/country-checkbox.page";
import CountryInterstitialPage from "../../../generated_pages/new_routing_checkbox_contains_any/country-interstitial-india-or-malta-or-both.page";
import CountryInterstitialOtherPage from "../../../generated_pages/new_routing_checkbox_contains_any/country-interstitial-not-india-or-malta-or-both.page";

describe("Feature: Routing - ANY-IN Operator", () => {
  describe("Equals", () => {
    describe("Given I start the ANY-IN operator routing survey", () => {
      beforeEach(async () => {
        await browser.openQuestionnaire("test_new_routing_checkbox_contains_any.json");
      });

      it("When I do select India and Malta, Then I should be routed to the correct answer interstitial page", async () => {
        await $(CountryCheckboxPage.india()).click();
        await $(CountryCheckboxPage.malta()).click();
        await $(CountryCheckboxPage.submit()).click();
        await expect(browser.getUrl()).to.contain(CountryInterstitialPage.pageName);
      });

      it("When I do select India or Malta, Then I should be routed to the correct answer interstitial page", async () => {
        await $(CountryCheckboxPage.india()).click();
        await $(CountryCheckboxPage.submit()).click();
        await expect(browser.getUrl()).to.contain(CountryInterstitialPage.pageName);
      });
      it("When I do not select India or Malta, Then I should be routed to the incorrect answer interstitial page", async () => {
        await $(CountryCheckboxPage.liechtenstein()).click();
        await $(CountryCheckboxPage.submit()).click();
        await expect(browser.getUrl()).to.contain(CountryInterstitialOtherPage.pageName);
      });
    });
  });
});
