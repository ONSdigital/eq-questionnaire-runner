import MandatoryCheckboxPage from "../../../generated_pages/checkbox_detail_answer_multiple/mandatory-checkbox.page";
import SubmitPage from "../../../generated_pages/checkbox_detail_answer_multiple/submit.page";
import { click } from "../../../helpers";
describe('Checkbox with multiple "detail_answer" options', () => {
  const checkboxSchema = "test_checkbox_detail_answer_multiple.json";

  it("Given detail answer options are available, When the user clicks an option, Then the detail answer input should be visible.", async () => {
    await browser.openQuestionnaire(checkboxSchema);
    await $(MandatoryCheckboxPage.yourChoice()).click();
    await expect(await $(MandatoryCheckboxPage.yourChoiceDetail()).isDisplayed()).to.be.true;
    await $(MandatoryCheckboxPage.cheese()).click();
    await expect(await $(MandatoryCheckboxPage.cheeseDetail()).isDisplayed()).to.be.true;
  });

  it("Given a mandatory detail answer, When I select the option but leave the input field empty and submit, Then an error should be displayed.", async () => {
    // Given
    await browser.openQuestionnaire(checkboxSchema);
    // When
    // Non-Mandatory detail answer given
    await $(MandatoryCheckboxPage.cheese()).click();
    await $(MandatoryCheckboxPage.cheeseDetail()).setValue("Mozzarella");
    // Mandatory detail answer left blank
    await $(MandatoryCheckboxPage.yourChoice()).click();
    await click(MandatoryCheckboxPage.submit());
    // Then
    await expect(await $(MandatoryCheckboxPage.error()).isDisplayed()).to.be.true;
    await expect(await $(MandatoryCheckboxPage.errorNumber(1)).getText()).to.contain("Enter your topping choice to continue");
  });

  it("Given a selected checkbox answer with an error for a mandatory detail answer, When I enter valid value and submit the page, Then the error is cleared and I navigate to next page.", async () => {
    // Given
    await browser.openQuestionnaire(checkboxSchema);
    await $(MandatoryCheckboxPage.yourChoice()).click();
    await click(MandatoryCheckboxPage.submit());
    await expect(await $(MandatoryCheckboxPage.error()).isDisplayed()).to.be.true;

    // When
    await $(MandatoryCheckboxPage.yourChoiceDetail()).setValue("Bacon");
    await click(MandatoryCheckboxPage.submit());
    await expect(await browser.getUrl()).to.contain(SubmitPage.pageName);
  });

  it("Given a non-mandatory detail answer, When the user does not provide any text, Then just the option value should be displayed on the summary screen", async () => {
    // Given
    await browser.openQuestionnaire(checkboxSchema);
    // When
    await $(MandatoryCheckboxPage.cheese()).click();
    await expect(await $(MandatoryCheckboxPage.cheeseDetail()).isDisplayed()).to.be.true;
    await click(MandatoryCheckboxPage.submit());
    // Then
    await expect(await $(SubmitPage.mandatoryCheckboxAnswer()).getText()).to.equal("Cheese");
  });

  it("Given multiple detail answers, When the user provides text for all, Then that text should be displayed on the summary screen", async () => {
    // Given
    await browser.openQuestionnaire(checkboxSchema);
    // When
    await $(MandatoryCheckboxPage.cheese()).click();
    await $(MandatoryCheckboxPage.cheeseDetail()).setValue("Mozzarella");
    await $(MandatoryCheckboxPage.yourChoice()).click();
    await $(MandatoryCheckboxPage.yourChoiceDetail()).setValue("Bacon");
    await click(MandatoryCheckboxPage.submit());
    // Then
    await expect(await $(SubmitPage.mandatoryCheckboxAnswer()).getText()).to.equal("Cheese\nMozzarella\nYour choice\nBacon");
  });

  it("Given multiple detail answers, When the user provides text for just one, Then that text should be displayed on the summary screen", async () => {
    // Given
    await browser.openQuestionnaire(checkboxSchema);
    // When
    await $(MandatoryCheckboxPage.yourChoice()).click();
    await $(MandatoryCheckboxPage.yourChoiceDetail()).setValue("Bacon");
    await click(MandatoryCheckboxPage.submit());
    // Then
    await expect(await $(SubmitPage.mandatoryCheckboxAnswer()).getText()).to.equal("Your choice\nBacon");
  });

  it("Given I have previously added text in a detail answer and saved, When I uncheck the detail answer option and select a different checkbox, Then the text entered in the detail answer field should be empty.", async () => {
    // Given
    await browser.openQuestionnaire(checkboxSchema);
    // When
    await $(MandatoryCheckboxPage.cheese()).click();
    await $(MandatoryCheckboxPage.cheeseDetail()).setValue("Mozzarella");
    await click(MandatoryCheckboxPage.submit());
    await $(SubmitPage.previous()).click();
    await $(MandatoryCheckboxPage.cheese()).click();
    await $(MandatoryCheckboxPage.ham()).click();
    await click(MandatoryCheckboxPage.submit());
    await $(SubmitPage.previous()).click();
    // Then
    await $(MandatoryCheckboxPage.cheese()).click();
    await expect(await $(MandatoryCheckboxPage.cheeseDetail()).getValue()).to.equal("");
  });
});
