import MandatoryCheckboxPage from "../../../generated_pages/placeholder_playback_list/mandatory-checkbox.page";
import { click, getRawHTML from "../../../helpers";
describe("Feature: Playback Confirmation", () => {
  beforeEach("Open the schema", async () => {
    await browser.openQuestionnaire("test_placeholder_playback_list.json");
  });

  it("When the user submits an answer, their answers should be shown on the confirmation screen", async () => {
    await $(MandatoryCheckboxPage.cheese()).click();
    await $(MandatoryCheckboxPage.ham()).click();
    await click(MandatoryCheckboxPage.submit());

    await expect(await getRawHTML($("#confirm-answers-question ul"))).toContain("Ham");
    await expect(await getRawHTML($("#confirm-answers-question ul"))).toContain("Cheese");
  });
});
