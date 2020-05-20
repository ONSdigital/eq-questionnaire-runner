const ListCollectorPage = require("../generated_pages/answer_based_on_first_item_in_list/list-collector.page.js");
const ListCollectorAddPage = require("../generated_pages/answer_based_on_first_item_in_list/list-collector-add.page.js");
const ListStatusQuestion = require("../generated_pages/answer_based_on_first_item_in_list/list-status.page.js");
const FavouriteDrinkQuestion = require("../generated_pages/answer_based_on_first_item_in_list/favourite-drink.page.js");
const ListStatusTwoQuestion = require("../generated_pages/answer_based_on_first_item_in_list/list-status-2.page.js");
const SummaryPage = require("../generated_pages/answer_based_on_first_item_in_list/personal-details-section-summary.page.js");

const HubPage = require("../base_pages/hub.page.js");

describe("Answer Option Based on First Item in List", function() {
  it("Given I am the first person in the list, When I get to the question page, Then I should see the default answer option", function() {
    browser.openQuestionnaire("test_answer_based_on_first_item_in_list.json");
    $(HubPage.submit()).click();
    $(ListCollectorPage.yes()).click();
    $(ListCollectorPage.submit()).click();
    $(ListCollectorAddPage.firstName()).setValue("Marcus");
    $(ListCollectorAddPage.lastName()).setValue("Twin");
    $(ListCollectorAddPage.submit()).click();
    $(ListCollectorPage.no()).click();
    $(ListCollectorPage.submit()).click();
    $(HubPage.submit()).click();
    $(ListStatusQuestion.yes()).click();
    $(ListStatusQuestion.submit()).click();
    $(FavouriteDrinkQuestion.answer()).setValue("Orange Juice");
    $(FavouriteDrinkQuestion.submit()).click();
    expect($(ListStatusTwoQuestion.listStatus2TeaLabel()).getText()).to.contain("Tea");
  });

    it("Given I am the the second person in the list, When I get to the question page, Then I should see the correct answer option", function() {
    browser.openQuestionnaire("test_answer_based_on_first_item_in_list.json");
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
    $(ListStatusQuestion.yes()).click();
    $(ListStatusQuestion.submit()).click();
    $(FavouriteDrinkQuestion.answer()).setValue("Orange Juice");
    $(FavouriteDrinkQuestion.submit()).click();
    $(ListStatusTwoQuestion.listStatus2Tea()).click();
    $(ListStatusTwoQuestion.submit()).click();
    $(SummaryPage.submit()).click();
    $(HubPage.submit()).click();
    $(ListStatusQuestion.yes()).click();
    $(ListStatusQuestion.submit()).click();
    $(FavouriteDrinkQuestion.answer()).setValue("Lemonade");
    $(FavouriteDrinkQuestion.submit()).click();
    expect($(ListStatusTwoQuestion.listStatus2TeaLabel()).getText()).to.contain("Orange Juice");
  });
});
