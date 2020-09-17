import MandatoryCheckboxPage from "../generated_pages/checkbox/mandatory-checkbox.page";
import NonMandatoryCheckboxPage from "../generated_pages/checkbox/non-mandatory-checkbox.page";
import singleCheckboxPage from "../generated_pages/checkbox/single-checkbox.page";
import SummaryPage from "../generated_pages/checkbox/summary.page";

describe('Checkbox with "other" option', () => {
  beforeEach("Load the survey", () => {
    browser.openQuestionnaire("test_checkbox.json");
  });

  it("Given a label has not been provided in the schema for a checkbox answer, When the checkbox answer is displayed, Then the default label should be visible", () => {
    expect($("body").getText()).to.have.string("Select at least one answer");
  });

  it("Given a label has been set in the schema for a checkbox answer, When the checkbox answer is displayed, Then the label should be visible", () => {
    $(MandatoryCheckboxPage.none()).click();
    $(MandatoryCheckboxPage.submit()).click();
    expect($("body").getText()).to.have.string("Select any answers that apply");
  });

  it("Given that there is only one checkbox, When the checkbox answer is displayed, Then no label should be present", () => {
    $(MandatoryCheckboxPage.none()).click();
    $(MandatoryCheckboxPage.submit()).click();
    $(NonMandatoryCheckboxPage.submit()).click();
    expect($("body").getText()).to.not.have.string("Select all that apply");
  });

  it('Given an "other" option is available, when the user clicks the "other" option the other input should be visible.', () => {
    expect($(MandatoryCheckboxPage.otherLabelDescription()).getText()).to.have.string("Choose any other topping");
    $(MandatoryCheckboxPage.other()).click();
    expect($(MandatoryCheckboxPage.otherDetail()).isDisplayed()).to.be.true;
  });

  it("Given a mandatory checkbox answer, When I select the other option, leave the input field empty and submit, Then an error should be displayed.", () => {
    // When
    $(MandatoryCheckboxPage.other()).click();
    $(MandatoryCheckboxPage.submit()).click();
    // Then
    expect($(MandatoryCheckboxPage.error()).isDisplayed()).to.be.true;
  });

  it("Given a mandatory checkbox answer, When I leave the input field empty and submit, Then the question text should be hidden in the error message using a span element.", () => {
    // When
    $(MandatoryCheckboxPage.submit()).click();
    // Then
    expect($(MandatoryCheckboxPage.error()).getHTML()).to.contain(
      'Select at least one answer <span class="u-vh">to ‘Which pizza toppings would you like?’</span></a>'
    );
  });

  it("Given a mandatory checkbox answer, when there is an error on the page for other field and I enter valid value and submit page, then the error is cleared and I navigate to next page.s", () => {
    $(MandatoryCheckboxPage.other()).click();
    $(MandatoryCheckboxPage.submit()).click();
    expect($(MandatoryCheckboxPage.error()).isDisplayed()).to.be.true;

    // When
    $(MandatoryCheckboxPage.otherDetail()).setValue("Other Text");
    $(MandatoryCheckboxPage.submit()).click();
    expect(browser.getUrl()).to.contain(NonMandatoryCheckboxPage.pageName);
  });

  it('Given a non-mandatory checkbox answer, when the user does not select an option, then "No answer provided" should be displayed on the summary screen', () => {
    // When
    $(MandatoryCheckboxPage.other()).click();
    $(MandatoryCheckboxPage.otherDetail()).setValue("Other value");
    $(MandatoryCheckboxPage.submit()).click();
    $(NonMandatoryCheckboxPage.submit()).click();
    $(singleCheckboxPage.submit()).click();
    // Then
    expect($(SummaryPage.nonMandatoryCheckboxAnswer()).getText()).to.contain("No answer provided");
  });

  it('Given a non-mandatory checkbox answer, when the user selects Other but does not supply a value, then "Other" should be displayed on the summary screen', () => {
    // When
    $(MandatoryCheckboxPage.other()).click();
    $(MandatoryCheckboxPage.otherDetail()).setValue("Other value");
    $(MandatoryCheckboxPage.submit()).click();
    $(NonMandatoryCheckboxPage.other()).click();
    $(NonMandatoryCheckboxPage.submit()).click();
    $(singleCheckboxPage.submit()).click();
    // Then
    expect($(SummaryPage.nonMandatoryCheckboxAnswer()).getText()).to.contain("Other");
  });

  it("Given a non-mandatory checkbox answer, when the user selects Other and supplies a value, then the supplied value should be displayed on the summary screen", () => {
    // When
    $(MandatoryCheckboxPage.other()).click();
    $(MandatoryCheckboxPage.otherDetail()).setValue("Other value");
    $(MandatoryCheckboxPage.submit()).click();
    $(NonMandatoryCheckboxPage.other()).click();
    $(NonMandatoryCheckboxPage.otherDetail()).setValue("The other value");
    $(NonMandatoryCheckboxPage.submit()).click();
    $(singleCheckboxPage.submit()).click();
    // Then
    expect($(SummaryPage.nonMandatoryCheckboxAnswer()).getText()).to.contain("The other value");
  });

  it("Given I have previously added text in other textfield and saved, when I uncheck other options and select a different checkbox as answer, then the text entered in other field must be wiped.", () => {
    // When
    $(MandatoryCheckboxPage.other()).click();
    $(MandatoryCheckboxPage.otherDetail()).setValue("Other value");
    $(MandatoryCheckboxPage.submit()).click();
    $(NonMandatoryCheckboxPage.previous()).click();
    $(MandatoryCheckboxPage.other()).click();
    $(MandatoryCheckboxPage.cheese()).click();
    $(MandatoryCheckboxPage.submit()).click();
    $(NonMandatoryCheckboxPage.previous()).click();
    // Then
    $(MandatoryCheckboxPage.other()).click();
    expect($(MandatoryCheckboxPage.otherDetail()).getValue()).to.equal("");
  });

  it("Given a mandatory checkbox answer, when the user selects only one option, then the answer should not be displayed as a list on the summary screen", () => {
    // When
    $(MandatoryCheckboxPage.ham()).click();
    $(MandatoryCheckboxPage.submit()).click();
    $(NonMandatoryCheckboxPage.submit()).click();
    // Then

    const listLength = $$(`${SummaryPage.mandatoryCheckboxAnswer()} li`).length;

    // Then
    expect(listLength).to.equal(0);
  });

  it("Given a mandatory checkbox answer, when the user selects more than one option, then the answer should be displayed as a list on the summary screen", () => {
    // When
    $(MandatoryCheckboxPage.ham()).click();
    $(MandatoryCheckboxPage.cheese()).click();
    $(MandatoryCheckboxPage.submit()).click();
    $(NonMandatoryCheckboxPage.submit()).click();
    $(singleCheckboxPage.submit()).click();

    const listLength = $$(`${SummaryPage.mandatoryCheckboxAnswer()} li`).length;

    // Then
    expect(listLength).to.equal(2);
  });
});
