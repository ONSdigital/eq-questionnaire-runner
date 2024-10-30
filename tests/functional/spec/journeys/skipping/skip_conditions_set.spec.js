import FoodPage from "../../../generated_pages/skip_condition_set/food-block.page";
import DrinkPage from "../../../generated_pages/skip_condition_set/drink-block.page";
import SubmitPage from "../../../generated_pages/skip_condition_set/submit.page";
import { click, verifyUrlContains } from "../../../helpers";
describe("Skip Conditions - Set", () => {
  beforeEach("Load the survey", async () => {
    await browser.openQuestionnaire("test_skip_condition_set.json");
  });

  it("Given I complete the first page, Then I should see the summary page", async () => {
    await $(FoodPage.bacon()).click();
    await click(FoodPage.submit());
    await verifyUrlContains(SubmitPage.pageName);
  });

  it("Given I do not complete the first page, Then I should see the drink page", async () => {
    await click(FoodPage.submit());
    await verifyUrlContains(DrinkPage.pageName);
  });
});
