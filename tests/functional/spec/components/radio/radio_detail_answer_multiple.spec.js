import MandatoryRadioPage from "../../../generated_pages/radio_detail_answer_multiple/radio-mandatory.page";
import SubmitPage from "../../../generated_pages/radio_detail_answer_multiple/submit.page";
import { click } from "../../../helpers";
describe('Radio with multiple "detail_answer" options', () => {
  const radioSchema = "test_radio_detail_answer_multiple.json";

  it("Given detail answer options are available, When the user clicks an option, Then the detail answer input should be visible.", async () => {
    await browser.openQuestionnaire(radioSchema);
    await $(MandatoryRadioPage.eggs()).click();
    await expect(await $(MandatoryRadioPage.eggsDetail()).isDisplayed()).toBe(true);
    await $(MandatoryRadioPage.favouriteNotListed()).click();
    await expect(await $(MandatoryRadioPage.favouriteNotListedDetail()).isDisplayed()).toBe(true);
  });

  it("Given a mandatory detail answer, When I select the option but leave the input field empty and submit, Then an error should be displayed.", async () => {
    // Given
    await browser.openQuestionnaire(radioSchema);
    // When
    await $(MandatoryRadioPage.favouriteNotListed()).click();
    await click(MandatoryRadioPage.submit());
    // Then
    await expect(await $(MandatoryRadioPage.error()).isDisplayed()).toBe(true);
    await expect(await $(MandatoryRadioPage.errorNumber(1)).getText()).toBe("Enter your favourite to continue");
  });

  it("Given a selected radio answer with an error for a mandatory detail answer, When I enter valid value and submit the page, Then the error is cleared and I navigate to next page.", async () => {
    // Given
    await browser.openQuestionnaire(radioSchema);
    await $(MandatoryRadioPage.favouriteNotListed()).click();
    await click(MandatoryRadioPage.submit());
    await expect(await $(MandatoryRadioPage.error()).isDisplayed()).toBe(true);

    // When
    await $(MandatoryRadioPage.favouriteNotListedDetail()).setValue("Bacon");
    await click(MandatoryRadioPage.submit());
    await expect(browser).toHaveUrl(expect.stringContaining(SubmitPage.pageName));
  });

  it("Given a non-mandatory detail answer, When the user does not provide any text, Then just the option value should be displayed on the summary screen", async () => {
    // Given
    await browser.openQuestionnaire(radioSchema);
    // When
    await $(MandatoryRadioPage.eggs()).click();
    await expect(await $(MandatoryRadioPage.eggsDetail()).isDisplayed()).toBe(true);
    await click(MandatoryRadioPage.submit());
    // Then
    await expect(await $(SubmitPage.radioMandatoryAnswer()).getText()).toBe("Eggs");
  });

  it("Given a detail answer, When the user provides text, Then that text should be displayed on the summary screen", async () => {
    // Given
    await browser.openQuestionnaire(radioSchema);
    // When
    await $(MandatoryRadioPage.eggs()).click();
    await $(MandatoryRadioPage.eggsDetail()).setValue("Scrambled");
    await click(MandatoryRadioPage.submit());
    // Then
    await expect(await $(SubmitPage.radioMandatoryAnswer()).getText()).toBe("Eggs\nScrambled");
  });

  it("Given I have previously added text in a detail answer and saved, When I select a different radio and save, Then the text entered in the detail answer field should be empty.", async () => {
    // Given
    await browser.openQuestionnaire(radioSchema);
    // When
    await $(MandatoryRadioPage.favouriteNotListed()).click();
    await $(MandatoryRadioPage.favouriteNotListedDetail()).setValue("Bacon");
    await click(MandatoryRadioPage.submit());
    await $(SubmitPage.previous()).click();
    await $(MandatoryRadioPage.eggs()).click();
    await click(MandatoryRadioPage.submit());
    await $(SubmitPage.previous()).click();
    // Then
    await $(MandatoryRadioPage.favouriteNotListed()).click();
    await expect(await $(MandatoryRadioPage.favouriteNotListedDetail()).getValue()).toBe("");
  });
});
