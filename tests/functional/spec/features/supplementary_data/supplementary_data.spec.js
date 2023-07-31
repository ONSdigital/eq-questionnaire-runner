import AddAdditionalEmployeePage from "../../../generated_pages/supplementary_data/list-collector-additional-add.page.js";
import AdditionalLengthOfEmploymentPage from "../../../generated_pages/supplementary_data/additional-length-of-employment.page.js";
import AnyAdditionalEmployeesPage from "../../../generated_pages/supplementary_data/any-additional-employees.page.js";
import CalculatedSummarySalesPage from "../../../generated_pages/supplementary_data/calculated-summary-sales.page.js";
import CalculatedSummaryValueSalesPage from "../../../generated_pages/supplementary_data/calculated-summary-value-sales.page.js";
import CalculatedSummaryVolumeSalesPage from "../../../generated_pages/supplementary_data/calculated-summary-volume-sales.page.js";
import CalculatedSummaryVolumeTotalPage from "../../../generated_pages/supplementary_data/calculated-summary-volume-total.page.js";
import DynamicProductsPage from "../../../generated_pages/supplementary_data/dynamic-products.page.js";
import EmailBlockPage from "../../../generated_pages/supplementary_data/email-block.page.js";
import HubPage from "../../../base_pages/hub.page";
import IntroductionBlockPage from "../../../generated_pages/supplementary_data/introduction-block.page.js";
import LengthOfEmploymentPage from "../../../generated_pages/supplementary_data/length-of-employment.page.js";
import ListCollectorAdditionalPage from "../../../generated_pages/supplementary_data/list-collector-additional.page.js";
import ListCollectorEmployeesPage from "../../../generated_pages/supplementary_data/list-collector-employees.page.js";
import ListCollectorProductsPage from "../../../generated_pages/supplementary_data/list-collector-products.page.js";
import LoadedSuccessfullyBlockPage from "../../../generated_pages/supplementary_data/loaded-successfully-block.page.js";
import NewEmailPage from "../../../generated_pages/supplementary_data/new-email.page.js";
import ProductRepeatingBlock1Page from "../../../generated_pages/supplementary_data/product-repeating-block-1-repeating-block.page.js";
import SalesBreakdownBlockPage from "../../../generated_pages/supplementary_data/sales-breakdown-block.page.js";
import Section1InterstitialPage from "../../../generated_pages/supplementary_data/section-1-interstitial.page.js";
import Section1Page from "../../../generated_pages/supplementary_data/section-1-summary.page.js";
import Section2Page from "../../../generated_pages/supplementary_data/section-2-summary.page.js";
import Section3Page from "../../../generated_pages/supplementary_data/section-3-summary.page.js";
import Section4Page from "../../../generated_pages/supplementary_data/section-4-summary.page.js";
import Section5Page from "../../../generated_pages/supplementary_data/section-5-summary.page.js";
import Section6Page from "../../../generated_pages/supplementary_data/section-6-summary.page.js";
import ThankYouPage from "../../../base_pages/thank-you.page";
import TradingPage from "../../../generated_pages/supplementary_data/trading.page.js";
import ViewSubmittedResponsePage from "../../../generated_pages/supplementary_data/view-submitted-response.page.js";
import { assertSummaryItems, assertSummaryTitles, assertSummaryValues } from "../../../helpers";
import { getRandomString } from "../../../jwt_helper";

