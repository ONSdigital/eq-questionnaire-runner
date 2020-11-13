import CheckboxDropdownPage from "../../../generated_pages/checkbox_detail_answer_dropdown/optional-checkbox-with-dropdown-detail-answer-block.page";
import SummaryPage from "../../../generated_pages/checkbox_detail_answer_dropdown/summary.page";
import DropdownMandatoryPage from "../../../generated_pages/dropdown_mandatory/dropdown-mandatory.page";

describe("Optional Checkbox with a Dropdown detail answer", () => {
  beforeEach(() => {
    browser.openQuestionnaire("test_checkbox_detail_answer_dropdown.json");
  });

  describe("Given an optional checkbox with a dropdown detail answer", () => {
    it("When a placeholder is set for the detail answer, Then that value should be displayed as the first option", () => {
      $(CheckboxDropdownPage.fruit()).click();

      expect($(CheckboxDropdownPage.fruitDetail()).getText()).to.contain("Select fruit");
    });

    it("When a placeholder is not set for the detail answer, Then the default placeholder should be displayed as the first option", () => {
      $(CheckboxDropdownPage.jam()).click();

      expect($(CheckboxDropdownPage.jamDetail()).getText()).to.contain("Select an answer");
    });

    it("When the user does not provide an answer and submits, Then the summary should display 'No answer provided'", () => {
      $(CheckboxDropdownPage.submit()).click();

      expect($(SummaryPage.optionalCheckboxWithDropdownDetailAnswer()).getText()).to.equal("No answer provided");
    });

    it("When the user selects an option with an optional detail answer but does not provide a detail answer, Then the summary should display the chosen option without the detail answer", () => {
      $(CheckboxDropdownPage.fruit()).click();
      $(CheckboxDropdownPage.submit()).click();

      expect($(SummaryPage.optionalCheckboxWithDropdownDetailAnswer()).getText()).to.equal("Fruit");
    });

    it("When the user selects an option with an optional detail answer and provides a detail answer, Then the summary should display the chosen option and the detail answer", () => {
      $(CheckboxDropdownPage.fruit()).click();
      $(CheckboxDropdownPage.fruitDetail()).selectByAttribute("value", "Mango");
      $(CheckboxDropdownPage.submit()).click();

      expect($(SummaryPage.optionalCheckboxWithDropdownDetailAnswer()).getText()).to.equal("Fruit\nMango");
    });

    it("When the user selects the default dropdown option after submitting a detail answer, Then the summary should not display the detail answer", () => {
      $(CheckboxDropdownPage.fruit()).click();
      $(CheckboxDropdownPage.fruitDetail()).selectByAttribute("value", "Mango");
      $(CheckboxDropdownPage.submit()).click();
      $(SummaryPage.previous()).click();
      $(CheckboxDropdownPage.fruitDetail()).selectByVisibleText("Select fruit");
      $(CheckboxDropdownPage.submit()).click();

      expect($(SummaryPage.optionalCheckboxWithDropdownDetailAnswer()).getText()).to.equal("Fruit");
    });

    it("When the user selects an option with an mandatory detail answer but does not provide a detail answer, Then an error should be displayed when the user submits", () => {
      $(CheckboxDropdownPage.jam()).click();
      $(CheckboxDropdownPage.submit()).click();

      expect($(DropdownMandatoryPage.errorNumber(1)).getText()).to.equal("Please select the type of Jam");
    });

    it("When the user selects an option with an mandatory detail answer and provides a detail answer, Then the summary should display the chosen option and its details", () => {
      $(CheckboxDropdownPage.jam()).click();
      $(CheckboxDropdownPage.jamDetail()).selectByAttribute("value", "Strawberry");
      $(CheckboxDropdownPage.submit()).click();

      expect($(SummaryPage.optionalCheckboxWithDropdownDetailAnswer()).getText()).to.equal("Jam\nStrawberry");
    });

    it("When the user removes a previously submitted detail answer, Then the summary should not display the removed detail answer", () => {
      $(CheckboxDropdownPage.fruit()).click();
      $(CheckboxDropdownPage.fruitDetail()).selectByAttribute("value", "Mango");
      $(CheckboxDropdownPage.submit()).click();
      $(SummaryPage.previous()).click();
      $(CheckboxDropdownPage.fruit()).click();
      $(CheckboxDropdownPage.submit()).click();

      expect($(SummaryPage.optionalCheckboxWithDropdownDetailAnswer()).getText()).to.equal("No answer provided");
    });

    it("When the user selects multiple options with detail answers and submits, Then the summary should display all the chosen options and their detail answer", () => {
      $(CheckboxDropdownPage.fruit()).click();
      $(CheckboxDropdownPage.fruitDetail()).selectByAttribute("value", "Mango");
      $(CheckboxDropdownPage.jam()).click();
      $(CheckboxDropdownPage.jamDetail()).selectByAttribute("value", "Strawberry");
      $(CheckboxDropdownPage.submit()).click();

      expect($(SummaryPage.optionalCheckboxWithDropdownDetailAnswer()).getText()).to.equal("Fruit\nMango\nJam\nStrawberry");
    });
  });
});
