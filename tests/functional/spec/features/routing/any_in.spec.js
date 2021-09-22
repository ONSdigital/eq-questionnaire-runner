import CountryCheckboxPage from "../../../generated_pages/new_routing_checkbox_contains_any/country-checkbox.page";
import CountryInterstitialPage from "../../../generated_pages/new_routing_checkbox_contains_any/country-interstitial-india-malta.page";
import SubmitPage from "../../../generated_pages/new_routing_checkbox_contains_any/submit.page";

describe("Feature: Routing - Any-In Operator", () => {
  describe("Equals", () => {
    describe("Given I start the any-in operator routing survey", () => {
      beforeEach(() => {
        browser.openQuestionnaire("test_new_routing_checkbox_contains_any.json");
      });

      it("When I do select India and Malta, Then I should be routed to the interstitial page", () => {
        $(CountryCheckboxPage.india()).click();
        $(CountryCheckboxPage.malta()).click();
        $(CountryCheckboxPage.submit()).click();
        expect(browser.getUrl()).to.contain(CountryInterstitialPage.pageName);
      });

      it("When I do select India or Malta, Then I should be routed to the interstitial page", () => {
        $(CountryCheckboxPage.india()).click();
        $(CountryCheckboxPage.submit()).click();
        expect(browser.getUrl()).to.contain(CountryInterstitialPage.pageName);
      });
      it("When I do not select India or Malta, Then I should be routed to the submit page", () => {
        $(CountryCheckboxPage.liechtenstein()).click();
        $(CountryCheckboxPage.submit()).click();
        expect(browser.getUrl()).to.contain(SubmitPage.pageName);
      });
    });
  });
});
