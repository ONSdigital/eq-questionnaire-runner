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
import { click } from "../../../helpers";
describe("Component: Radio", () => {
  describe("Given I start a Mandatory Radio survey", () => {
    before(async () => {
      await browser.openQuestionnaire("test_radio_mandatory.json");
    });

    it("When I have selected a radio option that contains an escaped character, Then the selected option should be displayed in the summary", async () => {
      await $(RadioMandatoryPage.teaCoffee()).click();
      await click(RadioMandatoryPage.submit());
      await expect(browser).toHaveUrlContaining(RadioMandatorySummary.pageName);
      await expect(await $(RadioMandatorySummary.radioMandatoryAnswer()).getText()).toBe("Tea & Coffee");
    });
  });

  describe("Given I start a Mandatory Radio survey", () => {
    before(async () => {
      await browser.openQuestionnaire("test_radio_mandatory.json");
    });

    it("When I have selected a radio option, Then the selected option should be displayed in the summary", async () => {
      await $(RadioMandatoryPage.coffee()).click();
      await click(RadioMandatoryPage.submit());
      await expect(browser).toHaveUrlContaining(RadioMandatorySummary.pageName);
      await expect(await $(RadioMandatorySummary.radioMandatoryAnswer()).getText()).toBe("Coffee");
    });
  });

  describe("Given I start a Mandatory Radio survey  ", () => {
    before(async () => {
      await browser.openQuestionnaire("test_radio_mandatory.json");
    });

    it("When I have submitted the page without any option, Then the question text is hidden in the error message using a span element", async () => {
      await click(RadioMandatoryOverriddenPage.submit());
      await expect(await $(RadioMandatoryOverriddenPage.errorNumber(1)).getHTML()).toContain(
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
      await click(RadioMandatoryOptionalDetailAnswerPage.submit());
      await expect(browser).toHaveUrlContaining(RadioMandatoryOptionDetailAnswerSummary.pageName);
      await expect(
        await $(RadioMandatoryOptionDetailAnswerSummary.radioMandatoryAnswer()).getText()
      ).toContain("Hello World");
    });
  });

  describe("Given I start a Mandatory Radio DetailAnswer Overridden Error survey ", () => {
    before(async () => {
      await browser.openQuestionnaire("test_radio_mandatory_with_detail_answer_mandatory_with_overridden_error.json");
    });

    it("When I submit without any data in the other text field it should Then throw an overridden error", async () => {
      await $(RadioMandatoryDetailAnswerOverriddenPage.other()).click();
      await click(RadioMandatoryDetailAnswerOverriddenPage.submit());
      await expect(await $(RadioMandatoryDetailAnswerOverriddenPage.errorNumber(1)).getText()).toBe("Test error message is overridden");
    });
  });

  describe("Given I start a Mandatory Radio DetailAnswer survey ", () => {
    before(async () => {
      await browser.openQuestionnaire("test_radio_mandatory_with_detail_answer_optional.json");
    });

    it("When I submit without any data in the other text field is selected, Then the selected option should be displayed in the summary", async () => {
      await click(RadioMandatoryOptionalDetailAnswerPage.submit());
      await expect(browser).toHaveUrlContaining(RadioMandatoryOptionDetailAnswerSummary.pageName);
      await expect(
        await $(RadioMandatoryOptionDetailAnswerSummary.radioMandatoryAnswer()).getText()
      ).toContain("No answer provided");
    });
  });

  describe("Given I start a Mandatory Radio DetailAnswer Overridden error survey  ", () => {
    before(async () => {
      await browser.openQuestionnaire("test_radio_mandatory_with_overridden_error.json");
    });

    it("When I have submitted the page without any option, Then an overridden error is displayed", async () => {
      await click(RadioMandatoryOverriddenPage.submit());
      await expect(await $(RadioMandatoryOverriddenPage.errorNumber(1)).getText()).toBe("Test error message is overridden");
    });
  });

  describe("Given I start a Optional survey", () => {
    before(async () => {
      await browser.openQuestionnaire("test_radio_optional.json");
    });

    it("When I have selected no option, Then the selected option should be displayed in the summary", async () => {
      await click(RadioNonMandatoryPage.submit());
      await expect(browser).toHaveUrlContaining(RadioNonMandatorySummary.pageName);
      await expect(await $(RadioNonMandatorySummary.radioNonMandatoryAnswer()).getText()).toBe("No answer provided");
    });
  });

  describe("Given I start a Optional DetailAnswer Overridden error survey", () => {
    before(async () => {
      await browser.openQuestionnaire("test_radio_optional_with_detail_answer_mandatory_with_overridden_error.json");
    });

    it("When I have submitted an other option with an empty text field, Then an overridden error is displayed", async () => {
      await $(RadioNonMandatoryDetailAnswerOverriddenPage.other()).click();
      await click(RadioNonMandatoryDetailAnswerOverriddenPage.submit());
      await expect(
        await $(RadioNonMandatoryDetailAnswerOverriddenPage.errorNumber(1)).getText()
      ).toBe("Test error message is overridden");
    });
  });

  describe("Given I Start a Optional Mandatory DetailAnswer survey", () => {
    before(async () => {
      await browser.openQuestionnaire("test_radio_optional_with_detail_answer_mandatory.json");
    });

    it("When I submit data in the other text field it should be persisted and Then displayed on the summary", async () => {
      await $(RadioNonMandatoryDetailAnswerPage.other()).click();
      await $(RadioNonMandatoryDetailAnswerPage.otherDetail()).setValue("Hello World");
      await click(RadioNonMandatoryDetailAnswerPage.submit());
      await expect(browser).toHaveUrlContaining(RadioNonMandatoryDetailAnswerSummary.pageName);
      await expect(
        await $(RadioNonMandatoryDetailAnswerSummary.radioNonMandatoryAnswer()).getText()
      ).toContain("Hello World");
    });
  });
});
