import ToppingCheckboxPage from "../../../generated_pages/routing_checkbox_set_not_set/topping-checkbox.page.js";
import ToppingInterstitialNotSetPage from "../../../generated_pages/routing_checkbox_set_not_set/topping-interstitial-not-set.page.js";
import ToppingInterstitialSetPage from "../../../generated_pages/routing_checkbox_set_not_set/topping-interstitial-set.page.js";
import OptionalMutuallyExclusivePage from "../../../generated_pages/routing_checkbox_set_not_set/optional-mutually-exclusive.page.js";
import CheeseInterstitialNotSetPage from "../../../generated_pages/routing_checkbox_set_not_set/cheese-interstitial-not-set.page.js";
import CheeseInterstitialSetPage from "../../../generated_pages/routing_checkbox_set_not_set/cheese-interstitial-set.page.js";
import SummaryPage from "../../../generated_pages/routing_checkbox_set_not_set/summary.page.js";

describe("Test routing using not set and set conditions on checkboxes", () => {
  beforeEach(() => {
    browser.openQuestionnaire("test_routing_checkbox_set_not_set.json");
  });

  it("Given a user sets a topping and a cheese, they should see an interstitial for each saying that they were set", () => {
    $(ToppingCheckboxPage.cheese()).click();
    $(ToppingCheckboxPage.submit()).click();

    expect(browser.getUrl()).to.contain(ToppingInterstitialSetPage.pageName);

    $(ToppingInterstitialSetPage.submit()).click();

    $(OptionalMutuallyExclusivePage.iDonTLikeCheese()).click();
    $(OptionalMutuallyExclusivePage.submit()).click();

    expect(browser.getUrl()).to.contain(CheeseInterstitialSetPage.pageName);

    $(CheeseInterstitialSetPage.submit()).click();

    expect(browser.getUrl()).to.contain(SummaryPage.pageName);
  });

  it("Given a user does not set a topping and does not set a cheese, they should see an interstitial for each saying that they were not set", () => {
    $(ToppingCheckboxPage.submit()).click();

    expect(browser.getUrl()).to.contain(ToppingInterstitialNotSetPage.pageName);

    $(ToppingInterstitialNotSetPage.submit()).click();

    $(OptionalMutuallyExclusivePage.submit()).click();

    expect(browser.getUrl()).to.contain(CheeseInterstitialNotSetPage.pageName);

    $(CheeseInterstitialNotSetPage.submit()).click();

    expect(browser.getUrl()).to.contain(SummaryPage.pageName);
  });
});
