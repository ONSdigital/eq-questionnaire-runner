import CountryCheckboxPage from "../../../generated_pages/new_routing_checkbox_contains_all/country-checkbox.page";
import CountryInterstitialPage from "../../../generated_pages/new_routing_checkbox_contains_all/country-interstitial-india-malta.page";
import CountryInterstitialOtherPage from "../../../generated_pages/new_routing_checkbox_contains_all/country-interstitial-other.page";

describe("Feature: Routing - ALL-IN Operator", () => {
  describe("Equals", () => {
    describe("Given I start the ALL-IN operator routing survey", () => {
      beforeEach(() => {
        browser.openQuestionnaire("test_new_routing_checkbox_contains_all.json");
      });

      it("When I do select India and Malta, Then I should be routed to the interstitial page", () => {
        $(CountryCheckboxPage.india()).click();
        $(CountryCheckboxPage.malta()).click();
        $(CountryCheckboxPage.submit()).click();
        expect(browser.getUrl()).to.contain(CountryInterstitialPage.pageName);
      });
      it("When I do select India only, Then I should be routed to the submit page", () => {
        $(CountryCheckboxPage.india()).click();
        $(CountryCheckboxPage.submit()).click();
        expect(browser.getUrl()).to.contain(CountryInterstitialOtherPage.pageName);
      });

      it("When I do not select India or Malta, Then I should be routed to the submit page", () => {
        $(CountryCheckboxPage.liechtenstein()).click();
        $(CountryCheckboxPage.submit()).click();
        expect(browser.getUrl()).to.contain(CountryInterstitialOtherPage.pageName);
      });
    });
  });
});
