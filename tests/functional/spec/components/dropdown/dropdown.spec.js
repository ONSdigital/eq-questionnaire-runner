import DropdownMandatoryPage from "../../../generated_pages/dropdown_mandatory/dropdown-mandatory.page";
import DropdownMandatorySummary from "../../../generated_pages/dropdown_mandatory/summary.page";
import DropdownMandatoryOverriddenPage from "../../../generated_pages/dropdown_mandatory_with_overridden_error/dropdown-mandatory-with-overridden-error.page";
import DropdownOptionalPage from "../../../generated_pages/dropdown_optional/dropdown-optional.page";
import DropdownOptionalSummary from "../../../generated_pages/dropdown_optional/summary.page";

describe("Component: Dropdown", () => {
  // Mandatory
  describe("Given I start a Mandatory Dropdown survey", () => {
    beforeEach(() => {
      browser.openQuestionnaire("test_dropdown_mandatory.json");
    });

    it("When I have selected a dropdown option, Then the selected option should be displayed in the summary", () => {
      $(DropdownMandatoryPage.answer()).selectByAttribute("value", "Rugby is better!");
      $(DropdownMandatoryPage.submit()).click();
      expect($(DropdownMandatorySummary.dropdownMandatoryAnswer()).getText()).to.contain("Rugby is better!");
    });

    it("When I have not selected a dropdown option and click Continue, Then the default error message should be displayed", () => {
      $(DropdownMandatoryPage.submit()).click();
      expect($(DropdownMandatoryPage.errorNumber(1)).getText()).to.contain("Select an answer");
    });

    it("When I have selected a dropdown option and I try to select a default (disabled) dropdown option, Then the already selected option should be displayed in summary", () => {
      $(DropdownMandatoryPage.answer()).selectByAttribute("value", "Liverpool");
      $(DropdownMandatoryPage.answer()).selectByAttribute("value", "");
      $(DropdownMandatoryPage.submit()).click();
      expect($(DropdownMandatorySummary.dropdownMandatoryAnswer()).getText()).to.contain("Liverpool");
    });

    it("When I click the dropdown label, Then the dropdown should be focused", () => {
      $(DropdownMandatoryPage.answerLabel()).click();
      expect($(DropdownMandatoryPage.answer()).isFocused()).to.be.true;
    });

    it("When I'm on the summary page and I click Edit then Continue, Then the answer on the summary page should be unchanged", () => {
      $(DropdownMandatoryPage.answer()).selectByAttribute("value", "Rugby is better!");
      $(DropdownMandatoryPage.submit()).click();
      expect($(DropdownMandatorySummary.dropdownMandatoryAnswer()).getText()).to.contain("Rugby is better!");
      $(DropdownMandatorySummary.dropdownMandatoryAnswerEdit()).click();
      $(DropdownMandatoryPage.submit()).click();
      expect($(DropdownMandatorySummary.dropdownMandatoryAnswer()).getText()).to.contain("Rugby is better!");
    });

    it("When I'm on the summary page and I click Edit and change the answer, Then the newly selected answer should be displayed in the summary", () => {
      $(DropdownMandatoryPage.answer()).selectByAttribute("value", "Rugby is better!");
      $(DropdownMandatoryPage.submit()).click();
      expect($(DropdownMandatorySummary.dropdownMandatoryAnswer()).getText()).to.contain("Rugby is better!");
      $(DropdownMandatorySummary.dropdownMandatoryAnswerEdit()).click();
      $(DropdownMandatoryPage.submit()).click();
      expect($(DropdownMandatorySummary.dropdownMandatoryAnswer()).getText()).to.contain("Rugby is better!");
      $(DropdownMandatorySummary.dropdownMandatoryAnswerEdit()).click();
      $(DropdownMandatoryPage.answer()).selectByAttribute("value", "Liverpool");
      $(DropdownMandatoryPage.submit()).click();
      expect($(DropdownMandatorySummary.dropdownMandatoryAnswer()).getText()).to.contain("Liverpool");
    });
  });

  describe("Given I start a Mandatory With Overridden Error Dropdown survey", () => {
    before(() => {
      browser.openQuestionnaire("test_dropdown_mandatory_with_overridden_error.json");
    });

    it("When I have not selected a dropdown option and click Continue, Then the overridden error message should be displayed", () => {
      $(DropdownMandatoryOverriddenPage.submit()).click();
      expect($(DropdownMandatoryOverriddenPage.errorNumber(1)).getText()).to.contain("Overridden test error message.");
    });
  });

  // Optional
  describe("Given I start a Optional Dropdown survey", () => {
    beforeEach(() => {
      browser.openQuestionnaire("test_dropdown_optional.json");
    });

    it('When I have not selected a dropdown option, Then the summary should display "No answer provided"', () => {
      $(DropdownOptionalPage.submit()).click();
      expect($(DropdownOptionalSummary.dropdownOptionalAnswer()).getText()).to.contain("No answer provided");
    });

    it("When I have selected a dropdown option, Then the selected option should be displayed in the summary", () => {
      $(DropdownOptionalPage.answer()).selectByAttribute("value", "Rugby is better!");
      $(DropdownOptionalPage.submit()).click();
      expect($(DropdownOptionalSummary.dropdownOptionalAnswer()).getText()).to.contain("Rugby is better!");
    });

    it('When I have selected a dropdown option and I reselect the default option (Select an answer), Then the summary should display "No answer provided"', () => {
      $(DropdownOptionalPage.answer()).selectByAttribute("value", "Chelsea");
      $(DropdownOptionalPage.submit()).click();
      expect($(DropdownOptionalSummary.dropdownOptionalAnswer()).getText()).to.contain("Chelsea");
      $(DropdownOptionalSummary.dropdownOptionalAnswerEdit()).click();
      $(DropdownOptionalPage.answer()).selectByAttribute("value", "");
      $(DropdownOptionalPage.submit()).click();
      expect($(DropdownOptionalSummary.dropdownOptionalAnswer()).getText()).to.contain("No answer provided");
    });
  });
});
