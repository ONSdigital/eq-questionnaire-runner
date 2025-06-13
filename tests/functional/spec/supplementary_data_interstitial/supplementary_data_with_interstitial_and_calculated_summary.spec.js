import { click, assertSummaryTitles } from "../../helpers";
import { expect } from "@wdio/globals";
import { getRandomString } from "../../jwt_helper";
import CalculatedSummarySalesPage from "../../generated_pages/supplementary_data_with_interstitial_and_calculated_summary/calculated-summary-sales.page.js";
import EmailBlockPage from "../../generated_pages/supplementary_data_with_interstitial_and_calculated_summary/email-block.page.js";
import HubPage from "../../base_pages/hub.page";
import IntroductionBlockPage from "../../generated_pages/supplementary_data_with_interstitial_and_calculated_summary/introduction-block.page.js";
import LoadedSuccessfullyBlockPage from "../../generated_pages/supplementary_data_with_interstitial_and_calculated_summary/loaded-successfully-block.page.js";
import NewEmailPage from "../../generated_pages/supplementary_data_with_interstitial_and_calculated_summary/new-email.page.js";
import SalesBreakdownBlockPage from "../../generated_pages/supplementary_data_with_interstitial_and_calculated_summary/sales-breakdown-block.page.js";
import Section1InterstitialPage from "../../generated_pages/supplementary_data_with_interstitial_and_calculated_summary/section-1-interstitial.page.js";
import Section1Page from "../../generated_pages/supplementary_data_with_interstitial_and_calculated_summary/section-1-summary.page.js";
import TradingPage from "../../generated_pages/supplementary_data_with_interstitial_and_calculated_summary/trading.page.js";
import ThankYouPage from "../../base_pages/thank-you.page";
import ViewSubmittedResponsePage from "../../generated_pages/supplementary_data_with_interstitial_and_calculated_summary/view-submitted-response.page.js";

