import MandatoryCheckboxPage from "../../../generated_pages/placeholder_playback_list/mandatory-checkbox.page";

describe("Feature: Playback Confirmation", () => {
  beforeEach("Open the schema", async ()=> {
    await browser.openQuestionnaire("test_placeholder_playback_list.json");
  });

  it("When the user submits an answer, their answers should be shown on the confirmation screen", async ()=> {
    await $(await MandatoryCheckboxPage.cheese()).click();
    await $(await MandatoryCheckboxPage.ham()).click();
    await $(await MandatoryCheckboxPage.submit()).click();

    await expect($("#confirm-answers-question ul").getHTML()).to.contain("Cheese").to.contain("Ham");
  });
});
