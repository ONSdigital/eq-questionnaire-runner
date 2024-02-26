import { assertSummaryItems, assertSummaryTitles, assertSummaryValues, checkListItemComplete, checkListItemIncomplete, click } from "../../../helpers";
import { expect } from "@wdio/globals";
import { getRandomString } from "../../../jwt_helper";
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
import ProductQuestion3EnabledPage from "../../../generated_pages/supplementary_data/product-question-3-enabled.page";
import ProductRepeatingBlock1Page from "../../../generated_pages/supplementary_data/product-repeating-block-1-repeating-block.page.js";
import ProductSalesInterstitialPage from "../../../generated_pages/supplementary_data/product-sales-interstitial.page";
import ProductVolumeInterstitialPage from "../../../generated_pages/supplementary_data/product-volume-interstitial.page";
import SalesBreakdownBlockPage from "../../../generated_pages/supplementary_data/sales-breakdown-block.page.js";
import Section1InterstitialPage from "../../../generated_pages/supplementary_data/section-1-interstitial.page.js";
import Section1Page from "../../../generated_pages/supplementary_data/section-1-summary.page.js";
import Section3Page from "../../../generated_pages/supplementary_data/section-3-summary.page.js";
import Section4Page from "../../../generated_pages/supplementary_data/section-4-summary.page.js";
import Section5Page from "../../../generated_pages/supplementary_data/section-5-summary.page.js";
import Section6Page from "../../../generated_pages/supplementary_data/section-6-summary.page.js";
import ThankYouPage from "../../../base_pages/thank-you.page";
import TradingPage from "../../../generated_pages/supplementary_data/trading.page.js";
import ViewSubmittedResponsePage from "../../../generated_pages/supplementary_data/view-submitted-response.page.js";

