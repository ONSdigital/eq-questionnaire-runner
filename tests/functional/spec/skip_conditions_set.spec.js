import FoodPage from "../generated_pages/skip_condition_set/food-block.page";
import DrinkPage from "../generated_pages/skip_condition_set/drink-block.page";
import SummaryPage from "../generated_pages/skip_condition_set/summary.page";

describe("Skip Conditions - Set", () => {
  beforeEach("Load the survey", () => {
    browser.openQuestionnaire("test_skip_condition_set.json");
  });

  it("Given I complete the first page, Then I should see the summary page", () => {
    $(FoodPage.bacon()).click();
    $(FoodPage.submit()).click();
    expect(browser.getUrl()).to.contain(SummaryPage.pageName);
  });

  it("Given I do not complete the first page, Then I should see the drink page", () => {
    $(FoodPage.submit()).click();
    expect(browser.getUrl()).to.contain(DrinkPage.pageName);
  });
});
