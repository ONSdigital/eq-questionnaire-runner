import ListCollectorPage from "../../../generated_pages/placeholder_based_on_first_item_in_list/list-collector.page.js";
import ListCollectorAddPage from "../../../generated_pages/placeholder_based_on_first_item_in_list/list-collector-add.page.js";
import ListStatusInterstitial from "../../../generated_pages/placeholder_based_on_first_item_in_list/list-status.page.js";
import FavouriteDrinkQuestion from "../../../generated_pages/placeholder_based_on_first_item_in_list/favourite-drink.page.js";
import ListStatusQuestion from "../../../generated_pages/placeholder_based_on_first_item_in_list/list-status-2.page.js";
import SummaryPage from "../../../generated_pages/placeholder_based_on_first_item_in_list/personal-details-section-summary.page.js";
import HubPage from "../../../base_pages/hub.page.js";

describe("Component: Definition", () => {
  describe("Load the Survey", () => {
    beforeEach(async () => {
      await browser.openQuestionnaire("test_placeholder_based_on_first_item_in_list.json");
    });

    it("Given I am the first person in the list, When I get to the question page, Then I should see the default answer option", async () => {
      // Given
      await $(HubPage.submit()).click();
      await $(ListCollectorPage.yes()).click();
      await $(ListCollectorPage.submit()).click();
      await $(ListCollectorAddPage.firstName()).setValue("Marcus");
      await $(ListCollectorAddPage.lastName()).setValue("Twin");
      await $(ListCollectorAddPage.submit()).click();
      await $(ListCollectorPage.no()).click();
      await $(ListCollectorPage.submit()).click();
      await $(HubPage.submit()).click();

      // When
      await $(ListStatusInterstitial.submit()).click();
      await $(FavouriteDrinkQuestion.answer()).setValue("Orange Juice");
      await $(FavouriteDrinkQuestion.submit()).click();

      // Then
      await expect(await $(ListStatusQuestion.listStatus2TeaLabel()).getText()).to.contain("Tea");
    });

    it("Given I am not the first person in the list, When I get to the question page, Then I should see the correct answer option", async () => {
      // Given
      await $(HubPage.submit()).click();
      await $(ListCollectorPage.yes()).click();
      await $(ListCollectorPage.submit()).click();
      await $(ListCollectorAddPage.firstName()).setValue("Marcus");
      await $(ListCollectorAddPage.lastName()).setValue("Twin");
      await $(ListCollectorAddPage.submit()).click();
      await $(ListCollectorPage.yes()).click();
      await $(ListCollectorPage.submit()).click();
      await $(ListCollectorAddPage.firstName()).setValue("John");
      await $(ListCollectorAddPage.lastName()).setValue("Doe");
      await $(ListCollectorAddPage.submit()).click();
      await $(ListCollectorPage.no()).click();
      await $(ListCollectorPage.submit()).click();
      await $(HubPage.submit()).click();

      // When
      await $(ListStatusInterstitial.submit()).click();
      await $(FavouriteDrinkQuestion.answer()).setValue("Orange Juice");
      await $(FavouriteDrinkQuestion.submit()).click();
      await $(ListStatusQuestion.listStatus2Tea()).click();
      await $(ListStatusQuestion.submit()).click();
      await $(SummaryPage.submit()).click();
      await $(HubPage.submit()).click();
      await $(ListStatusInterstitial.submit()).click();
      await $(FavouriteDrinkQuestion.answer()).setValue("Lemonade");
      await $(FavouriteDrinkQuestion.submit()).click();

      // Then
      await expect(await $(ListStatusQuestion.listStatus2TeaLabel()).getText()).to.contain("Orange Juice");
    });
  });
});
