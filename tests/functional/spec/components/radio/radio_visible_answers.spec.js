import RadioVisibleTruePage from "../../../generated_pages/radio_detail_answer_visible/radio-visible-true.page.js";
import RadioVisibleFalsePage from "../../../generated_pages/radio_detail_answer_visible/radio-visible-false.page.js";
import RadioVisibleNonePage from "../../../generated_pages/radio_detail_answer_visible/radio-visible-none.page.js";
import { click } from "../../../helpers";
describe("Given I start a Radio survey with a write-in option", () => {
  beforeEach(async () => {
    await browser.openQuestionnaire("test_radio_detail_answer_visible.json");
  });

  it("When I view a write-in radio and the visible option is set to true, Then the detail answer label should be displayed", async () => {
    await expect(await $(RadioVisibleTruePage.otherDetail()).isDisplayed()).toBe(true);
  });

  it("When I view a write-in radio and the visible option is set to true, Then after choosing non write-in option the detail answer label should be displayed", async () => {
    await $(RadioVisibleTruePage.coffee()).click();
    await expect(await $(RadioVisibleTruePage.otherDetail()).isDisplayed()).toBe(true);
  });

  it("When I view a write-in radio and the visible option is set to false, Then the detail answer label should not be displayed", async () => {
    await $(RadioVisibleTruePage.coffee()).click();
    await click(RadioVisibleTruePage.submit());
    await expect(await $(RadioVisibleFalsePage.otherDetail()).isDisplayed()).toBe(false);
  });

  it("When I view a write-in radio and the visible option is not set, Then the detail answer label should not be displayed", async () => {
    await $(RadioVisibleTruePage.coffee()).click();
    await click(RadioVisibleFalsePage.submit());
    await $(RadioVisibleFalsePage.iceCream()).click();
    await click(RadioVisibleFalsePage.submit());
    await expect(await $(RadioVisibleNonePage.otherDetail()).isDisplayed()).toBe(false);
  });
});
