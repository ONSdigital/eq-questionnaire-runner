import RadioMandatoryPage from "../../../generated_pages/radio_mandatory/radio-mandatory.page";
import RadioMandatorySummary from "../../../generated_pages/radio_mandatory/submit.page";

import RadioMandatoryOptionalDetailAnswerPage from "../../../generated_pages/radio_mandatory_with_detail_answer_optional/radio-mandatory.page";
import RadioMandatoryOptionDetailAnswerSummary from "../../../generated_pages/radio_mandatory_with_detail_answer_optional/submit.page";

import RadioMandatoryDetailAnswerOverriddenPage from "../../../generated_pages/radio_mandatory_with_detail_answer_mandatory_with_overridden_error/radio-mandatory.page";

import RadioMandatoryOverriddenPage from "../../../generated_pages/radio_mandatory_with_overridden_error/radio-mandatory.page";

import RadioNonMandatoryPage from "../../../generated_pages/radio_optional/radio-non-mandatory.page";
import RadioNonMandatorySummary from "../../../generated_pages/radio_optional/submit.page";

import RadioNonMandatoryDetailAnswerOverriddenPage from "../../../generated_pages/radio_optional_with_detail_answer_mandatory_with_overridden_error/radio-non-mandatory.page";

import RadioNonMandatoryDetailAnswerPage from "../../../generated_pages/radio_optional_with_detail_answer_mandatory/radio-non-mandatory.page";
import RadioNonMandatoryDetailAnswerSummary from "../../../generated_pages/radio_optional_with_detail_answer_mandatory/submit.page";