// :TODO: this test currently only runs locally, remove the .skip once the mock endpoint is running in a container
describe.skip("Using supplementary data", () => {
  const responseId = getRandomString(16);
  const summaryItems = ".ons-summary__item--text";
  const summaryValues = ".ons-summary__values";
  const summaryRowTitles = ".ons-summary__row-title";

  before("Starting the survey", async () => {
    await browser.openQuestionnaire("test_supplementary_data.json", {
      version: "v2",
      sdsDatasetId: "c067f6de-6d64-42b1-8b02-431a3486c178",
      responseId: responseId,
    });
  });

  it("Given I launch a survey using supplementary data, When I begin the introduction block, Then I see the supplementary data piped in", async () => {
    await $(LoadedSuccessfullyBlockPage.submit()).click();
    await $(IntroductionBlockPage.acceptCookies()).click();
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
  });

  it("Given I have a section summary enabled, When I reach the section summary, Then I see it rendered correctly with supplementary data", async () => {
    await $(Section1InterstitialPage.submit()).click();
    await expect(await $(Section1Page.emailQuestion()).getText()).to.contain("Is contact@tesco.org still the correct contact email for Tesco?");
    await expect(await $(Section1Page.sameEmailAnswer()).getText()).to.contain("Yes");
    await expect(await $(Section1Page.tradingQuestion()).getText()).to.contain("When did Tesco begin trading?");
    await expect(await $(Section1Page.tradingAnswer()).getText()).to.contain("Sunday 30 November 1947");
    await expect(await $$(summaryRowTitles)[0].getText()).to.contain("How much of the £555,000.00 total UK sales was from Bristol and London?");
    await expect(await $(Section1Page.salesBristolAnswer()).getText()).to.contain("£333,000.00");
    await expect(await $(Section1Page.salesLondonAnswer()).getText()).to.contain("£111,000.00");
  });

  it("Given I change the email for the company, When I return to the interstitial block, Then I see the email has updated", async () => {
    await $(Section1Page.sameEmailAnswerEdit()).click();
    await $(EmailBlockPage.no()).click();
    await $(EmailBlockPage.submit()).click();
    await $(NewEmailPage.answer()).setValue("new.contact@gmail.com");
    await $(NewEmailPage.submit()).click();
    await $(Section1Page.previous()).click();
    await expect(await $("body").getText()).to.have.string("Email: new.contact@gmail.com");
    await $(Section1InterstitialPage.submit()).click();
    await $(Section1Page.submit()).click();
  });

  it("Given I have a list collector block using a supplementary list, When I start the section, I see the supplementary list items in the list", async () => {
    await $(HubPage.submit()).click();
    // TODO once list collector content block is merged in update this test accordingly
    await expect(await $(ListCollectorEmployeesPage.listLabel(1)).getText()).to.contain("Harry Potter");
    await expect(await $(ListCollectorEmployeesPage.listLabel(2)).getText()).to.contain("Clark Kent");
    await $(ListCollectorEmployeesPage.no()).click();
    await $(ListCollectorEmployeesPage.submit()).click();
  });

  it("Given I have a list collector block using a supplementary list, When I reach the section summary, I see the supplementary list items in the list", async () => {
    // TODO once list collector content block is merged in update this test accordingly
    await expect(await $(Section2Page.employeesListLabel(1)).getText()).to.contain("Harry Potter");
    await expect(await $(Section2Page.employeesListLabel(2)).getText()).to.contain("Clark Kent");
    await $(Section2Page.submit()).click();
  });

  it("Given I add some additional employees via a list collector, When I return to the Hub, Then I see new enabled sections for the supplementary list items, and my added ones", async () => {
    await $(HubPage.submit()).click();
    await $(AnyAdditionalEmployeesPage.yes()).click();
    await $(AnyAdditionalEmployeesPage.submit()).click();
    await $(AddAdditionalEmployeePage.employeeFirstName()).setValue("Jane");
    await $(AddAdditionalEmployeePage.employeeLastName()).setValue("Doe");
    await $(AddAdditionalEmployeePage.submit()).click();
    await $(ListCollectorAdditionalPage.yes()).click();
    await $(ListCollectorAdditionalPage.submit()).click();
    await $(AddAdditionalEmployeePage.employeeFirstName()).setValue("John");
    await $(AddAdditionalEmployeePage.employeeLastName()).setValue("Smith");
    await $(AddAdditionalEmployeePage.submit()).click();
    await $(ListCollectorAdditionalPage.no()).click();
    await $(ListCollectorAdditionalPage.submit()).click();
    await $(Section3Page.submit()).click();
    await expect(await $(HubPage.summaryItems("section-4-1")).getText()).to.contain("Harry Potter");
    await expect(await $(HubPage.summaryItems("section-4-2")).getText()).to.contain("Clark Kent");
    await expect(await $(HubPage.summaryItems("section-5-1")).getText()).to.contain("Jane Doe");
    await expect(await $(HubPage.summaryItems("section-5-2")).getText()).to.contain("John Smith");
    await $(HubPage.submit()).click();
  });

  it("Given I have repeating sections for both supplementary and dynamic list items, When I start a repeating section for a supplementary list item, Then I see static supplementary data correctly piped in", async () => {
    await expect(await $(LengthOfEmploymentPage.questionTitle()).getText()).to.contain("When did Harry Potter start working for Tesco?");
    await expect(await $(LengthOfEmploymentPage.employmentStartLegend()).getText()).to.contain("Start date at Tesco");
  });

  it("Given I have validation on the start date in the repeating section, When I enter a date before the incorporation date, Then I see an error message", async () => {
    await $(LengthOfEmploymentPage.day()).setValue(1);
    await $(LengthOfEmploymentPage.month()).setValue(1);
    await $(LengthOfEmploymentPage.year()).setValue(1930);
    await $(LengthOfEmploymentPage.submit()).click();
    await expect(await $(LengthOfEmploymentPage.singleErrorLink()).getText()).to.contain("Enter a date after 26 November 1947");
  });

  it("Given I have validation on the start date in the repeating section, When I enter a date after the incorporation date, Then I see that date on the summary page for the section", async () => {
    await $(LengthOfEmploymentPage.year()).setValue(1990);
    await $(LengthOfEmploymentPage.submit()).click();
    await expect(await $(Section4Page.lengthEmploymentQuestion()).getText()).to.contain("When did Harry Potter start working for Tesco?");
    await expect(await $(Section4Page.employmentStart()).getText()).to.contain("1 January 1990");
  });

  it("Given I complete the repeating section for the other supplementary item, When I reach the summary page, Then I see the correct supplementary data with my answers", async () => {
    await $(Section4Page.submit()).click();
    await $(HubPage.submit()).click();
    await expect(await $(LengthOfEmploymentPage.questionTitle()).getText()).to.contain("When did Clark Kent start working for Tesco?");
    await $(LengthOfEmploymentPage.day()).setValue(5);
    await $(LengthOfEmploymentPage.month()).setValue(6);
    await $(LengthOfEmploymentPage.year()).setValue(2011);
    await $(LengthOfEmploymentPage.submit()).click();
    await expect(await $(Section4Page.lengthEmploymentQuestion()).getText()).to.contain("When did Clark Kent start working for Tesco?");
    await expect(await $(Section4Page.employmentStart()).getText()).to.contain("5 June 2011");
  });

  it("Given I move onto the dynamic list items, When I start a repeating section for a dynamic list item, Then I see static supplementary data correctly piped in and the same validation and summary", async () => {
    await $(Section4Page.submit()).click();
    await $(HubPage.submit()).click();
    await expect(await $(AdditionalLengthOfEmploymentPage.questionTitle()).getText()).to.contain("When did Jane Doe start working for Tesco?");
    await expect(await $(AdditionalLengthOfEmploymentPage.additionalEmploymentStartLegend()).getText()).to.contain("Start date at Tesco");
    await $(AdditionalLengthOfEmploymentPage.day()).setValue(1);
    await $(AdditionalLengthOfEmploymentPage.month()).setValue(1);
    await $(AdditionalLengthOfEmploymentPage.year()).setValue(1930);
    await $(AdditionalLengthOfEmploymentPage.submit()).click();
    await expect(await $(AdditionalLengthOfEmploymentPage.singleErrorLink()).getText()).to.contain("Enter a date after 26 November 1947");
    await $(AdditionalLengthOfEmploymentPage.year()).setValue(2000);
    await $(AdditionalLengthOfEmploymentPage.submit()).click();
    await expect(await $(Section5Page.additionalLengthEmploymentQuestion()).getText()).to.contain("When did Jane Doe start working for Tesco?");
    await expect(await $(Section5Page.additionalEmploymentStart()).getText()).to.contain("1 January 2000");
    await $(Section5Page.submit()).click();
    await $(HubPage.submit()).click();
    await $(AdditionalLengthOfEmploymentPage.day()).setValue(3);
    await $(AdditionalLengthOfEmploymentPage.month()).setValue(3);
    await $(AdditionalLengthOfEmploymentPage.year()).setValue(2010);
    await $(AdditionalLengthOfEmploymentPage.submit()).click();
    await expect(await $(Section5Page.additionalLengthEmploymentQuestion()).getText()).to.contain("When did John Smith start working for Tesco?");
    await expect(await $(Section5Page.additionalEmploymentStart()).getText()).to.contain("3 March 2010");
    await $(Section5Page.submit()).click();
  });

  it("Given I have some repeating blocks with supplementary data, When I begin the section, Then I see the supplementary names rendered correctly", async () => {
    await $(HubPage.submit()).click();
    await expect(await $(ListCollectorProductsPage.listLabel(1)).getText()).to.contain("Articles and equipment for sports or outdoor games");
    await expect(await $(ListCollectorProductsPage.listLabel(2)).getText()).to.contain("Kitchen Equipment");
    await $(ListCollectorProductsPage.no()).click();
    await $(ListCollectorProductsPage.submit()).click();
  });

  it("Given I have repeating blocks with supplementary data, When I start the first repeating block, Then I see the supplementary data for the first list item", async () => {
    await expect(await $("body").getText()).to.have.string("Include");
    await expect(await $("body").getText()).to.have.string("for children's playgrounds");
    await expect(await $("body").getText()).to.have.string("Exclude");
    await expect(await $("body").getText()).to.have.string(
      "sports holdalls, gloves, clothing of textile materials, footwear, protective eyewear, rackets, balls, skates"
    );
    await expect(await $(ProductRepeatingBlock1Page.productVolumeSalesLabel()).getText()).to.contain(
      "Volume of sales for Articles and equipment for sports or outdoor games"
    );
    await expect(await $(ProductRepeatingBlock1Page.productVolumeTotalLabel()).getText()).to.contain(
      "Total volume produced for Articles and equipment for sports or outdoor games"
    );
    await $(ProductRepeatingBlock1Page.productVolumeSales()).setValue(100);
    await $(ProductRepeatingBlock1Page.productVolumeTotal()).setValue(200);
  });

  it("Given I have repeating blocks with supplementary data, When I start the second repeating block, Then I see the supplementary data for the second list item", async () => {
    await $(ProductRepeatingBlock1Page.submit()).click();
    // TODO once using list collector content, shouldn't need these two lines
    await $(ListCollectorProductsPage.no()).click();
    await $(ListCollectorProductsPage.submit()).click();
    await expect(await $("body").getText()).to.have.string("Include");
    await expect(await $("body").getText()).to.have.string("pots and pans");
    await expect(await $("body").getText()).not.to.have.string("Exclude");
    await expect(await $(ProductRepeatingBlock1Page.productVolumeSalesLabel()).getText()).to.contain("Volume of sales for Kitchen Equipment");
    await expect(await $(ProductRepeatingBlock1Page.productVolumeTotalLabel()).getText()).to.contain("Total volume produced for Kitchen Equipment");
    await $(ProductRepeatingBlock1Page.productVolumeSales()).setValue(50);
    await $(ProductRepeatingBlock1Page.productVolumeTotal()).setValue(300);
    await $(ProductRepeatingBlock1Page.submit()).click();
  });

  it("Given I have a calculated summary using the repeating blocks, When I reach the Calculated Summary, Then I see the correct total and supplementary data labels", async () => {
    await $(ListCollectorProductsPage.no()).click();
    await $(ListCollectorProductsPage.submit()).click();
    await expect(await $(CalculatedSummaryVolumeSalesPage.calculatedSummaryTitle()).getText()).to.contain(
      "We calculate the total volume of sales over the previous quarter to be 150 kg. Is this correct?"
    );
    assertSummaryItems(["Volume of sales for Articles and equipment for sports or outdoor games", "Volume of sales for Kitchen Equipment"]);
    assertSummaryValues(["100 kg", "50 kg"]);
    await $(CalculatedSummaryVolumeSalesPage.submit()).click();
  });

  it("Given I have another calculated summary using the repeating blocks, When I reach the Calculated Summary, Then I see the correct total and supplementary data labels", async () => {
    await expect(await $(CalculatedSummaryVolumeTotalPage.calculatedSummaryTitle()).getText()).to.contain(
      "We calculate the total volume produced over the previous quarter to be 500 kg. Is this correct?"
    );
    assertSummaryItems(["Total volume produced for Articles and equipment for sports or outdoor games", "Total volume produced for Kitchen Equipment"]);
    assertSummaryValues(["200 kg", "300 kg"]);
    await $(CalculatedSummaryVolumeTotalPage.submit()).click();
  });

  it("Given I have dynamic answers using a supplementary list, When I reach the dynamic answer page, Then I see the correct supplementary data in the answer labels", async () => {
    await expect(await $$(DynamicProductsPage.labels())[0].getText()).to.contain("Value of sales for Articles and equipment for sports or outdoor games");
    await expect(await $$(DynamicProductsPage.labels())[1].getText()).to.contain("Value of sales for Kitchen Equipment");
    await expect(await $$(DynamicProductsPage.labels())[2].getText()).to.contain("Value of sales from other categories");
    await $$(DynamicProductsPage.inputs())[0].setValue(110);
    await $$(DynamicProductsPage.inputs())[1].setValue(220);
    await $$(DynamicProductsPage.inputs())[2].setValue(330);
    await $(DynamicProductsPage.submit()).click();
  });

  it("Given I have a calculated summary of dynamic answers for a supplementary list, When I reach the calculated summary, Then I see the correct supplementary data in the title and labels", async () => {
    await expect(await $(CalculatedSummaryValueSalesPage.calculatedSummaryTitle()).getText()).to.contain(
      "We calculate the total value of sales over the previous quarter to be £660.00. Is this correct?"
    );
    assertSummaryItems([
      "Value of sales for Articles and equipment for sports or outdoor games",
      "Value of sales for Kitchen Equipment",
      "Value of sales from other categories",
    ]);
    assertSummaryValues(["£110.00", "£220.00", "£330.00"]);
    await $(CalculatedSummaryValueSalesPage.submit()).click();
  });

  it("Given I have a section summary for product details, When I reach the summary page, Then I see the supplementary data and my answers rendered correctly", async () => {
    await expect(await $$(summaryRowTitles)[0].getText()).to.contain("Sales during the previous quarter");
    assertSummaryItems([
      "Articles and equipment for sports or outdoor games",
      "Volume of sales for Articles and equipment for sports or outdoor games",
      "Total volume produced for Articles and equipment for sports or outdoor games",
      "Kitchen Equipment",
      "Volume of sales for Kitchen Equipment",
      "Total volume produced for Kitchen Equipment",
      "Value of sales for Articles and equipment for sports or outdoor games",
      "Value of sales for Kitchen Equipment",
      "Value of sales from other categories",
    ]);
    assertSummaryValues(["100 kg", "200 kg", "110 kg", "50 kg", "300 kg", "220 kg", "£110.00", "£220.00", "£330.00"]);
    await $(Section6Page.submit()).click();
  });

  it("Given I relaunch the survey for a newer version of the supplementary data, When I open the Hub page, Then I see the new supplementary list items as new incomplete sections and not the old ones", async () => {
    await browser.openQuestionnaire("test_supplementary_data.json", {
      version: "v2",
      sdsDatasetId: "693dc252-2e90-4412-bd9c-c4d953e36fcd",
      responseId: responseId,
    });
    await expect(await $(HubPage.summaryItems("section-4-1")).getText()).to.contain("Harry Potter");
    await expect(await $(HubPage.summaryItems("section-4-2")).getText()).to.contain("Bruce Wayne");
    await expect(await $(HubPage.summaryItems("section-5-1")).getText()).to.contain("Jane Doe");
    await expect(await $(HubPage.summaryItems("section-5-2")).getText()).to.contain("John Smith");
    await expect(await $(HubPage.summaryRowState("section-4-1")).getText()).to.equal("Completed");
    await expect(await $(HubPage.summaryRowState("section-4-2")).getText()).to.equal("Not started");
    await expect(await $(HubPage.summaryRowState("section-5-1")).getText()).to.equal("Completed");
    await expect(await $(HubPage.summaryRowState("section-5-2")).getText()).to.equal("Completed");
    await expect(await $("body").getText()).to.not.have.string("Clark Kent");
  });

  it("Given I now have a new incomplete section, When I start the section, Then I see the new supplementary data piped in accordingly", async () => {
    await $(HubPage.submit()).click();
    await $(LengthOfEmploymentPage.day()).setValue(10);
    await $(LengthOfEmploymentPage.month()).setValue(10);
    await $(LengthOfEmploymentPage.year()).setValue(1999);
    await $(LengthOfEmploymentPage.submit()).click();
    await expect(await $(Section4Page.lengthEmploymentQuestion()).getText()).to.contain("When did Bruce Wayne start working for Lidl?");
    await expect(await $(Section4Page.employmentStart()).getText()).to.contain("10 October 1999");
    await $(Section4Page.submit()).click();
  });

  it("Given I can view my response after submission, When I submit the survey, Then I see the values I've entered and correct rendering with supplementary data", async () => {
    await $(HubPage.submit()).click();
    await $(ThankYouPage.savePrintAnswersLink()).click();

    assertSummaryTitles(["Company Details", "Employees", "Additional Employees", "Harry Potter", "Bruce Wayne", "Jane Doe", "John Smith", "Product details"]);

    // Company details
    await expect(await $(ViewSubmittedResponsePage.emailQuestion()).getText()).to.contain("Is contact@lidl.org still the correct contact email for Lidl?");
    await expect(await $(ViewSubmittedResponsePage.sameEmailAnswer()).getText()).to.contain("No");
    await expect(await $(ViewSubmittedResponsePage.newEmailQuestion()).getText()).to.contain("What is the new contact email for Lidl?");
    await expect(await $(ViewSubmittedResponsePage.newEmailAnswer()).getText()).to.contain("new.contact@gmail.com");
    await expect(await $(ViewSubmittedResponsePage.tradingQuestion()).getText()).to.contain("When did Lidl begin trading?");
    await expect(await $(ViewSubmittedResponsePage.tradingAnswer()).getText()).to.contain("Sunday 30 November 1947");
    await expect(await $$(summaryRowTitles)[0].getText()).to.contain("How much of the £555,000.00 total UK sales was from Bristol and London?");
    await expect(await $(ViewSubmittedResponsePage.salesBristolAnswer()).getText()).to.contain("£333,000.00");
    await expect(await $(ViewSubmittedResponsePage.salesLondonAnswer()).getText()).to.contain("£111,000.00");

    // Employees
    await expect(await $(ViewSubmittedResponsePage.employeeReportingContent(0)).$$(summaryItems)[0].getText()).to.equal("Harry Potter");
    await expect(await $(ViewSubmittedResponsePage.employeeReportingContent(0)).$$(summaryItems)[1].getText()).to.equal("Bruce Wayne");

    // Additional Employees
    await expect(await $(ViewSubmittedResponsePage.anyAdditionalEmployeeQuestion()).getText()).to.contain("Do you have any additional employees to report on?");
    await expect(await $(ViewSubmittedResponsePage.anyAdditionalEmployeeAnswer()).getText()).to.contain("Yes");
    await expect(await $(ViewSubmittedResponsePage.additionalEmployeeReportingContent(1)).$$(summaryItems)[0].getText()).to.equal("Jane Doe");
    await expect(await $(ViewSubmittedResponsePage.additionalEmployeeReportingContent(1)).$$(summaryItems)[1].getText()).to.equal("John Smith");

    // Harry Potter
    await expect(await $(ViewSubmittedResponsePage.employeeDetailQuestionsContent(0)).$$(summaryItems)[0].getText()).to.equal(
      "When did Harry Potter start working for Lidl?"
    );
    await expect(await $(ViewSubmittedResponsePage.employeeDetailQuestionsContent(0)).$$(summaryValues)[0].getText()).to.equal("1 January 1990");

    // Bruce Wayne
    await expect(await $(ViewSubmittedResponsePage.employeeDetailQuestionsContent("0-1")).$$(summaryItems)[0].getText()).to.equal(
      "When did Bruce Wayne start working for Lidl?"
    );
    await expect(await $(ViewSubmittedResponsePage.employeeDetailQuestionsContent("0-1")).$$(summaryValues)[0].getText()).to.equal("10 October 1999");

    // Jane Doe
    await expect(await $(ViewSubmittedResponsePage.additionalEmployeeDetailQuestionsContent(0)).$$(summaryItems)[0].getText()).to.equal(
      "When did Jane Doe start working for Lidl?"
    );
    await expect(await $(ViewSubmittedResponsePage.additionalEmployeeDetailQuestionsContent(0)).$$(summaryValues)[0].getText()).to.equal("1 January 2000");

    // John Smith
    await expect(await $(ViewSubmittedResponsePage.additionalEmployeeDetailQuestionsContent("0-2")).$$(summaryItems)[0].getText()).to.equal(
      "When did John Smith start working for Lidl?"
    );
    await expect(await $(ViewSubmittedResponsePage.additionalEmployeeDetailQuestionsContent("0-2")).$$(summaryValues)[0].getText()).to.equal("3 March 2010");

    // Product details
    await expect(await $(ViewSubmittedResponsePage.productReportingContent(0)).$$(summaryItems)[0].getText()).to.equal(
      "Articles and equipment for sports or outdoor games"
    );
    await expect(await $(ViewSubmittedResponsePage.productReportingContent(0)).$$(summaryItems)[1].getText()).to.equal(
      "Volume of sales for Articles and equipment for sports or outdoor games"
    );
    await expect(await $(ViewSubmittedResponsePage.productReportingContent(0)).$$(summaryItems)[2].getText()).to.equal(
      "Total volume produced for Articles and equipment for sports or outdoor games"
    );
    await expect(await $(ViewSubmittedResponsePage.productReportingContent(0)).$$(summaryValues)[0].getText()).to.equal("100 kg");
    await expect(await $(ViewSubmittedResponsePage.productReportingContent(0)).$$(summaryValues)[1].getText()).to.equal("200 kg");
    await expect(await $(ViewSubmittedResponsePage.productReportingContent(0)).$$(summaryItems)[3].getText()).to.equal("Kitchen Equipment");
    await expect(await $(ViewSubmittedResponsePage.productReportingContent(0)).$$(summaryItems)[4].getText()).to.equal("Volume of sales for Kitchen Equipment");
    await expect(await $(ViewSubmittedResponsePage.productReportingContent(0)).$$(summaryItems)[5].getText()).to.equal(
      "Total volume produced for Kitchen Equipment"
    );
    await expect(await $(ViewSubmittedResponsePage.productReportingContent(0)).$$(summaryValues)[2].getText()).to.equal("50 kg");
    await expect(await $(ViewSubmittedResponsePage.productReportingContent(0)).$$(summaryValues)[3].getText()).to.equal("300 kg");
    await expect(await $(ViewSubmittedResponsePage.productReportingContent(1)).$$(summaryRowTitles)[0].getText()).to.equal("Sales during the previous quarter");
    await expect(await $(ViewSubmittedResponsePage.productReportingContent(1)).$$(summaryItems)[0].getText()).to.equal(
      "Value of sales for Articles and equipment for sports or outdoor games"
    );
    await expect(await $(ViewSubmittedResponsePage.productReportingContent(1)).$$(summaryItems)[1].getText()).to.equal("Value of sales for Kitchen Equipment");
    await expect(await $(ViewSubmittedResponsePage.productReportingContent(1)).$$(summaryItems)[2].getText()).to.equal("Value of sales for Groceries");
    await expect(await $(ViewSubmittedResponsePage.productReportingContent(1)).$$(summaryItems)[3].getText()).to.equal("Value of sales from other categories");
    await expect(await $(ViewSubmittedResponsePage.productReportingContent(1)).$$(summaryValues)[0].getText()).to.equal("£110.00");
    await expect(await $(ViewSubmittedResponsePage.productReportingContent(1)).$$(summaryValues)[1].getText()).to.equal("£220.00");
    await expect(await $(ViewSubmittedResponsePage.productReportingContent(1)).$$(summaryValues)[2].getText()).to.equal("No answer provided");
    await expect(await $(ViewSubmittedResponsePage.productReportingContent(1)).$$(summaryValues)[3].getText()).to.equal("£330.00");
  });
});