describe("Using supplementary data", () => {
  const responseId = getRandomString(16);
  const summaryRowTitles = ".ons-summary__row-title";

  before("Starting the survey", async () => {
    await browser.openQuestionnaire("test_supplementary_data_with_interstitial_and_calculated_summary.json", {
      version: "v2",
      sdsDatasetId: "203b2f9d-c500-8175-98db-86ffcfdccfa3",
      responseId,
    });
  });
  it("Given I launch a survey using supplementary data, When I am outside a repeating section, Then I am able to see the list of items relating to a given supplementary data list item on the page", async () => {
    await expect(await $("#main-content #guidance-1").getText()).toContain("The surnames of the employees are: Potter, Kent.");
    await expect(await $$("#main-content li")[0].getText()).toBe("Articles and equipment for sports or outdoor games");
    await expect(await $$("#main-content li")[1].getText()).toBe("Kitchen Equipment");
  });

  it("Given I progress through the interstitial block, When I begin the introduction block, Then I see the supplementary data piped in", async () => {
    await click(LoadedSuccessfullyBlockPage.submit());
    await $(IntroductionBlockPage.acceptCookies()).click();
    await expect(await $(IntroductionBlockPage.businessDetailsContent()).getText()).toContain("You are completing this survey for Tesco");
    await expect(await $(IntroductionBlockPage.businessDetailsContent()).getText()).toContain(
      "If the company details or structure have changed contact us on 01171231231",
    );
    await expect(await $(IntroductionBlockPage.guidancePanel(1)).getText()).toContain("Some supplementary guidance about the survey");
    await click(IntroductionBlockPage.submit());
    await click(HubPage.submit());
    await $(EmailBlockPage.yes()).click();
    await click(EmailBlockPage.submit());
  });

  it("Given I have dynamic answer options based off a supplementary date value, When I reach the block using them, Then I see a correct list of options to choose from", async () => {
    await expect(await $(TradingPage.answerLabelByIndex(0)).getText()).toBe("Thursday 27 November 1947");
    await expect(await $(TradingPage.answerLabelByIndex(1)).getText()).toBe("Friday 28 November 1947");
    await expect(await $(TradingPage.answerLabelByIndex(2)).getText()).toBe("Saturday 29 November 1947");
    await expect(await $(TradingPage.answerLabelByIndex(3)).getText()).toBe("Sunday 30 November 1947");
    await expect(await $(TradingPage.answerLabelByIndex(4)).getText()).toBe("Monday 1 December 1947");
    await expect(await $(TradingPage.answerLabelByIndex(5)).getText()).toBe("Tuesday 2 December 1947");
    await expect(await $(TradingPage.answerLabelByIndex(6)).getText()).toBe("Wednesday 3 December 1947");
    await $(TradingPage.answerByIndex(3)).click();
    await click(TradingPage.submit());
  });

  it("Given I have a calculated question validated against a supplementary data value, When I enter a breakdown that exceeds the total, Then I see an error message", async () => {
    await $(SalesBreakdownBlockPage.salesBristol()).setValue(333000);
    await $(SalesBreakdownBlockPage.salesLondon()).setValue(444000);
    await click(SalesBreakdownBlockPage.submit());
    await expect(await $(SalesBreakdownBlockPage.errorNumber(1)).getText()).toContain("Enter answers that add up to or are less than 555,000");
  });

  it("Given I have a calculated question validated against a supplementary data value, When I enter a breakdown less than the total, Then I see a calculated summary page with the sum of my previous answers", async () => {
    await $(SalesBreakdownBlockPage.salesLondon()).setValue(111000);
    await click(SalesBreakdownBlockPage.submit());
    await expect(await $(CalculatedSummarySalesPage.calculatedSummaryTitle()).getText()).toBe(
      "Total value of sales from Bristol and London is calculated to be £444,000.00. Is this correct?",
    );
  });

  it("Given I have an interstitial block with all answers and supplementary data, When I reach this block, Then I see the placeholders rendered correctly", async () => {
    await click(CalculatedSummarySalesPage.submit());
    await expect(await $(Section1InterstitialPage.questionText()).getText()).toContain("Summary of information provided for Tesco");
    await expect(await $("body").getText()).toContain("Telephone Number: 01171231231");
    await expect(await $("body").getText()).toContain("Email: contact@tesco.org");
    await expect(await $("body").getText()).toContain("Note Title: Value of total sales");
    await expect(await $("body").getText()).toContain("Note Description: Total value of goods sold during the period of the return");
    await expect(await $("body").getText()).toContain("Note Example Title: Including");
    await expect(await $("body").getText()).toContain("Note Example Description: Sales across all UK stores");
    await expect(await $("body").getText()).toContain("Incorporation Date: 27 November 1947");
    await expect(await $("body").getText()).toContain("Trading start date: 30 November 1947");
    await expect(await $("body").getText()).toContain("Guidance: Some supplementary guidance about the survey");
    await expect(await $("body").getText()).toContain("Total Uk Sales: £555,000.00");
    await expect(await $("body").getText()).toContain("Bristol sales: £333,000.00");
    await expect(await $("body").getText()).toContain("London sales: £111,000.00");
    await expect(await $("body").getText()).toContain("Sum of Bristol and London sales: £444,000.00");
  });

  it("Given I have a section summary enabled, When I reach the section summary, Then I see it rendered correctly with supplementary data", async () => {
    await click(Section1InterstitialPage.submit());
    await expect(await $(Section1Page.emailQuestion()).getText()).toBe("Is contact@tesco.org still the correct contact email for Tesco?");
    await expect(await $(Section1Page.sameEmailAnswer()).getText()).toBe("Yes");
    await expect(await $(Section1Page.tradingQuestion()).getText()).toBe("When did Tesco begin trading?");
    await expect(await $(Section1Page.tradingAnswer()).getText()).toBe("Sunday 30 November 1947");
    await expect(await $$(summaryRowTitles)[0].getText()).toBe("How much of the £555,000.00 total UK sales was from Bristol and London?");
    await expect(await $(Section1Page.salesBristolAnswer()).getText()).toBe("£333,000.00");
    await expect(await $(Section1Page.salesLondonAnswer()).getText()).toBe("£111,000.00");
  });

  it("Given I add an answer used in a first non empty item transform with supplementary data, When I return to the interstitial block, Then I see the transform value has updated", async () => {
    await $(Section1Page.sameEmailAnswerEdit()).click();
    await $(EmailBlockPage.no()).click();
    await click(EmailBlockPage.submit());
    await $(NewEmailPage.answer()).setValue("new.contact@gmail.com");
    await click(NewEmailPage.submit());
    await $(Section1Page.previous()).click();
    await expect(await $("body").getText()).toContain("Email: new.contact@gmail.com");
    await click(Section1InterstitialPage.submit());
    await click(Section1Page.submit());
  });
  it("Given I can view my response after submission, When I submit the survey, Then I see the values I've entered and correct rendering with supplementary data", async () => {
    await browser.openQuestionnaire("test_supplementary_data_with_interstitial_and_calculated_summary.json", {
      version: "v2",
      sdsDatasetId: "3bb41d29-4daa-9520-82f0-cae365f390c6",
      responseId,
    });
    await click(HubPage.submit());
    await $(ThankYouPage.savePrintAnswersLink()).click();
    await assertSummaryTitles(["Company Details"]);

    // Company details
    await expect(await $(ViewSubmittedResponsePage.emailQuestion()).getText()).toBe("Is contact@lidl.org still the correct contact email for Lidl?");
    await expect(await $(ViewSubmittedResponsePage.sameEmailAnswer()).getText()).toBe("No");
    await expect(await $(ViewSubmittedResponsePage.newEmailQuestion()).getText()).toBe("What is the new contact email for Lidl?");
    await expect(await $(ViewSubmittedResponsePage.newEmailAnswer()).getText()).toBe("new.contact@gmail.com");
    await expect(await $(ViewSubmittedResponsePage.tradingQuestion()).getText()).toBe("When did Lidl begin trading?");
    await expect(await $(ViewSubmittedResponsePage.tradingAnswer()).getText()).toBe("Sunday 30 November 1947");
    await expect(await $$(summaryRowTitles)[0].getText()).toBe("How much of the £555,000.00 total UK sales was from Bristol and London?");
    await expect(await $(ViewSubmittedResponsePage.salesBristolAnswer()).getText()).toBe("£333,000.00");
    await expect(await $(ViewSubmittedResponsePage.salesLondonAnswer()).getText()).toBe("£111,000.00");
  });
});