describe("Component: Radio", () => {
  describe("Given I start a Mandatory Radio survey", () => {
    before(async () => {
      await browser.openQuestionnaire("test_radio_mandatory.json");
    });

    it("When I have selected a radio option that contains an escaped character, Then the selected option should be displayed in the summary", async () => {
      await $(RadioMandatoryPage.teaCoffee()).click();
      await $(RadioMandatoryPage.submit()).click();
      await expect(await browser.getUrl()).to.contain(RadioMandatorySummary.pageName);
      await expect(await $(RadioMandatorySummary.radioMandatoryAnswer()).getText()).to.contain("Tea & Coffee");
    });
  });

  describe("Given I start a Mandatory Radio survey", () => {
    before(async () => {
      await browser.openQuestionnaire("test_radio_mandatory.json");
    });

    it("When I have selected a radio option, Then the selected option should be displayed in the summary", async () => {
      await $(RadioMandatoryPage.coffee()).click();
      await $(RadioMandatoryPage.submit()).click();
      await expect(await browser.getUrl()).to.contain(RadioMandatorySummary.pageName);
      await expect(await $(RadioMandatorySummary.radioMandatoryAnswer()).getText()).to.contain("Coffee");
    });
  });

  describe("Given I start a Mandatory Radio survey  ", () => {
    before(async () => {
      await browser.openQuestionnaire("test_radio_mandatory.json");
    });

    it("When I have submitted the page without any option, Then the question text is hidden in the error message using a span element", async () => {
      await $(RadioMandatoryOverriddenPage.submit()).click();
      await expect(await $(RadioMandatoryOverriddenPage.errorNumber(1)).getHTML()).to.contain(
        'Select an answer <span class="ons-u-vh">to ‘What do you prefer for breakfast?’</span></a>'
      );
    });
  });

  describe("Given I start a Mandatory Radio DetailAnswer survey", () => {
    before(async () => {
      await browser.openQuestionnaire("test_radio_mandatory_with_detail_answer_mandatory.json");
    });

    it("When I have selected a other text field, Then the selected option should be displayed in the summary", async () => {
      await $(RadioMandatoryOptionalDetailAnswerPage.other()).click();
      await $(RadioMandatoryOptionalDetailAnswerPage.otherDetail()).setValue("Hello World");
      await $(RadioMandatoryOptionalDetailAnswerPage.submit()).click();
      await expect(await browser.getUrl()).to.contain(RadioMandatoryOptionDetailAnswerSummary.pageName);
      await expect(await $(RadioMandatoryOptionDetailAnswerSummary.radioMandatoryAnswer()).getText()).to.contain("Hello World");
    });
  });

  describe("Given I start a Mandatory Radio DetailAnswer Overridden Error survey ", () => {
    before(async () => {
      await browser.openQuestionnaire("test_radio_mandatory_with_detail_answer_mandatory_with_overridden_error.json");
    });

    it("When I submit without any data in the other text field it should Then throw an overridden error", async () => {
      await $(RadioMandatoryDetailAnswerOverriddenPage.other()).click();
      await $(RadioMandatoryDetailAnswerOverriddenPage.submit()).click();
      await expect(await $(RadioMandatoryDetailAnswerOverriddenPage.errorNumber(1)).getText()).to.contain("Test error message is overridden");
    });
  });

  describe("Given I start a Mandatory Radio DetailAnswer survey ", () => {
    before(async () => {
      await browser.openQuestionnaire("test_radio_mandatory_with_detail_answer_optional.json");
    });

    it("When I submit without any data in the other text field is selected, Then the selected option should be displayed in the summary", async () => {
      await $(RadioMandatoryOptionalDetailAnswerPage.submit()).click();
      await expect(await browser.getUrl()).to.contain(RadioMandatoryOptionDetailAnswerSummary.pageName);
      await expect(await $(RadioMandatoryOptionDetailAnswerSummary.radioMandatoryAnswer()).getText()).to.contain("No answer provided");
    });
  });

  describe("Given I start a Mandatory Radio DetailAnswer Overridden error survey  ", () => {
    before(async () => {
      await browser.openQuestionnaire("test_radio_mandatory_with_overridden_error.json");
    });

    it("When I have submitted the page without any option, Then an overridden error is displayed", async () => {
      await $(RadioMandatoryOverriddenPage.submit()).click();
      await expect(await $(RadioMandatoryOverriddenPage.errorNumber(1)).getText()).to.contain("Test error message is overridden");
    });
  });

  describe("Given I start a Optional survey", () => {
    before(async () => {
      await browser.openQuestionnaire("test_radio_optional.json");
    });

    it("When I have selected no option, Then the selected option should be displayed in the summary", async () => {
      await $(RadioNonMandatoryPage.submit()).click();
      await expect(await browser.getUrl()).to.contain(RadioNonMandatorySummary.pageName);
      await expect(await $(RadioNonMandatorySummary.radioNonMandatoryAnswer()).getText()).to.contain("No answer provided");
    });
  });

  describe("Given I start a Optional DetailAnswer Overridden error survey", () => {
    before(async () => {
      await browser.openQuestionnaire("test_radio_optional_with_detail_answer_mandatory_with_overridden_error.json");
    });

    it("When I have submitted an other option with an empty text field, Then an overridden error is displayed", async () => {
      await $(RadioNonMandatoryDetailAnswerOverriddenPage.other()).click();
      await $(RadioNonMandatoryDetailAnswerOverriddenPage.submit()).click();
      await expect(await $(RadioNonMandatoryDetailAnswerOverriddenPage.errorNumber(1)).getText()).to.contain("Test error message is overridden");
    });
  });

  describe("Given I Start a Optional Mandatory DetailAnswer survey", () => {
    before(async () => {
      await browser.openQuestionnaire("test_radio_optional_with_detail_answer_mandatory.json");
    });

    it("When I submit data in the other text field it should be persisted and Then displayed on the summary", async () => {
      await $(RadioNonMandatoryDetailAnswerPage.other()).click();
      await $(RadioNonMandatoryDetailAnswerPage.otherDetail()).setValue("Hello World");
      await $(RadioNonMandatoryDetailAnswerPage.submit()).click();
      await expect(await browser.getUrl()).to.contain(RadioNonMandatoryDetailAnswerSummary.pageName);
      await expect(await $(RadioNonMandatoryDetailAnswerSummary.radioNonMandatoryAnswer()).getText()).to.contain("Hello World");
    });
  });
});
