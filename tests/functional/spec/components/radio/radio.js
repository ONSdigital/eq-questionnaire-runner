import RadioMandatoryPage from "../../../generated_pages/radio_mandatory/radio-mandatory.page";
import RadioMandatorySummary from "../../../generated_pages/radio_mandatory/summary.page";

import RadioMandatoryOptionalOtherPage from "../../../generated_pages/radio_mandatory_with_optional_other/radio-mandatory.page";
import RadioMandatoryOptionOtherSummary from "../../../generated_pages/radio_mandatory_with_optional_other/summary.page";

import RadioMandatoryOtherOverriddenPage from "../../../generated_pages/radio_mandatory_with_mandatory_other_overridden_error/radio-mandatory.page";

import RadioMandatoryOverriddenPage from "../../../generated_pages/radio_mandatory_with_overridden_error/radio-mandatory.page";

import RadioNonMandatoryPage from "../../../generated_pages/radio_optional/radio-non-mandatory.page";
import RadioNonMandatorySummary from "../../../generated_pages/radio_optional/summary.page";

import RadioNonMandatoryOtherOverriddenPage from "../../../generated_pages/radio_optional_with_mandatory_other_overridden_error/radio-non-mandatory.page";

import RadioNonMandatoryOtherPage from "../../../generated_pages/radio_optional_with_mandatory_other/radio-non-mandatory.page";
import RadioNonMandatoryOtherSummary from "../../../generated_pages/radio_optional_with_mandatory_other/summary.page";

describe("Component: Radio", () => {
  describe("Given I start a Mandatory Radio survey", () => {
    before(() => {
      browser.openQuestionnaire("test_radio_mandatory.json");
    });

    it("When I have selected a radio option, Then the selected option should be displayed in the summary", () => {
      $(RadioMandatoryPage.coffee()).click();
      $(RadioMandatoryPage.submit()).click();
      expect(browser.getUrl()).to.contain(RadioMandatorySummary.pageName);
      expect($(RadioMandatorySummary.radioMandatoryAnswer()).getText()).to.contain("Coffee");
    });
  });

  describe("Given I start a Mandatory Radio survey  ", () => {
    before(() => {
      browser.openQuestionnaire("test_radio_mandatory.json");
    });

    it("When I have submitted the page without any option, Then the question text is hidden in the error message using a span element", () => {
      $(RadioMandatoryOverriddenPage.submit()).click();
      expect($(RadioMandatoryOverriddenPage.errorNumber(1)).getText()).to.contain("Select an answer\nto ‘What do you prefer for breakfast?’");
    });
  });

  describe("Given I start a Mandatory Radio Other survey", () => {
    before(() => {
      browser.openQuestionnaire("test_radio_mandatory_with_mandatory_other.json");
    });

    it("When I have selected a other text field, Then the selected option should be displayed in the summary", () => {
      $(RadioMandatoryOptionalOtherPage.other()).click();
      $(RadioMandatoryOptionalOtherPage.otherDetail()).setValue("Hello World");
      $(RadioMandatoryOptionalOtherPage.submit()).click();
      expect(browser.getUrl()).to.contain(RadioMandatoryOptionOtherSummary.pageName);
      expect($(RadioMandatoryOptionOtherSummary.radioMandatoryAnswer()).getText()).to.contain("Hello World");
    });
  });

  describe("Given I start a Mandatory Radio Other Overridden Error survey ", () => {
    before(() => {
      browser.openQuestionnaire("test_radio_mandatory_with_mandatory_other_overridden_error.json");
    });

    it("When I submit without any data in the other text field it should Then throw an overridden error", () => {
      $(RadioMandatoryOtherOverriddenPage.other()).click();
      $(RadioMandatoryOtherOverriddenPage.submit()).click();
      expect($(RadioMandatoryOtherOverriddenPage.errorNumber(1)).getText()).to.contain("Test error message is overridden");
    });
  });

  describe("Given I start a Mandatory Radio Other survey ", () => {
    before(() => {
      browser.openQuestionnaire("test_radio_mandatory_with_optional_other.json");
    });

    it("When I submit without any data in the other text field is selected, Then the selected option should be displayed in the summary", () => {
      $(RadioMandatoryOptionalOtherPage.submit()).click();
      expect(browser.getUrl()).to.contain(RadioMandatoryOptionOtherSummary.pageName);
      expect($(RadioMandatoryOptionOtherSummary.radioMandatoryAnswer()).getText()).to.contain("No answer provided");
    });
  });

  describe("Given I start a Mandatory Radio Other Overridden error survey  ", () => {
    before(() => {
      browser.openQuestionnaire("test_radio_mandatory_with_overridden_error.json");
    });

    it("When I have submitted the page without any option, Then an overridden error is displayed", () => {
      $(RadioMandatoryOverriddenPage.submit()).click();
      expect($(RadioMandatoryOverriddenPage.errorNumber(1)).getText()).to.contain("Test error message is overridden");
    });
  });

  describe("Given I start a Optional survey", () => {
    before(() => {
      browser.openQuestionnaire("test_radio_optional.json");
    });

    it("When I have selected no option, Then the selected option should be displayed in the summary", () => {
      $(RadioNonMandatoryPage.submit()).click();
      expect(browser.getUrl()).to.contain(RadioNonMandatorySummary.pageName);
      expect($(RadioNonMandatorySummary.radioNonMandatoryAnswer()).getText()).to.contain("No answer provided");
    });
  });

  describe("Given I start a Optional Other Overridden error survey", () => {
    before(() => {
      browser.openQuestionnaire("test_radio_optional_with_mandatory_other_overridden_error.json");
    });

    it("When I have submitted an other option with an empty text field, Then an overridden error is displayed", () => {
      $(RadioNonMandatoryOtherOverriddenPage.other()).click();
      $(RadioNonMandatoryOtherOverriddenPage.submit()).click();
      expect($(RadioNonMandatoryOtherOverriddenPage.errorNumber(1)).getText()).to.contain("Test error message is overridden");
    });
  });

  describe("Given I Start a Optional Mandatory Other survey", () => {
    before(() => {
      browser.openQuestionnaire("test_radio_optional_with_mandatory_other.json");
    });

    it("When I submit data in the other text field it should be persisted and Then displayed on the summary", () => {
      $(RadioNonMandatoryOtherPage.other()).click();
      $(RadioNonMandatoryOtherPage.otherDetail()).setValue("Hello World");
      $(RadioNonMandatoryOtherPage.submit()).click();
      expect(browser.getUrl()).to.contain(RadioNonMandatoryOtherSummary.pageName);
      expect($(RadioNonMandatoryOtherSummary.radioNonMandatoryAnswer()).getText()).to.contain("Hello World");
    });
  });
});
