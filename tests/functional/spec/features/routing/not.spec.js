import CountryCheckboxPage from "../../../generated_pages/new_routing_not/country-checkbox.page";
import CountryInterstitialPage from "../../../generated_pages/new_routing_not/country-interstitial-india.page";
import SubmitPage from "../../../generated_pages/new_routing_not/submit.page";

describe("Feature: Routing - Not Operator", () => {
  describe("Equals", () => {
    describe("Given I start the not operator routing survey", () => {
      beforeEach(() => {
        browser.openQuestionnaire("test_new_routing_not.json");
      });

      it("When I do not select India, Then I should be routed to the interstitial page", () => {
        $(CountryCheckboxPage.azerbaijan()).click();
        $(CountryCheckboxPage.submit()).click();
        expect(browser.getUrl()).to.contain(CountryInterstitialPage.pageName);
      });

      it("When I do select India, Then I should be routed to the submit page", () => {
        $(CountryCheckboxPage.india()).click();
        $(CountryCheckboxPage.submit()).click();
        expect(browser.getUrl()).to.contain(SubmitPage.pageName);
      });
    });
  });
});
