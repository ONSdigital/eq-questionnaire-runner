import HubPage from "../../../base_pages/hub.page";
import IntroductionBlockPage from "../../../generated_pages/supplementary_data_all_variations/introduction-block.page.js";
import Section1Page from "../../../generated_pages/supplementary_data_all_variations/section-1-summary.page.js";
import EmailBlockPage from "../../../generated_pages/supplementary_data_all_variations/email-block.page.js";
import NewEmailPage from "../../../generated_pages/supplementary_data_all_variations/new-email.page.js";
import SalesBreakdownBlockPage from "../../../generated_pages/supplementary_data_all_variations/sales-breakdown-block.page.js";
import CalculatedSummarySalesPage from "../../../generated_pages/supplementary_data_all_variations/calculated-summary-sales.page.js";
import Section1InterstitialPage from "../../../generated_pages/supplementary_data_all_variations/section-1-interstitial.page.js";
import TradingPage from "../../../generated_pages/supplementary_data_all_variations/trading.page";
import ListCollectorPage from "../../../generated_pages/supplementary_data_all_variations/list-collector.page";
import AnyEmployeesPage from "../../../generated_pages/supplementary_data_all_variations/any-employees.page";
import Section2Page from "../../../generated_pages/supplementary_data_all_variations/section-2-summary.page.js";
import AddEmployeePage from "../../../generated_pages/supplementary_data_all_variations/list-collector-add.page.js";
import Section3Page from "../../../generated_pages/supplementary_data_all_variations/section-3-summary.page.js";
import LengthOfEmploymentPage from "../../../generated_pages/supplementary_data_all_variations/length-of-employment.page.js";
import SupermarketTransportPage from "../../../generated_pages/new_calculated_summary_repeating_and_static_answers/supermarket-transport.page";

