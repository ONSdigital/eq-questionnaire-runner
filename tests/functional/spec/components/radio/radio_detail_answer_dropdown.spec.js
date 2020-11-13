import RadioDropdownPage from "../../../generated_pages/radio_detail_answer_dropdown/optional-radio-with-dropdown-detail-answer-block.page";
import SummaryPage from "../../../generated_pages/radio_detail_answer_dropdown/summary.page";
import DropdownMandatoryPage from "../../../generated_pages/dropdown_mandatory/dropdown-mandatory.page";

describe("Optional Radio with a Dropdown detail answer", () => {
  beforeEach(() => {
    browser.openQuestionnaire("test_radio_detail_answer_dropdown.json");
  });

  describe("Given an optional radio with a dropdown detail answer", () => {
    it("When a placeholder is set for the detail answer, Then that value should be displayed as the first option", () => {
      $(RadioDropdownPage.fruit()).click();

      expect($(RadioDropdownPage.fruitDetail()).getText()).to.contain("Select fruit");
    });

    it("When a placeholder is not set for the detail answer, Then the default placeholder should be displayed as the first option", () => {
      $(RadioDropdownPage.jam()).click();

      expect($(RadioDropdownPage.jamDetail()).getText()).to.contain("Select an answer");
    });

    it("When the user does not provide an answer and submits, Then the summary should display 'No answer provided'", () => {
      $(RadioDropdownPage.submit()).click();

      expect($(SummaryPage.optionalRadioWithDropdownDetailAnswer()).getText()).to.equal("No answer provided");
    });

    it("When the user selects an option with an optional detail answer but does not provide a detail answer, Then the summary should display the chosen option without the detail answer", () => {
      $(RadioDropdownPage.fruit()).click();
      $(RadioDropdownPage.submit()).click();

      expect($(SummaryPage.optionalRadioWithDropdownDetailAnswer()).getText()).to.equal("Fruit");
    });

    it("When the user selects an option with an optional detail answer and provides a detail answer, Then the summary should display the chosen option and the detail answer", () => {
      $(RadioDropdownPage.fruit()).click();
      $(RadioDropdownPage.fruitDetail()).selectByAttribute("value", "Mango");
      $(RadioDropdownPage.submit()).click();

      expect($(SummaryPage.optionalRadioWithDropdownDetailAnswer()).getText()).to.equal("Fruit\nMango");
    });

    it("When the user selects the default dropdown option after submitting a detail answer, Then the summary should not display the detail answer", () => {
      $(RadioDropdownPage.fruit()).click();
      $(RadioDropdownPage.fruitDetail()).selectByAttribute("value", "Mango");
      $(RadioDropdownPage.submit()).click();
      $(SummaryPage.previous()).click();
      $(RadioDropdownPage.fruitDetail()).selectByVisibleText("Select fruit");
      $(RadioDropdownPage.submit()).click();

      expect($(SummaryPage.optionalRadioWithDropdownDetailAnswer()).getText()).to.equal("Fruit");
    });

    it("When the user selects an option with an mandatory detail answer but does not provide a detail answer, Then an error should be displayed when the user submits", () => {
      $(RadioDropdownPage.jam()).click();
      $(RadioDropdownPage.submit()).click();

      expect($(DropdownMandatoryPage.errorNumber(1)).getText()).to.equal("Please select the type of Jam");
    });

    it("When the user selects an option with an mandatory detail answer and provides a detail answer, Then the summary should display the chosen option and its detail answer", () => {
      $(RadioDropdownPage.jam()).click();
      $(RadioDropdownPage.jamDetail()).selectByAttribute("value", "Strawberry");
      $(RadioDropdownPage.submit()).click();

      expect($(SummaryPage.optionalRadioWithDropdownDetailAnswer()).getText()).to.equal("Jam\nStrawberry");
    });

    it("When the user removes a previously submitted detail answer by selecting another radio option, Then the summary should only display the new radio option", () => {
      $(RadioDropdownPage.jam()).click();
      $(RadioDropdownPage.jamDetail()).selectByAttribute("value", "Raspberry");
      $(RadioDropdownPage.submit()).click();
      $(SummaryPage.previous()).click();
      $(RadioDropdownPage.fruit()).click();
      $(RadioDropdownPage.submit()).click();

      expect($(SummaryPage.optionalRadioWithDropdownDetailAnswer()).getText()).to.equal("Fruit");
    });
  });
});
