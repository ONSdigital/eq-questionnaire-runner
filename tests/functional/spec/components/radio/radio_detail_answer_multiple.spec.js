import MandatoryRadioPage from "../../../generated_pages/radio_detail_answer_multiple/radio-mandatory.page";
import SubmitPage from "../../../generated_pages/radio_detail_answer_multiple/submit.page";

describe('Radio with multiple "detail_answer" options', () => {
  const radioSchema = "test_radio_detail_answer_multiple.json";

  it("Given detail answer options are available, When the user clicks an option, Then the detail answer input should be visible.", async ()=> {
    await browser.openQuestionnaire(radioSchema);
    await $(await MandatoryRadioPage.eggs()).click();
    await expect(await $(await MandatoryRadioPage.eggsDetail()).isDisplayed()).to.be.true;
    await $(await MandatoryRadioPage.favouriteNotListed()).click();
    await expect(await $(await MandatoryRadioPage.favouriteNotListedDetail()).isDisplayed()).to.be.true;
  });

  it("Given a mandatory detail answer, When I select the option but leave the input field empty and submit, Then an error should be displayed.", async ()=> {
    // Given
    await browser.openQuestionnaire(radioSchema);
    // When
    await $(await MandatoryRadioPage.favouriteNotListed()).click();
    await $(await MandatoryRadioPage.submit()).click();
    // Then
    await expect(await $(await MandatoryRadioPage.error()).isDisplayed()).to.be.true;
    await expect(await $(await MandatoryRadioPage.errorNumber(1)).getText()).to.contain("Enter your favourite to continue");
  });

  it("Given a selected radio answer with an error for a mandatory detail answer, When I enter valid value and submit the page, Then the error is cleared and I navigate to next page.", async ()=> {
    // Given
    await browser.openQuestionnaire(radioSchema);
    await $(await MandatoryRadioPage.favouriteNotListed()).click();
    await $(await MandatoryRadioPage.submit()).click();
    await expect(await $(await MandatoryRadioPage.error()).isDisplayed()).to.be.true;

    // When
    await $(await MandatoryRadioPage.favouriteNotListedDetail()).setValue("Bacon");
    await $(await MandatoryRadioPage.submit()).click();
    await expect(browser.getUrl()).to.contain(SubmitPage.pageName);
  });

  it("Given a non-mandatory detail answer, When the user does not provide any text, Then just the option value should be displayed on the summary screen", async ()=> {
    // Given
    await browser.openQuestionnaire(radioSchema);
    // When
    await $(await MandatoryRadioPage.eggs()).click();
    await expect(await $(await MandatoryRadioPage.eggsDetail()).isDisplayed()).to.be.true;
    await $(await MandatoryRadioPage.submit()).click();
    // Then
    await expect(await $(await SubmitPage.radioMandatoryAnswer()).getText()).to.equal("Eggs");
  });

  it("Given a detail answer, When the user provides text, Then that text should be displayed on the summary screen", async ()=> {
    // Given
    await browser.openQuestionnaire(radioSchema);
    // When
    await $(await MandatoryRadioPage.eggs()).click();
    await $(await MandatoryRadioPage.eggsDetail()).setValue("Scrambled");
    await $(await MandatoryRadioPage.submit()).click();
    // Then
    await expect(await $(await SubmitPage.radioMandatoryAnswer()).getText()).to.equal("Eggs\nScrambled");
  });

  it("Given I have previously added text in a detail answer and saved, When I select a different radio and save, Then the text entered in the detail answer field should be empty.", async ()=> {
    // Given
    await browser.openQuestionnaire(radioSchema);
    // When
    await $(await MandatoryRadioPage.favouriteNotListed()).click();
    await $(await MandatoryRadioPage.favouriteNotListedDetail()).setValue("Bacon");
    await $(await MandatoryRadioPage.submit()).click();
    await $(await SubmitPage.previous()).click();
    await $(await MandatoryRadioPage.eggs()).click();
    await $(await MandatoryRadioPage.submit()).click();
    await $(await SubmitPage.previous()).click();
    // Then
    await $(await MandatoryRadioPage.favouriteNotListed()).click();
    await expect(await $(await MandatoryRadioPage.favouriteNotListedDetail()).getValue()).to.equal("");
  });
});