describe("Using supplementary data", () => {
  const responseId = getRandomString(16);
  const summaryItems = ".ons-summary__item--text";
  const summaryValues = ".ons-summary__values";
  const summaryRowTitles = ".ons-summary__row-title";

  before("Starting the survey", async () => {
    await browser.openQuestionnaire("test_supplementary_data.json", {
      version: "v2",
      sdsDatasetId: "c067f6de-6d64-42b1-8b02-431a3486c178",
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

  it("Given I have a list collector content block using a supplementary list, When I start the section, I see the supplementary list items in the list", async () => {
    await click(HubPage.submit());
    await expect(await $(ListCollectorEmployeesPage.listLabel(1)).getText()).toBe("Harry Potter");
    await expect(await $(ListCollectorEmployeesPage.listLabel(2)).getText()).toBe("Clark Kent");
    await click(ListCollectorEmployeesPage.submit());
  });

  it("Given I add some additional employees via another list collector, When I return to the Hub, Then I see new enabled sections for the supplementary list items and my added ones", async () => {
    await click(HubPage.submit());
    await $(AnyAdditionalEmployeesPage.yes()).click();
    await click(AnyAdditionalEmployeesPage.submit());
    await $(AddAdditionalEmployeePage.employeeFirstName()).setValue("Jane");
    await $(AddAdditionalEmployeePage.employeeLastName()).setValue("Doe");
    await click(AddAdditionalEmployeePage.submit());
    await $(ListCollectorAdditionalPage.yes()).click();
    await click(ListCollectorAdditionalPage.submit());
    await $(AddAdditionalEmployeePage.employeeFirstName()).setValue("John");
    await $(AddAdditionalEmployeePage.employeeLastName()).setValue("Smith");
    await click(AddAdditionalEmployeePage.submit());
    await $(ListCollectorAdditionalPage.no()).click();
    await click(ListCollectorAdditionalPage.submit());
    await click(Section3Page.submit());
    await expect(await $(HubPage.summaryItems("section-4-1")).getText()).toContain("Harry Potter");
    await expect(await $(HubPage.summaryItems("section-4-2")).getText()).toContain("Clark Kent");
    await expect(await $(HubPage.summaryItems("section-5-1")).getText()).toContain("Jane Doe");
    await expect(await $(HubPage.summaryItems("section-5-2")).getText()).toContain("John Smith");
    await click(HubPage.submit());
  });

  it("Given I have repeating sections for both supplementary and dynamic list items, When I start a repeating section for a supplementary list item, Then I see static supplementary data correctly piped in", async () => {
    await expect(await $(LengthOfEmploymentPage.questionTitle()).getText()).toContain("When did Harry Potter start working for Tesco?");
    await expect(await $(LengthOfEmploymentPage.employmentStartLegend()).getText()).toContain("Start date at Tesco");
  });

  it("Given I have validation on the start date in the repeating section, When I enter a date before the incorporation date, Then I see an error message", async () => {
    await $(LengthOfEmploymentPage.day()).setValue(1);
    await $(LengthOfEmploymentPage.month()).setValue(1);
    await $(LengthOfEmploymentPage.year()).setValue(1930);
    await click(LengthOfEmploymentPage.submit());
    await expect(await $(LengthOfEmploymentPage.singleErrorLink()).getText()).toBe("Enter a date after 26 November 1947");
  });

  it("Given I have validation on the start date in the repeating section, When I enter a date after the incorporation date, Then I see that date on the summary page for the section", async () => {
    await $(LengthOfEmploymentPage.year()).setValue(1990);
    await click(LengthOfEmploymentPage.submit());
    await expect(await $(Section4Page.lengthEmploymentQuestion()).getText()).toBe("When did Harry Potter start working for Tesco?");
    await expect(await $(Section4Page.employmentStart()).getText()).toBe("1 January 1990");
  });

  it("Given I complete the repeating section for another supplementary item, When I reach the summary page, Then I see the correct supplementary data with my answers", async () => {
    await click(Section4Page.submit());
    await click(HubPage.submit());
    await expect(await $(LengthOfEmploymentPage.questionTitle()).getText()).toContain("When did Clark Kent start working for Tesco?");
    await $(LengthOfEmploymentPage.day()).setValue(5);
    await $(LengthOfEmploymentPage.month()).setValue(6);
    await $(LengthOfEmploymentPage.year()).setValue(2011);
    await click(LengthOfEmploymentPage.submit());
    await expect(await $(Section4Page.lengthEmploymentQuestion()).getText()).toBe("When did Clark Kent start working for Tesco?");
    await expect(await $(Section4Page.employmentStart()).getText()).toBe("5 June 2011");
  });

  it("Given I move onto the dynamic list items, When I start a repeating section for a dynamic list item, Then I see static supplementary data correctly piped in and the same validation and summary", async () => {
    await click(Section4Page.submit());
    await click(HubPage.submit());
    await expect(await $(AdditionalLengthOfEmploymentPage.questionTitle()).getText()).toContain("When did Jane Doe start working for Tesco?");
    await expect(await $(AdditionalLengthOfEmploymentPage.additionalEmploymentStartLegend()).getText()).toBe("Start date at Tesco");
    await $(AdditionalLengthOfEmploymentPage.day()).setValue(1);
    await $(AdditionalLengthOfEmploymentPage.month()).setValue(1);
    await $(AdditionalLengthOfEmploymentPage.year()).setValue(1930);
    await click(AdditionalLengthOfEmploymentPage.submit());
    await expect(await $(AdditionalLengthOfEmploymentPage.singleErrorLink()).getText()).toBe("Enter a date after 26 November 1947");
    await $(AdditionalLengthOfEmploymentPage.year()).setValue(2000);
    await click(AdditionalLengthOfEmploymentPage.submit());
    await expect(await $(Section5Page.additionalLengthEmploymentQuestion()).getText()).toBe("When did Jane Doe start working for Tesco?");
    await expect(await $(Section5Page.additionalEmploymentStart()).getText()).toBe("1 January 2000");
    await click(Section5Page.submit());
    await click(HubPage.submit());
    await $(AdditionalLengthOfEmploymentPage.day()).setValue(3);
    await $(AdditionalLengthOfEmploymentPage.month()).setValue(3);
    await $(AdditionalLengthOfEmploymentPage.year()).setValue(2010);
    await click(AdditionalLengthOfEmploymentPage.submit());
    await expect(await $(Section5Page.additionalLengthEmploymentQuestion()).getText()).toBe("When did John Smith start working for Tesco?");
    await expect(await $(Section5Page.additionalEmploymentStart()).getText()).toBe("3 March 2010");
    await click(Section5Page.submit());
  });

  it("Given I have some repeating blocks with supplementary data, When I begin the section, Then I see the supplementary names rendered correctly", async () => {
    await click(HubPage.submit());
    await expect(await $(ListCollectorProductsPage.listLabel(1)).getText()).toBe("Articles and equipment for sports or outdoor games");
    await expect(await $(ListCollectorProductsPage.listLabel(2)).getText()).toBe("Kitchen Equipment");
    await click(ListCollectorProductsPage.submit());
  });

  it("Given I have repeating blocks with supplementary data, When I start the first repeating block, Then I see the supplementary data for the first list item", async () => {
    await expect(await $("body").getHTML()).toContain("<h2>Include</h2>");
    await expect(await $("body").getHTML()).toContain("<li>for children's playgrounds</li>");
    await expect(await $("body").getHTML()).toContain("<li>swimming pools and paddling pools</li>");
    await expect(await $("body").getHTML()).toContain("<h2>Exclude</h2>");
    await expect(await $("body").getHTML()).toContain(
      "<li>sports holdalls, gloves, clothing of textile materials, footwear, protective eyewear, rackets, balls, skates</li>",
    );
    await expect(await $("body").getHTML()).toContain(
      "<li>for skiing, water sports, golf, fishing', for skiing, water sports, golf, fishing, table tennis, PE, gymnastics, athletics</li>",
    );
    await expect(await $(ProductRepeatingBlock1Page.productVolumeSalesLabel()).getText()).toBe(
      "Volume of sales for Articles and equipment for sports or outdoor games",
    );
    await expect(await $(ProductRepeatingBlock1Page.productVolumeTotalLabel()).getText()).toBe(
      "Total volume produced for Articles and equipment for sports or outdoor games",
    );
    await $(ProductRepeatingBlock1Page.productVolumeSales()).setValue(100);
    await $(ProductRepeatingBlock1Page.productVolumeTotal()).setValue(200);
  });

  it("Given I have repeating blocks with supplementary data, When I start the second repeating block, Then I see the supplementary data for the second list item", async () => {
    await click(ProductRepeatingBlock1Page.submit());
    await click(ListCollectorProductsPage.submit());
    await expect(await $("body").getText()).toContain("Include");
    await expect(await $("body").getText()).toContain("pots and pans");
    await expect(await $("body").getText()).not.toBe("Exclude");
    await expect(await $(ProductRepeatingBlock1Page.productVolumeSalesLabel()).getText()).toBe("Volume of sales for Kitchen Equipment");
    await expect(await $(ProductRepeatingBlock1Page.productVolumeTotalLabel()).getText()).toBe("Total volume produced for Kitchen Equipment");
    await $(ProductRepeatingBlock1Page.productVolumeSales()).setValue(50);
    await $(ProductRepeatingBlock1Page.productVolumeTotal()).setValue(300);
    await click(ProductRepeatingBlock1Page.submit());
  });

  it("Given I have a calculated summary using the repeating blocks, When I reach the Calculated Summary, Then I see the correct total and supplementary data labels", async () => {
    await click(ListCollectorProductsPage.submit());
    await expect(browser).toHaveUrlContaining(CalculatedSummaryVolumeSalesPage.pageName);
    await expect(await $(CalculatedSummaryVolumeSalesPage.calculatedSummaryTitle()).getText()).toBe(
      "We calculate the total volume of sales over the previous quarter to be 150 kg. Is this correct?",
    );
    await assertSummaryItems([
      "Volume of sales for Articles and equipment for sports or outdoor games",
      "Volume of sales for Kitchen Equipment",
      "Total sales volume",
    ]);
    await assertSummaryValues(["100 kg", "50 kg", "150 kg"]);
    await click(CalculatedSummaryVolumeSalesPage.submit());
  });

  it("Given I have another calculated summary using the repeating blocks, When I reach the Calculated Summary, Then I see the correct total and supplementary data labels", async () => {
    await expect(await $(CalculatedSummaryVolumeTotalPage.calculatedSummaryTitle()).getText()).toBe(
      "We calculate the total volume produced over the previous quarter to be 500 kg. Is this correct?",
    );
    await assertSummaryItems([
      "Total volume produced for Articles and equipment for sports or outdoor games",
      "Total volume produced for Kitchen Equipment",
      "Total volume produced",
    ]);
    await assertSummaryValues(["200 kg", "300 kg", "500 kg"]);
    await click(CalculatedSummaryVolumeTotalPage.submit());
  });

  it("Given I have dynamic answers using a supplementary list, When I reach the dynamic answer page, Then I see the correct supplementary data in the answer labels", async () => {
    await expect(await $$(DynamicProductsPage.labels())[0].getText()).toBe("Value of sales for Articles and equipment for sports or outdoor games");
    await expect(await $$(DynamicProductsPage.labels())[1].getText()).toBe("Value of sales for Kitchen Equipment");
    await expect(await $$(DynamicProductsPage.labels())[2].getText()).toBe("Value of sales from other categories");
    await $$(DynamicProductsPage.inputs())[0].setValue(110);
    await $$(DynamicProductsPage.inputs())[1].setValue(220);
    await $$(DynamicProductsPage.inputs())[2].setValue(330);
    await click(DynamicProductsPage.submit());
  });

  it("Given I have a calculated summary of dynamic answers for a supplementary list, When I reach the calculated summary, Then I see the correct supplementary data in the title and labels", async () => {
    await expect(await $(CalculatedSummaryValueSalesPage.calculatedSummaryTitle()).getText()).toBe(
      "We calculate the total value of sales over the previous quarter to be £660.00. Is this correct?",
    );
    await assertSummaryItems([
      "Value of sales for Articles and equipment for sports or outdoor games",
      "Value of sales for Kitchen Equipment",
      "Value of sales from other categories",
      "Total sales value",
    ]);
    await assertSummaryValues(["£110.00", "£220.00", "£330.00", "£660.00"]);
    await click(CalculatedSummaryValueSalesPage.submit());
  });

  it("Given I have a section with repeating answers for a supplementary list, When I reach the section summary page, Then I see the supplementary data and my answers rendered correctly", async () => {
    await expect(await $$(summaryRowTitles)[0].getText()).toBe("Sales during the previous quarter");
    await assertSummaryItems([
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
    await assertSummaryValues(["100 kg", "200 kg", "50 kg", "300 kg", "£110.00", "£220.00", "£330.00"]);
    await click(Section6Page.submit());
    await expect(await $(HubPage.summaryRowState("section-6")).getText()).toBe("Completed");
  });

  it("Given I am using a supplementary dataset where the size of one of the lists skips a question in a section, When I enter the section, Then I only see an interstitial block as the other block is skipped", async () => {
    await $(HubPage.summaryRowLink("section-8")).click();
    await expect(browser).toHaveUrlContaining(ProductVolumeInterstitialPage.pageName);
    await click(ProductVolumeInterstitialPage.submit());
    await expect(await $(HubPage.summaryRowState("section-8")).getText()).toBe("Completed");
  });

  it("Given I relaunch the survey with new supplementary data and new list items for the repeating section, When I open the Hub page, Then I see the new supplementary list items as new incomplete sections and not any old ones", async () => {
    await browser.openQuestionnaire("test_supplementary_data.json", {
      version: "v2",
      sdsDatasetId: "693dc252-2e90-4412-bd9c-c4d953e36fcd",
      responseId,
    });
    await expect(await $(HubPage.summaryItems("section-4-1")).getText()).toContain("Harry Potter");
    await expect(await $(HubPage.summaryItems("section-4-2")).getText()).toContain("Bruce Wayne");
    await expect(await $(HubPage.summaryItems("section-5-1")).getText()).toContain("Jane Doe");
    await expect(await $(HubPage.summaryItems("section-5-2")).getText()).toContain("John Smith");
    await expect(await $(HubPage.summaryRowState("section-4-1")).getText()).toBe("Completed");
    await expect(await $(HubPage.summaryRowState("section-4-2")).getText()).toBe("Not started");
    await expect(await $(HubPage.summaryRowState("section-5-1")).getText()).toBe("Completed");
    await expect(await $(HubPage.summaryRowState("section-5-2")).getText()).toBe("Completed");
    await expect(await $("body").getText()).not.toContain("Clark Kent");
  });

  it("Given the survey has been relaunched with new data and more items in the products list, When I am on the Hub, Then I see the products section and section with a new block due to the product list size are both in progress", async () => {
    await expect(await $(HubPage.summaryRowState("section-6")).getText()).toBe("Partially completed");
    await expect(await $(HubPage.summaryRowState("section-8")).getText()).toBe("Partially completed");
  });

  it("Given I am using a supplementary dataset with a product list size that skips a question in the sales target section, When I enter the section, Then I only see an interstitial block", async () => {
    await $(HubPage.summaryRowLink("section-7")).click();
    await expect(browser).toHaveUrlContaining(ProductSalesInterstitialPage.pageName);
    await click(ProductSalesInterstitialPage.submit());
    await expect(await $(HubPage.summaryRowState("section-7")).getText()).toBe("Completed");
  });

  it("Given there is now an additional product, When I resume the Product Details Section, Then I start from the list collector content block and see the new product is incomplete", async () => {
    await $(HubPage.summaryRowLink("section-6")).click();
    await expect(browser).toHaveUrlContaining(ListCollectorProductsPage.pageName);
    await checkListItemComplete(`dt[data-qa="list-item-1-label"]`);
    await checkListItemComplete(`dt[data-qa="list-item-2-label"]`);
    await checkListItemIncomplete(`dt[data-qa="list-item-3-label"]`);
    await click(ListCollectorProductsPage.submit());
    await expect(browser).toHaveUrlContaining(ProductRepeatingBlock1Page.pageName);
  });

  it("Given I complete the section and relaunch with the old data that has fewer items in the products list, When I am on the Hub, Then I see the products section and sales targets sections are now in progress", async () => {
    await $(ProductRepeatingBlock1Page.productVolumeSales()).setValue(40);
    await $(ProductRepeatingBlock1Page.productVolumeTotal()).setValue(50);
    await click(ProductRepeatingBlock1Page.submit());
    await click(ListCollectorProductsPage.submit());
    await click(CalculatedSummaryVolumeSalesPage.submit());
    await click(CalculatedSummaryVolumeTotalPage.submit());
    await $$(DynamicProductsPage.inputs())[2].setValue(115);
    await click(DynamicProductsPage.submit());
    await click(CalculatedSummaryValueSalesPage.submit());
    await click(Section6Page.submit());
    await expect(await $(HubPage.summaryRowState("section-6")).getText()).toBe("Completed");
    await browser.openQuestionnaire("test_supplementary_data.json", {
      version: "v2",
      sdsDatasetId: "c067f6de-6d64-42b1-8b02-431a3486c178",
      responseId,
    });
    await expect(await $(HubPage.summaryRowState("section-6")).getText()).toBe("Partially completed");
    await expect(await $(HubPage.summaryRowState("section-7")).getText()).toBe("Partially completed");
  });

  it("Given I return to the new data resulting in a new incomplete section, When I start the section, Then I see the new supplementary data piped in accordingly", async () => {
    await browser.openQuestionnaire("test_supplementary_data.json", {
      version: "v2",
      sdsDatasetId: "693dc252-2e90-4412-bd9c-c4d953e36fcd",
      responseId,
    });
    await click(HubPage.submit());
    await $(LengthOfEmploymentPage.day()).setValue(10);
    await $(LengthOfEmploymentPage.month()).setValue(10);
    await $(LengthOfEmploymentPage.year()).setValue(1999);
    await click(LengthOfEmploymentPage.submit());
    await expect(await $(Section4Page.lengthEmploymentQuestion()).getText()).toBe("When did Bruce Wayne start working for Lidl?");
    await expect(await $(Section4Page.employmentStart()).getText()).toBe("10 October 1999");
    await click(Section4Page.submit());
  });

  it("Given I can view my response after submission, When I submit the survey, Then I see the values I've entered and correct rendering with supplementary data", async () => {
    await click(HubPage.submit());
    await click(ListCollectorProductsPage.submit());
    await $(ProductRepeatingBlock1Page.productVolumeSales()).setValue(40);
    await $(ProductRepeatingBlock1Page.productVolumeTotal()).setValue(50);
    await click(ProductRepeatingBlock1Page.submit());
    await click(ListCollectorProductsPage.submit());
    await click(CalculatedSummaryVolumeSalesPage.submit());
    await click(CalculatedSummaryVolumeTotalPage.submit());
    await $$(DynamicProductsPage.inputs())[2].setValue(115);
    await click(DynamicProductsPage.submit());
    await click(CalculatedSummaryValueSalesPage.submit());
    await click(Section6Page.submit());
    await click(HubPage.submit());
    await $(ProductQuestion3EnabledPage.yes()).click();
    await click(ProductQuestion3EnabledPage.submit());
    await click(HubPage.submit());
    await $(ThankYouPage.savePrintAnswersLink()).click();

    await assertSummaryTitles([
      "Company Details",
      "Additional Employees",
      "Harry Potter",
      "Bruce Wayne",
      "Jane Doe",
      "John Smith",
      "Product details",
      "Production Targets",
    ]);

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

    // Additional Employees
    await expect(await $(ViewSubmittedResponsePage.anyAdditionalEmployeeQuestion()).getText()).toBe("Do you have any additional employees to report on?");
    await expect(await $(ViewSubmittedResponsePage.anyAdditionalEmployeeAnswer()).getText()).toBe("Yes");
    await expect(await $(ViewSubmittedResponsePage.additionalEmployeeReportingContent(1)).$$(summaryItems)[0].getText()).toBe("Jane Doe");
    await expect(await $(ViewSubmittedResponsePage.additionalEmployeeReportingContent(1)).$$(summaryItems)[1].getText()).toBe("John Smith");

    // Harry Potter
    await expect(await $(ViewSubmittedResponsePage.employeeDetailQuestionsContent(0)).$$(summaryItems)[0].getText()).toBe(
      "When did Harry Potter start working for Lidl?",
    );
    await expect(await $(ViewSubmittedResponsePage.employeeDetailQuestionsContent(0)).$$(summaryValues)[0].getText()).toBe("1 January 1990");

    // Bruce Wayne
    await expect(await $(ViewSubmittedResponsePage.employeeDetailQuestionsContent("0-1")).$$(summaryItems)[0].getText()).toBe(
      "When did Bruce Wayne start working for Lidl?",
    );
    await expect(await $(ViewSubmittedResponsePage.employeeDetailQuestionsContent("0-1")).$$(summaryValues)[0].getText()).toBe("10 October 1999");

    // Jane Doe
    await expect(await $(ViewSubmittedResponsePage.additionalEmployeeDetailQuestionsContent(0)).$$(summaryItems)[0].getText()).toBe(
      "When did Jane Doe start working for Lidl?",
    );
    await expect(await $(ViewSubmittedResponsePage.additionalEmployeeDetailQuestionsContent(0)).$$(summaryValues)[0].getText()).toBe("1 January 2000");

    // John Smith
    await expect(await $(ViewSubmittedResponsePage.additionalEmployeeDetailQuestionsContent("0-2")).$$(summaryItems)[0].getText()).toBe(
      "When did John Smith start working for Lidl?",
    );
    await expect(await $(ViewSubmittedResponsePage.additionalEmployeeDetailQuestionsContent("0-2")).$$(summaryValues)[0].getText()).toBe("3 March 2010");

    // Product details
    await expect(await $(ViewSubmittedResponsePage.productReportingContent(0)).$$(summaryItems)[0].getText()).toBe(
      "Articles and equipment for sports or outdoor games",
    );
    await expect(await $(ViewSubmittedResponsePage.productReportingContent(0)).$$(summaryItems)[1].getText()).toBe(
      "Volume of sales for Articles and equipment for sports or outdoor games",
    );
    await expect(await $(ViewSubmittedResponsePage.productReportingContent(0)).$$(summaryItems)[2].getText()).toBe(
      "Total volume produced for Articles and equipment for sports or outdoor games",
    );
    await expect(await $(ViewSubmittedResponsePage.productReportingContent(0)).$$(summaryValues)[0].getText()).toBe("100 kg");
    await expect(await $(ViewSubmittedResponsePage.productReportingContent(0)).$$(summaryValues)[1].getText()).toBe("200 kg");
    await expect(await $(ViewSubmittedResponsePage.productReportingContent(0)).$$(summaryItems)[3].getText()).toBe("Kitchen Equipment");
    await expect(await $(ViewSubmittedResponsePage.productReportingContent(0)).$$(summaryItems)[4].getText()).toBe("Volume of sales for Kitchen Equipment");
    await expect(await $(ViewSubmittedResponsePage.productReportingContent(0)).$$(summaryItems)[5].getText()).toBe(
      "Total volume produced for Kitchen Equipment",
    );
    await expect(await $(ViewSubmittedResponsePage.productReportingContent(0)).$$(summaryValues)[2].getText()).toBe("50 kg");
    await expect(await $(ViewSubmittedResponsePage.productReportingContent(0)).$$(summaryValues)[3].getText()).toBe("300 kg");
    await expect(await $(ViewSubmittedResponsePage.productReportingContent(0)).$$(summaryItems)[6].getText()).toBe("Groceries");
    await expect(await $(ViewSubmittedResponsePage.productReportingContent(0)).$$(summaryItems)[7].getText()).toBe("Volume of sales for Groceries");
    await expect(await $(ViewSubmittedResponsePage.productReportingContent(0)).$$(summaryItems)[8].getText()).toBe("Total volume produced for Groceries");
    await expect(await $(ViewSubmittedResponsePage.productReportingContent(0)).$$(summaryValues)[4].getText()).toBe("40 kg");
    await expect(await $(ViewSubmittedResponsePage.productReportingContent(0)).$$(summaryValues)[5].getText()).toBe("50 kg");
    await expect(await $(ViewSubmittedResponsePage.productReportingContent(1)).$$(summaryRowTitles)[0].getText()).toBe("Sales during the previous quarter");
    await expect(await $(ViewSubmittedResponsePage.productReportingContent(1)).$$(summaryItems)[0].getText()).toBe(
      "Value of sales for Articles and equipment for sports or outdoor games",
    );
    await expect(await $(ViewSubmittedResponsePage.productReportingContent(1)).$$(summaryItems)[1].getText()).toBe("Value of sales for Kitchen Equipment");
    await expect(await $(ViewSubmittedResponsePage.productReportingContent(1)).$$(summaryItems)[2].getText()).toBe("Value of sales for Groceries");
    await expect(await $(ViewSubmittedResponsePage.productReportingContent(1)).$$(summaryItems)[3].getText()).toBe("Value of sales from other categories");
    await expect(await $(ViewSubmittedResponsePage.productReportingContent(1)).$$(summaryValues)[0].getText()).toBe("£110.00");
    await expect(await $(ViewSubmittedResponsePage.productReportingContent(1)).$$(summaryValues)[1].getText()).toBe("£220.00");
    await expect(await $(ViewSubmittedResponsePage.productReportingContent(1)).$$(summaryValues)[2].getText()).toBe("£115.00");
    await expect(await $(ViewSubmittedResponsePage.productReportingContent(1)).$$(summaryValues)[3].getText()).toBe("£330.00");
  });
});