describe("Using supplementary data non list items", () => {
  before("Starting the survey", async () => {
    await browser.openQuestionnaire("test_supplementary_data_all_variations.json", {
      version: "v2",
      sdsDatasetId: "c067f6de-6d64-42b1-8b02-431a3486c178",
    });
  });

  it("Given I launch a survey using supplementary data, When I begin the introduction block, Then I see the supplementary data piped in", async () => {
    await expect(await $(IntroductionBlockPage.businessDetailsContent()).getText()).to.contain("You are completing this survey for Tesco");
    await expect(await $(IntroductionBlockPage.businessDetailsContent()).getText()).to.contain(
      "If the company details or structure have changed contact us on 01171231231"
    );
    await expect(await $(IntroductionBlockPage.guidancePanel(1)).getText()).to.contain("Some supplementary guidance about the survey");
    await $(IntroductionBlockPage.submit()).click();
    await $(HubPage.submit()).click();
    await $(EmailBlockPage.yes()).click();
    await $(EmailBlockPage.submit()).click();
  });

  it("Given I have dynamic answer options based of a supplementary date value, When I reach the block on trading start date, Then I see a correct list of options to choose from", async () => {
    await expect(await $(TradingPage.answerLabelByIndex(0)).getText()).to.equal("Thursday 27 November 1947");
    await expect(await $(TradingPage.answerLabelByIndex(1)).getText()).to.equal("Friday 28 November 1947");
    await expect(await $(TradingPage.answerLabelByIndex(2)).getText()).to.equal("Saturday 29 November 1947");
    await expect(await $(TradingPage.answerLabelByIndex(3)).getText()).to.equal("Sunday 30 November 1947");
    await expect(await $(TradingPage.answerLabelByIndex(4)).getText()).to.equal("Monday 1 December 1947");
    await expect(await $(TradingPage.answerLabelByIndex(5)).getText()).to.equal("Tuesday 2 December 1947");
    await expect(await $(TradingPage.answerLabelByIndex(6)).getText()).to.equal("Wednesday 3 December 1947");
    await $(TradingPage.answerByIndex(3)).click();
    await $(TradingPage.submit()).click();
  });

  it("Given I have answers with a sum validated against a supplementary data value, When I enter a breakdown that exceeds the total, Then I see an error message", async () => {
    await $(SalesBreakdownBlockPage.salesBristol()).setValue(333000);
    await $(SalesBreakdownBlockPage.salesLondon()).setValue(444000);
    await $(SalesBreakdownBlockPage.submit()).click();
    await expect(await $(SalesBreakdownBlockPage.errorNumber(1)).getText()).to.contain("Enter answers that add up to or are less than 555,000");
  });

  it("Given I have answers with a sum validated against a supplementary data value, When I enter a breakdown less than the total, Then I see a calculated summary page with the sum of my previous answers", async () => {
    await $(SalesBreakdownBlockPage.salesLondon()).setValue(111000);
    await $(SalesBreakdownBlockPage.submit()).click();
    await expect(await $(CalculatedSummarySalesPage.calculatedSummaryTitle()).getText()).to.contain(
      "Total value of sales from Bristol and London is calculated to be £444,000.00. Is this correct?"
    );
  });

  it("Given I have an interstitial block with all answers and supplementary data, When I reach this block, Then I see the placeholders rendered correctly", async () => {
    await $(CalculatedSummarySalesPage.submit()).click();
    await expect(await $(Section1InterstitialPage.questionText()).getText()).to.contain("Summary of information provided for Tesco");
    await expect(await $("body").getText()).to.have.string("Telephone Number: 01171231231");
    await expect(await $("body").getText()).to.have.string("Email: contact@tesco.org");
    await expect(await $("body").getText()).to.have.string("Note Title: Value of total sales");
    await expect(await $("body").getText()).to.have.string("Note Description: Total value of goods sold during the period of the return");
    await expect(await $("body").getText()).to.have.string("Note Example Title: Including");
    await expect(await $("body").getText()).to.have.string("Note Example Description: Sales across all UK stores");
    await expect(await $("body").getText()).to.have.string("Incorporation Date: 27 November 1947");
    await expect(await $("body").getText()).to.have.string("Trading start date: 30 November 1947");
    await expect(await $("body").getText()).to.have.string("Guidance: Some supplementary guidance about the survey");
    await expect(await $("body").getText()).to.have.string("Total Uk Sales: £555,000.00");
    await expect(await $("body").getText()).to.have.string("Bristol sales: £333,000.00");
    await expect(await $("body").getText()).to.have.string("London sales: £111,000.00");
    await expect(await $("body").getText()).to.have.string("Sum of Bristol and London sales: £444,000.00");
    await $(Section1InterstitialPage.submit()).click();
  });

  it("Given I change the email for the company, When I return to the interstitial block, Then I see the email has updated", async () => {
    await $(Section1Page.sameEmailAnswerEdit()).click();
    await $(EmailBlockPage.no()).click();
    await $(EmailBlockPage.submit()).click();
    await $(NewEmailPage.answer()).setValue("new@tesco.com");
    await $(NewEmailPage.submit()).click();
    await $(Section1Page.previous()).click();
    await expect(await $("body").getText()).to.have.string("Email: new@tesco.com");
    await $(Section1InterstitialPage.submit()).click();
    await $(Section1Page.submit()).click();
  });

  it("Given I add some employees via a list collector, When I begin a repeating section for that employee, Then I see static supplementary data piped in correctly", async () => {
    await $(HubPage.submit()).click();
    await $(AnyEmployeesPage.yes()).click();
    await $(AnyEmployeesPage.submit()).click();
    await $(AddEmployeePage.employeeFirstName()).setValue("Jane");
    await $(AddEmployeePage.employeeLastName()).setValue("Doe");
    await $(AddEmployeePage.submit()).click();
    await $(ListCollectorPage.yes()).click();
    await $(ListCollectorPage.submit()).click();
    await $(AddEmployeePage.employeeFirstName()).setValue("John");
    await $(AddEmployeePage.employeeLastName()).setValue("Smith");
    await $(AddEmployeePage.submit()).click();
    await $(ListCollectorPage.no()).click();
    await $(ListCollectorPage.submit()).click();
    await $(Section2Page.submit()).click();
    await $(HubPage.submit()).click();
    await expect(await $(LengthOfEmploymentPage.questionTitle()).getText()).to.contain("When did Jane Doe start working for Tesco?");
    await expect(await $(LengthOfEmploymentPage.employmentStartLegend()).getText()).to.contain("Start date at Tesco");
  });

  it("Given I have validation on the start date in the repeating section, When I enter a date before the incorporation date, Then I see an error message", async () => {
    await $(LengthOfEmploymentPage.day()).setValue(1);
    await $(LengthOfEmploymentPage.month()).setValue(1);
    await $(LengthOfEmploymentPage.year()).setValue(1930);
    await $(LengthOfEmploymentPage.submit()).click();
    await expect(await $(SupermarketTransportPage.singleErrorLink()).getText()).to.contain("Enter a date after 26 November 1947");
  });

  it("Given I have validation on the start date in the repeating section, When I enter a date after the incorporation date, Then I see that date on the summary page for the section", async () => {
    await $(LengthOfEmploymentPage.year()).setValue(1990);
    await $(LengthOfEmploymentPage.submit()).click();
    await expect(await $(Section3Page.lengthEmploymentQuestion()).getText()).to.contain("When did Jane Doe start working for Tesco?");
    await expect(await $(Section3Page.employmentStart()).getText()).to.contain("1 January 1990");
  });
});
