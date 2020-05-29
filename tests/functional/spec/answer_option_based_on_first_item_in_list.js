const ListCollectorPage = require("../generated_pages/placeholder_based_on_first_item_in_list/list-collector.page.js");
const ListCollectorAddPage = require("../generated_pages/placeholder_based_on_first_item_in_list/list-collector-add.page.js");
const ListStatusInterstitial = require("../generated_pages/placeholder_based_on_first_item_in_list/list-status.page.js");
const FavouriteDrinkQuestion = require("../generated_pages/placeholder_based_on_first_item_in_list/favourite-drink.page.js");
const ListStatusQuestion = require("../generated_pages/placeholder_based_on_first_item_in_list/list-status-2.page.js");
const SummaryPage = require("../generated_pages/placeholder_based_on_first_item_in_list/personal-details-section-summary.page.js");

const HubPage = require("../base_pages/hub.page.js");

describe("Component: Definition", function() {
  describe("Load the Survey", function() {
    beforeEach(function() {
      browser.openQuestionnaire("test_placeholder_based_on_first_item_in_list.json");
    });

    it("Given I am the first person in the list, When I get to the question page, Then I should see the default answer option", function() {
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

    it("Given I am not the first person in the list, When I get to the question page, Then I should see the correct answer option", function() {
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
