import CountryCheckboxPage from "../../../generated_pages/new_routing_checkbox_contains_all/country-checkbox.page";
import CountryInterstitialPage from "../../../generated_pages/new_routing_checkbox_contains_all/country-interstitial-india-and-malta.page";
import CountryInterstitialOtherPage from "../../../generated_pages/new_routing_checkbox_contains_all/country-interstitial-not-india-and-malta.page";

describe("Feature: Routing - ALL-IN Operator", () => {
  describe("Equals", () => {
    describe("Given I start the ALL-IN operator routing survey", () => {
      beforeEach(async ()=> {
        await browser.openQuestionnaire("test_new_routing_checkbox_contains_all.json");
      });

      it("When I do select India and Malta, Then I should be routed to the correct answer interstitial page", async ()=> {
        await $(await CountryCheckboxPage.india()).click();
        await $(await CountryCheckboxPage.malta()).click();
        await $(await CountryCheckboxPage.submit()).click();
        await expect(browser.getUrl()).to.contain(CountryInterstitialPage.pageName);
      });
      it("When I do select India only, Then I should be routed to the correct answer interstitial page", async ()=> {
        await $(await CountryCheckboxPage.india()).click();
        await $(await CountryCheckboxPage.submit()).click();
        await expect(browser.getUrl()).to.contain(CountryInterstitialOtherPage.pageName);
      });

      it("When I do not select India or Malta, Then I should be routed to the incorrect answer interstitial page", async ()=> {
        await $(await CountryCheckboxPage.liechtenstein()).click();
        await $(await CountryCheckboxPage.submit()).click();
        await expect(browser.getUrl()).to.contain(CountryInterstitialOtherPage.pageName);
      });
    });
  });
});
