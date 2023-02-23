import MandatoryCheckboxPage from "../../../generated_pages/placeholder_playback_list/mandatory-checkbox.page";

describe("Feature: Playback Confirmation", () => {
  beforeEach("Open the schema", async () => {
    await browser.openQuestionnaire("test_placeholder_playback_list.json");
  });

  it("When the user submits an answer, their answers should be shown on the confirmation screen", async () => {
    await $(MandatoryCheckboxPage.cheese()).click();
    await $(MandatoryCheckboxPage.ham()).click();
    await $(MandatoryCheckboxPage.submit()).click();

    await expect(await $("#confirm-answers-question ul").getHTML())
      .to.contain("Cheese")
      .to.contain("Ham");
  });
});
