import ListCollectorPage from "../generated_pages/skip_condition_list/list-collector.page.js";
import ListCollectorAddPage from "../generated_pages/skip_condition_list/list-collector-add.page.js";
import LessThanTwoInterstitialPage from "../generated_pages/skip_condition_list/less-than-two-interstitial.page.js";
import TwoInterstitialPage from "../generated_pages/skip_condition_list/two-interstitial.page.js";
import MoreThanTwoInterstitialPage from "../generated_pages/skip_condition_list/more-than-two-interstitial.page.js";

describe("Feature: Routing on lists", () => {
  describe("Given I start skip condition list survey", () => {
    beforeEach(() => {
      browser.openQuestionnaire("test_skip_condition_list.json");
    });

    it("When I don't add a person to the list, Then the less than two people skippable page should be shown", () => {
      $(ListCollectorPage.no()).click();
      $(ListCollectorPage.submit()).click();
      expect(browser.getUrl()).to.contain(LessThanTwoInterstitialPage.pageName);
    });

    it("When I add one person to the list, Then the less than two people skippable page should be shown", () => {
      $(ListCollectorPage.yes()).click();
      $(ListCollectorPage.submit()).click();
      $(ListCollectorAddPage.firstName()).setValue("Marcus");
      $(ListCollectorAddPage.lastName()).setValue("Twin");
      $(ListCollectorAddPage.submit()).click();
      $(ListCollectorPage.no()).click();
      $(ListCollectorPage.submit()).click();
      expect(browser.getUrl()).to.contain(LessThanTwoInterstitialPage.pageName);
    });

    it("When I add two people to the list, Then the two people skippable page should be shown", () => {
      $(ListCollectorPage.yes()).click();
      $(ListCollectorPage.submit()).click();
      $(ListCollectorAddPage.firstName()).setValue("Marcus");
      $(ListCollectorAddPage.lastName()).setValue("Twin");
      $(ListCollectorAddPage.submit()).click();
      $(ListCollectorPage.yes()).click();
      $(ListCollectorPage.submit()).click();
      $(ListCollectorAddPage.firstName()).setValue("Samuel");
      $(ListCollectorAddPage.lastName()).setValue("Clemens");
      $(ListCollectorAddPage.submit()).click();
      $(ListCollectorPage.no()).click();
      $(ListCollectorPage.submit()).click();
      expect(browser.getUrl()).to.contain(TwoInterstitialPage.pageName);
    });

    it("When I add three people to the list, Then the more than two people skippable page should be shown", () => {
      $(ListCollectorPage.yes()).click();
      $(ListCollectorPage.submit()).click();
      $(ListCollectorAddPage.firstName()).setValue("Marcus");
      $(ListCollectorAddPage.lastName()).setValue("Twin");
      $(ListCollectorAddPage.submit()).click();
      $(ListCollectorPage.yes()).click();
      $(ListCollectorPage.submit()).click();
      $(ListCollectorAddPage.firstName()).setValue("Samuel");
      $(ListCollectorAddPage.lastName()).setValue("Clemens");
      $(ListCollectorAddPage.submit()).click();
      $(ListCollectorPage.yes()).click();
      $(ListCollectorPage.submit()).click();
      $(ListCollectorAddPage.firstName()).setValue("Olivia");
      $(ListCollectorAddPage.lastName()).setValue("Clemens");
      $(ListCollectorAddPage.submit()).click();
      $(ListCollectorPage.no()).click();
      $(ListCollectorPage.submit()).click();
      expect(browser.getUrl()).to.contain(MoreThanTwoInterstitialPage.pageName);
    });
  });
});
