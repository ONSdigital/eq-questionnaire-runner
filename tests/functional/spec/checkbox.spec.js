import MandatoryCheckboxPage from "../generated_pages/checkbox/mandatory-checkbox.page";
import NonMandatoryCheckboxPage from "../generated_pages/checkbox/non-mandatory-checkbox.page";
import singleCheckboxPage from "../generated_pages/checkbox/single-checkbox.page";
import SubmitPage from "../generated_pages/checkbox/submit.page";
import { click } from "../helpers";

describe('Checkbox with "other" option', () => {
  beforeEach("Load the survey", async () => {
    await browser.openQuestionnaire("test_checkbox.json");
  });

  it("Given a label has not been provided in the schema for a checkbox answer, When the checkbox answer is displayed, Then the default label should be visible", async () => {
    await expect(await $("body").getText()).to.have.string("Select all that apply");
  });

  it("Given a label has been set in the schema for a checkbox answer, When the checkbox answer is displayed, Then the label should be visible", async () => {
    await $(MandatoryCheckboxPage.none()).click();
    await click(MandatoryCheckboxPage.submit());
    await expect(await $("body").getText()).to.have.string("Select any answers that apply");
  });

  it("Given that there is only one checkbox, When the checkbox answer is displayed, Then no label should be present", async () => {
    await $(MandatoryCheckboxPage.none()).click();
    await click(MandatoryCheckboxPage.submit());
    await click(NonMandatoryCheckboxPage.submit());
    await expect(await $("body").getText()).to.not.have.string("Select all that apply");
  });

  it('Given an "other" option is available, when the user clicks the "other" option the other input should be visible.', async () => {
    await expect(await $(MandatoryCheckboxPage.otherLabelDescription()).getText()).to.have.string("Choose any other topping");
    await $(MandatoryCheckboxPage.other()).click();
    await expect(await $(MandatoryCheckboxPage.otherDetail()).isDisplayed()).to.be.true;
  });

  it("Given a mandatory checkbox answer, When I select the other option, leave the input field empty and submit, Then an error should be displayed.", async () => {
    // When
    await $(MandatoryCheckboxPage.other()).click();
    await click(MandatoryCheckboxPage.submit());
    // Then
    await expect(await $(MandatoryCheckboxPage.error()).isDisplayed()).to.be.true;
  });

  it("Given a mandatory checkbox answer, When I leave the input field empty and submit, Then the question text should be hidden in the error message using a span element.", async () => {
    // When
    await click(MandatoryCheckboxPage.submit());
    // Then
    await expect(await $(MandatoryCheckboxPage.error()).getHTML()).to.contain(
      'Select at least one answer <span class="ons-u-vh">to ‘Which pizza toppings would you like?’</span></a>',
    );
  });

  it("Given a mandatory checkbox answer, when there is an error on the page for other field and I enter valid value and submit page, then the error is cleared and I navigate to next page.s", async () => {
    await $(MandatoryCheckboxPage.other()).click();
    await click(MandatoryCheckboxPage.submit());
    await expect(await $(MandatoryCheckboxPage.error()).isDisplayed()).to.be.true;

    // When
    await $(MandatoryCheckboxPage.otherDetail()).setValue("Other Text");
    await click(MandatoryCheckboxPage.submit());
    await expect(await browser.getUrl()).to.contain(NonMandatoryCheckboxPage.pageName);
  });

  it('Given a non-mandatory checkbox answer, when the user does not select an option, then "No answer provided" should be displayed on the summary screen', async () => {
    // When
    await $(MandatoryCheckboxPage.other()).click();
    await $(MandatoryCheckboxPage.otherDetail()).setValue("Other value");
    await click(MandatoryCheckboxPage.submit());
    await click(NonMandatoryCheckboxPage.submit());
    await click(singleCheckboxPage.submit());
    // Then
    await expect(await $(SubmitPage.nonMandatoryCheckboxAnswer()).getText()).to.contain("No answer provided");
  });

  it('Given a non-mandatory checkbox answer, when the user selects Other but does not supply a value, then "Other" should be displayed on the summary screen', async () => {
    // When
    await $(MandatoryCheckboxPage.other()).click();
    await $(MandatoryCheckboxPage.otherDetail()).setValue("Other value");
    await click(MandatoryCheckboxPage.submit());
    await $(NonMandatoryCheckboxPage.other()).click();
    await click(NonMandatoryCheckboxPage.submit());
    await click(singleCheckboxPage.submit());
    // Then
    await expect(await $(SubmitPage.nonMandatoryCheckboxAnswer()).getText()).to.contain("Other");
  });

  it("Given a non-mandatory checkbox answer, when the user selects Other and supplies a value, then the supplied value should be displayed on the summary screen", async () => {
    // When
    await $(MandatoryCheckboxPage.other()).click();
    await $(MandatoryCheckboxPage.otherDetail()).setValue("Other value");
    await click(MandatoryCheckboxPage.submit());
    await $(NonMandatoryCheckboxPage.other()).click();
    await $(NonMandatoryCheckboxPage.otherDetail()).setValue("The other value");
    await click(NonMandatoryCheckboxPage.submit());
    await click(singleCheckboxPage.submit());
    // Then
    await expect(await $(SubmitPage.nonMandatoryCheckboxAnswer()).getText()).to.contain("The other value");
  });

  it("Given that there is an escaped character in an answer label, when the user selects the answer, then the label should be displayed on the summary screen", async () => {
    // When
    await $(MandatoryCheckboxPage.hamCheese()).click();
    await click(MandatoryCheckboxPage.submit());
    await $(NonMandatoryCheckboxPage.other()).click();
    await $(NonMandatoryCheckboxPage.otherDetail()).setValue("The other value");
    await click(NonMandatoryCheckboxPage.submit());
    await click(singleCheckboxPage.submit());
    // Then
    await expect(await $(SubmitPage.mandatoryCheckboxAnswer()).getText()).to.contain("Ham & Cheese");
  });

  it("Given I have previously added text in other textfield and saved, when I uncheck other options and select a different checkbox as answer, then the text entered in other field must be wiped.", async () => {
    // When
    await $(MandatoryCheckboxPage.other()).click();
    await $(MandatoryCheckboxPage.otherDetail()).setValue("Other value");
    await click(MandatoryCheckboxPage.submit());
    await $(NonMandatoryCheckboxPage.previous()).click();
    await $(MandatoryCheckboxPage.other()).click();
    await $(MandatoryCheckboxPage.hamCheese()).click();
    await click(MandatoryCheckboxPage.submit());
    await $(NonMandatoryCheckboxPage.previous()).click();
    // Then
    await $(MandatoryCheckboxPage.other()).click();
    await expect(await $(MandatoryCheckboxPage.otherDetail()).getValue()).to.equal("");
  });

  it("Given a mandatory checkbox answer, when the user selects only one option, then the answer should not be displayed as a list on the summary screen", async () => {
    // When
    await $(MandatoryCheckboxPage.ham()).click();
    await click(MandatoryCheckboxPage.submit());
    await click(NonMandatoryCheckboxPage.submit());
    // Then

    const listLength = await $$(`${SubmitPage.mandatoryCheckboxAnswer()} li`).length;

    // Then
    await expect(listLength).to.equal(0);
  });

  it("Given a mandatory checkbox answer, when the user selects more than one option, then the answer should be displayed as a list on the summary screen", async () => {
    // When
    await $(MandatoryCheckboxPage.ham()).click();
    await $(MandatoryCheckboxPage.hamCheese()).click();
    await click(MandatoryCheckboxPage.submit());
    await click(NonMandatoryCheckboxPage.submit());
    await click(singleCheckboxPage.submit());

    const listLength = await $$(`${SubmitPage.mandatoryCheckboxAnswer()} li`).length;

    // Then
    await expect(listLength).to.equal(2);
  });
});
