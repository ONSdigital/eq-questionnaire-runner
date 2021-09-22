import CountryCheckboxPage from "../../../generated_pages/new_routing_checkbox_contains/country-checkbox.page";
import CountryInterstitialPage from "../../../generated_pages/new_routing_checkbox_contains/country-interstitial-india.page";
import SubmitPage from "../../../generated_pages/new_routing_checkbox_contains/submit.page";

describe("Feature: Routing - In Operator", () => {
  describe("Equals", () => {
    describe("Given I start the in operator routing survey", () => {
      beforeEach(() => {
        browser.openQuestionnaire("test_new_routing_checkbox_contains.json");
      });

      it("When I do select India, Then I should be routed to the interstitial page", () => {
        $(CountryCheckboxPage.india()).click();
        $(CountryCheckboxPage.submit()).click();
        expect(browser.getUrl()).to.contain(CountryInterstitialPage.pageName);
      });

      it("When I do not select India, Then I should be routed to the submit page", () => {
        $(CountryCheckboxPage.liechtenstein()).click();
        $(CountryCheckboxPage.submit()).click();
        expect(browser.getUrl()).to.contain(SubmitPage.pageName);
      });
    });
  });
});
