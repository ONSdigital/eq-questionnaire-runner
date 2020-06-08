import ListCollectorPage from "../generated_pages/placeholder_based_on_first_item_in_list/list-collector.page.js";
import ListCollectorAddPage from "../generated_pages/placeholder_based_on_first_item_in_list/list-collector-add.page.js";
import ListStatusInterstitial from "../generated_pages/placeholder_based_on_first_item_in_list/list-status.page.js";
import FavouriteDrinkQuestion from "../generated_pages/placeholder_based_on_first_item_in_list/favourite-drink.page.js";
import ListStatusQuestion from "../generated_pages/placeholder_based_on_first_item_in_list/list-status-2.page.js";
import SummaryPage from "../generated_pages/placeholder_based_on_first_item_in_list/personal-details-section-summary.page.js";
import HubPage from "../base_pages/hub.page.js";

describe("Component: Definition", () => {
  describe("Load the Survey", () => {
    beforeEach(() => {
      browser.openQuestionnaire("test_placeholder_based_on_first_item_in_list.json");
    });

    it("Given I am the first person in the list, When I get to the question page, Then I should see the default answer option", () => {
      // Given
      $(HubPage.submit()).click();
      $(ListCollectorPage.yes()).click();
      $(ListCollectorPage.submit()).click();
      $(ListCollectorAddPage.firstName()).setValue("Marcus");
      $(ListCollectorAddPage.lastName()).setValue("Twin");
      $(ListCollectorAddPage.submit()).click();
      $(ListCollectorPage.no()).click();
      $(ListCollectorPage.submit()).click();
      $(HubPage.submit()).click();

      // When
      $(ListStatusInterstitial.submit()).click();
      $(FavouriteDrinkQuestion.answer()).setValue("Orange Juice");
      $(FavouriteDrinkQuestion.submit()).click();

      // Then
      expect($(ListStatusQuestion.listStatus2TeaLabel()).getText()).to.contain("Tea");
    });

    it("Given I am not the first person in the list, When I get to the question page, Then I should see the correct answer option", () => {
      // Given
      $(HubPage.submit()).click();
      $(ListCollectorPage.yes()).click();
      $(ListCollectorPage.submit()).click();
      $(ListCollectorAddPage.firstName()).setValue("Marcus");
      $(ListCollectorAddPage.lastName()).setValue("Twin");
      $(ListCollectorAddPage.submit()).click();
      $(ListCollectorPage.yes()).click();
      $(ListCollectorPage.submit()).click();
      $(ListCollectorAddPage.firstName()).setValue("John");
      $(ListCollectorAddPage.lastName()).setValue("Doe");
      $(ListCollectorAddPage.submit()).click();
      $(ListCollectorPage.no()).click();
      $(ListCollectorPage.submit()).click();
      $(HubPage.submit()).click();

      // When
      $(ListStatusInterstitial.submit()).click();
      $(FavouriteDrinkQuestion.answer()).setValue("Orange Juice");
      $(FavouriteDrinkQuestion.submit()).click();
      $(ListStatusQuestion.listStatus2Tea()).click();
      $(ListStatusQuestion.submit()).click();
      $(SummaryPage.submit()).click();
      $(HubPage.submit()).click();
      $(ListStatusInterstitial.submit()).click();
      $(FavouriteDrinkQuestion.answer()).setValue("Lemonade");
      $(FavouriteDrinkQuestion.submit()).click();

      // Then
      expect($(ListStatusQuestion.listStatus2TeaLabel()).getText()).to.contain("Orange Juice");
    });
  });
});
