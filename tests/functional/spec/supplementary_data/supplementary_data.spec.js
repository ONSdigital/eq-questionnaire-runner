import { assertSummaryItems, assertSummaryTitles, assertSummaryValues, listItemComplete, click, verifyUrlContains } from "../../helpers";
import { expect } from "@wdio/globals";
import { getRandomString } from "../../jwt_helper";
import AddAdditionalEmployeePage from "../../generated_pages/supplementary_data/list-collector-additional-add.page.js";
import AdditionalLengthOfEmploymentPage from "../../generated_pages/supplementary_data/additional-length-of-employment.page.js";
import AnyAdditionalEmployeesPage from "../../generated_pages/supplementary_data/any-additional-employees.page.js";
import CalculatedSummarySalesPage from "../../generated_pages/supplementary_data/calculated-summary-sales.page.js";
import CalculatedSummaryValueSalesPage from "../../generated_pages/supplementary_data/calculated-summary-value-sales.page.js";
import CalculatedSummaryVolumeSalesPage from "../../generated_pages/supplementary_data/calculated-summary-volume-sales.page.js";
import CalculatedSummaryVolumeTotalPage from "../../generated_pages/supplementary_data/calculated-summary-volume-total.page.js";
import DynamicProductsPage from "../../generated_pages/supplementary_data/dynamic-products.page.js";
import EmailBlockPage from "../../generated_pages/supplementary_data/email-block.page.js";
import HubPage from "../../base_pages/hub.page";
import IntroductionBlockPage from "../../generated_pages/supplementary_data/introduction-block.page.js";
import LengthOfEmploymentPage from "../../generated_pages/supplementary_data/length-of-employment.page.js";
import ListCollectorAdditionalPage from "../../generated_pages/supplementary_data/list-collector-additional.page.js";
import ListCollectorEmployeesPage from "../../generated_pages/supplementary_data/list-collector-employees.page.js";
import ListCollectorProductsPage from "../../generated_pages/supplementary_data/list-collector-products.page.js";
import LoadedSuccessfullyBlockPage from "../../generated_pages/supplementary_data/loaded-successfully-block.page.js";
import NewEmailPage from "../../generated_pages/supplementary_data/new-email.page.js";
import ProductQuestion3EnabledPage from "../../generated_pages/supplementary_data/product-question-3-enabled.page";
import ProductRepeatingBlock1Page from "../../generated_pages/supplementary_data/product-repeating-block-1-repeating-block.page.js";
import ProductSalesInterstitialPage from "../../generated_pages/supplementary_data/product-sales-interstitial.page";
import ProductVolumeInterstitialPage from "../../generated_pages/supplementary_data/product-volume-interstitial.page";
import SalesBreakdownBlockPage from "../../generated_pages/supplementary_data/sales-breakdown-block.page.js";
import Section1InterstitialPage from "../../generated_pages/supplementary_data/section-1-interstitial.page.js";
import Section1Page from "../../generated_pages/supplementary_data/section-1-summary.page.js";
import Section3Page from "../../generated_pages/supplementary_data/section-3-summary.page.js";
import Section4Page from "../../generated_pages/supplementary_data/section-4-summary.page.js";
import Section5Page from "../../generated_pages/supplementary_data/section-5-summary.page.js";
import Section6Page from "../../generated_pages/supplementary_data/section-6-summary.page.js";
import ThankYouPage from "../../base_pages/thank-you.page";
import TradingPage from "../../generated_pages/supplementary_data/trading.page.js";
import ViewSubmittedResponsePage from "../../generated_pages/supplementary_data/view-submitted-response.page.js";

describe("Using supplementary data", () => {
  const responseId = getRandomString(16);
  const summaryItems = ".ons-summary__item--text";
  const summaryValues = ".ons-summary__values";
  const summaryRowTitles = ".ons-summary__row-title";

  before("Starting the survey", () => {
    browser.openQuestionnaire("test_supplementary_data.json", {
      version: "v2",
      sdsDatasetId: "203b2f9d-c500-8175-98db-86ffcfdccfa3",
      responseId,
    });
  });
  it("Given I launch a survey using supplementary data, When I am outside a repeating section, Then I am able to see the list of items relating to a given supplementary data list item on the page", () => {
    expect($("#main-content #guidance-1").getText()).toContain("The surnames of the employees are: Potter, Kent.");
    expect($$("#main-content li")[0].getText()).toBe("Articles and equipment for sports or outdoor games");
    expect($$("#main-content li")[1].getText()).toBe("Kitchen Equipment");
  });

  it("Given I progress through the interstitial block, When I begin the introduction block, Then I see the supplementary data piped in", () => {
    click(LoadedSuccessfullyBlockPage.submit());
    $(IntroductionBlockPage.acceptCookies()).click();
    expect($(IntroductionBlockPage.businessDetailsContent()).getText()).toContain("You are completing this survey for Tesco");
    expect($(IntroductionBlockPage.businessDetailsContent()).getText()).toContain(
      "If the company details or structure have changed contact us on 01171231231",
    );
    expect($(IntroductionBlockPage.guidancePanel(1)).getText()).toContain("Some supplementary guidance about the survey");
    click(IntroductionBlockPage.submit());
    click(HubPage.submit());
    $(EmailBlockPage.yes()).click();
    click(EmailBlockPage.submit());
  });

  it("Given I have dynamic answer options based off a supplementary date value, When I reach the block using them, Then I see a correct list of options to choose from", () => {
    expect($(TradingPage.answerLabelByIndex(0)).getText()).toBe("Thursday 27 November 1947");
    expect($(TradingPage.answerLabelByIndex(1)).getText()).toBe("Friday 28 November 1947");
    expect($(TradingPage.answerLabelByIndex(2)).getText()).toBe("Saturday 29 November 1947");
    expect($(TradingPage.answerLabelByIndex(3)).getText()).toBe("Sunday 30 November 1947");
    expect($(TradingPage.answerLabelByIndex(4)).getText()).toBe("Monday 1 December 1947");
    expect($(TradingPage.answerLabelByIndex(5)).getText()).toBe("Tuesday 2 December 1947");
    expect($(TradingPage.answerLabelByIndex(6)).getText()).toBe("Wednesday 3 December 1947");
    $(TradingPage.answerByIndex(3)).click();
    click(TradingPage.submit());
  });

  it("Given I have a calculated question validated against a supplementary data value, When I enter a breakdown that exceeds the total, Then I see an error message", () => {
    $(SalesBreakdownBlockPage.salesBristol()).setValue(333000);
    $(SalesBreakdownBlockPage.salesLondon()).setValue(444000);
    click(SalesBreakdownBlockPage.submit());
    expect($(SalesBreakdownBlockPage.errorNumber(1)).getText()).toContain("Enter answers that add up to or are less than 555,000");
  });

  it("Given I have a calculated question validated against a supplementary data value, When I enter a breakdown less than the total, Then I see a calculated summary page with the sum of my previous answers", () => {
    $(SalesBreakdownBlockPage.salesLondon()).setValue(111000);
    click(SalesBreakdownBlockPage.submit());
    expect($(CalculatedSummarySalesPage.calculatedSummaryTitle()).getText()).toBe(
      "Total value of sales from Bristol and London is calculated to be £444,000.00. Is this correct?",
    );
  });

  it("Given I have an interstitial block with all answers and supplementary data, When I reach this block, Then I see the placeholders rendered correctly", () => {
    click(CalculatedSummarySalesPage.submit());
    expect($(Section1InterstitialPage.questionText()).getText()).toContain("Summary of information provided for Tesco");
    expect($("body").getText()).toContain("Telephone Number: 01171231231");
    expect($("body").getText()).toContain("Email: contact@tesco.org");
    expect($("body").getText()).toContain("Note Title: Value of total sales");
    expect($("body").getText()).toContain("Note Description: Total value of goods sold during the period of the return");
    expect($("body").getText()).toContain("Note Example Title: Including");
    expect($("body").getText()).toContain("Note Example Description: Sales across all UK stores");
    expect($("body").getText()).toContain("Incorporation Date: 27 November 1947");
    expect($("body").getText()).toContain("Trading start date: 30 November 1947");
    expect($("body").getText()).toContain("Guidance: Some supplementary guidance about the survey");
    expect($("body").getText()).toContain("Total Uk Sales: £555,000.00");
    expect($("body").getText()).toContain("Bristol sales: £333,000.00");
    expect($("body").getText()).toContain("London sales: £111,000.00");
    expect($("body").getText()).toContain("Sum of Bristol and London sales: £444,000.00");
  });

  it("Given I have a section summary enabled, When I reach the section summary, Then I see it rendered correctly with supplementary data", () => {
    click(Section1InterstitialPage.submit());
    expect($(Section1Page.emailQuestion()).getText()).toBe("Is contact@tesco.org still the correct contact email for Tesco?");
    expect($(Section1Page.sameEmailAnswer()).getText()).toBe("Yes");
    expect($(Section1Page.tradingQuestion()).getText()).toBe("When did Tesco begin trading?");
    expect($(Section1Page.tradingAnswer()).getText()).toBe("Sunday 30 November 1947");
    expect($$(summaryRowTitles)[0].getText()).toBe("How much of the £555,000.00 total UK sales was from Bristol and London?");
    expect($(Section1Page.salesBristolAnswer()).getText()).toBe("£333,000.00");
    expect($(Section1Page.salesLondonAnswer()).getText()).toBe("£111,000.00");
  });

  it("Given I add an answer used in a first non empty item transform with supplementary data, When I return to the interstitial block, Then I see the transform value has updated", () => {
    $(Section1Page.sameEmailAnswerEdit()).click();
    $(EmailBlockPage.no()).click();
    click(EmailBlockPage.submit());
    $(NewEmailPage.answer()).setValue("new.contact@gmail.com");
    click(NewEmailPage.submit());
    $(Section1Page.previous()).click();
    expect($("body").getText()).toContain("Email: new.contact@gmail.com");
    click(Section1InterstitialPage.submit());
    click(Section1Page.submit());
  });

  it("Given I have a list collector content block using a supplementary list, When I start the section, I see the supplementary list items in the list", () => {
    click(HubPage.submit());
    expect($(ListCollectorEmployeesPage.listLabel(1)).getText()).toBe("Harry Potter");
    expect($(ListCollectorEmployeesPage.listLabel(2)).getText()).toBe("Clark Kent");
    click(ListCollectorEmployeesPage.submit());
  });

  it("Given I add some additional employees via another list collector, When I return to the Hub, Then I see new enabled sections for the supplementary list items and my added ones", () => {
    click(HubPage.submit());
    $(AnyAdditionalEmployeesPage.yes()).click();
    click(AnyAdditionalEmployeesPage.submit());
    $(AddAdditionalEmployeePage.employeeFirstName()).setValue("Jane");
    $(AddAdditionalEmployeePage.employeeLastName()).setValue("Doe");
    click(AddAdditionalEmployeePage.submit());
    $(ListCollectorAdditionalPage.yes()).click();
    click(ListCollectorAdditionalPage.submit());
    $(AddAdditionalEmployeePage.employeeFirstName()).setValue("John");
    $(AddAdditionalEmployeePage.employeeLastName()).setValue("Smith");
    click(AddAdditionalEmployeePage.submit());
    $(ListCollectorAdditionalPage.no()).click();
    click(ListCollectorAdditionalPage.submit());
    click(Section3Page.submit());
    expect($(HubPage.summaryItems("section-4-1")).getText()).toContain("Harry Potter");
    expect($(HubPage.summaryItems("section-4-2")).getText()).toContain("Clark Kent");
    expect($(HubPage.summaryItems("section-5-1")).getText()).toContain("Jane Doe");
    expect($(HubPage.summaryItems("section-5-2")).getText()).toContain("John Smith");
    click(HubPage.submit());
  });

  it("Given I have repeating sections for both supplementary and dynamic list items, When I start a repeating section for a supplementary list item, Then I see static supplementary data correctly piped in", () => {
    expect($(LengthOfEmploymentPage.questionTitle()).getText()).toContain("When did Harry Potter start working for Tesco?");
    expect($(LengthOfEmploymentPage.employmentStartLegend()).getText()).toContain("Start date at Tesco");
  });

  it("Given I have validation on the start date in the repeating section, When I enter a date before the incorporation date, Then I see an error message", () => {
    $(LengthOfEmploymentPage.day()).setValue(1);
    $(LengthOfEmploymentPage.month()).setValue(1);
    $(LengthOfEmploymentPage.year()).setValue(1930);
    click(LengthOfEmploymentPage.submit());
    expect($(LengthOfEmploymentPage.singleErrorLink()).getText()).toBe("Enter a date after 26 November 1947");
  });

  it("Given I have validation on the start date in the repeating section, When I enter a date after the incorporation date, Then I see that date on the summary page for the section", () => {
    $(LengthOfEmploymentPage.year()).setValue(1990);
    click(LengthOfEmploymentPage.submit());
    expect($(Section4Page.lengthEmploymentQuestion()).getText()).toBe("When did Harry Potter start working for Tesco?");
    expect($(Section4Page.employmentStart()).getText()).toBe("1 January 1990");
  });

  it("Given I complete the repeating section for another supplementary item, When I reach the summary page, Then I see the correct supplementary data with my answers", () => {
    click(Section4Page.submit());
    click(HubPage.submit());
    expect($(LengthOfEmploymentPage.questionTitle()).getText()).toContain("When did Clark Kent start working for Tesco?");
    $(LengthOfEmploymentPage.day()).setValue(5);
    $(LengthOfEmploymentPage.month()).setValue(6);
    $(LengthOfEmploymentPage.year()).setValue(2011);
    click(LengthOfEmploymentPage.submit());
    expect($(Section4Page.lengthEmploymentQuestion()).getText()).toBe("When did Clark Kent start working for Tesco?");
    expect($(Section4Page.employmentStart()).getText()).toBe("5 June 2011");
  });

  it("Given I move onto the dynamic list items, When I start a repeating section for a dynamic list item, Then I see static supplementary data correctly piped in and the same validation and summary", () => {
    click(Section4Page.submit());
    click(HubPage.submit());
    expect($(AdditionalLengthOfEmploymentPage.questionTitle()).getText()).toContain("When did Jane Doe start working for Tesco?");
    expect($(AdditionalLengthOfEmploymentPage.additionalEmploymentStartLegend()).getText()).toBe("Start date at Tesco");
    $(AdditionalLengthOfEmploymentPage.day()).setValue(1);
    $(AdditionalLengthOfEmploymentPage.month()).setValue(1);
    $(AdditionalLengthOfEmploymentPage.year()).setValue(1930);
    click(AdditionalLengthOfEmploymentPage.submit());
    expect($(AdditionalLengthOfEmploymentPage.singleErrorLink()).getText()).toBe("Enter a date after 26 November 1947");
    $(AdditionalLengthOfEmploymentPage.year()).setValue(2000);
    click(AdditionalLengthOfEmploymentPage.submit());
    expect($(Section5Page.additionalLengthEmploymentQuestion()).getText()).toBe("When did Jane Doe start working for Tesco?");
    expect($(Section5Page.additionalEmploymentStart()).getText()).toBe("1 January 2000");
    click(Section5Page.submit());
    click(HubPage.submit());
    $(AdditionalLengthOfEmploymentPage.day()).setValue(3);
    $(AdditionalLengthOfEmploymentPage.month()).setValue(3);
    $(AdditionalLengthOfEmploymentPage.year()).setValue(2010);
    click(AdditionalLengthOfEmploymentPage.submit());
    expect($(Section5Page.additionalLengthEmploymentQuestion()).getText()).toBe("When did John Smith start working for Tesco?");
    expect($(Section5Page.additionalEmploymentStart()).getText()).toBe("3 March 2010");
    click(Section5Page.submit());
  });

  it("Given I have some repeating blocks with supplementary data, When I begin the section, Then I see the supplementary names rendered correctly", () => {
    click(HubPage.submit());
    expect($(ListCollectorProductsPage.listLabel(1)).getText()).toBe("Articles and equipment for sports or outdoor games");
    expect($(ListCollectorProductsPage.listLabel(2)).getText()).toBe("Kitchen Equipment");
    click(ListCollectorProductsPage.submit());
  });

  it("Given I have repeating blocks with supplementary data, When I start the first repeating block, Then I see the supplementary data for the first list item", () => {
    expect($("body").getHTML()).toContain("<h2>Include</h2>");
    expect($("body").getHTML()).toContain("<li>for children's playgrounds</li>");
    expect($("body").getHTML()).toContain("<li>swimming pools and paddling pools</li>");
    expect($("body").getHTML()).toContain("<h2>Exclude</h2>");
    expect($("body").getHTML()).toContain(
      "<li>sports holdalls, gloves, clothing of textile materials, footwear, protective eyewear, rackets, balls, skates</li>",
    );
    expect($("body").getHTML()).toContain(
      "<li>for skiing, water sports, golf, fishing', for skiing, water sports, golf, fishing, table tennis, PE, gymnastics, athletics</li>",
    );
    expect($(ProductRepeatingBlock1Page.productVolumeSalesLabel()).getText()).toBe(
      "Volume of sales for Articles and equipment for sports or outdoor games",
    );
    expect($(ProductRepeatingBlock1Page.productVolumeTotalLabel()).getText()).toBe(
      "Total volume produced for Articles and equipment for sports or outdoor games",
    );
    $(ProductRepeatingBlock1Page.productVolumeSales()).setValue(100);
    $(ProductRepeatingBlock1Page.productVolumeTotal()).setValue(200);
  });

  it("Given I have repeating blocks with supplementary data, When I start the second repeating block, Then I see the supplementary data for the second list item", () => {
    click(ProductRepeatingBlock1Page.submit());
    click(ListCollectorProductsPage.submit());
    expect($("body").getText()).toContain("Include");
    expect($("body").getText()).toContain("pots and pans");
    expect($("body").getText()).not.toBe("Exclude");
    expect($(ProductRepeatingBlock1Page.productVolumeSalesLabel()).getText()).toBe("Volume of sales for Kitchen Equipment");
    expect($(ProductRepeatingBlock1Page.productVolumeTotalLabel()).getText()).toBe("Total volume produced for Kitchen Equipment");
    $(ProductRepeatingBlock1Page.productVolumeSales()).setValue(50);
    $(ProductRepeatingBlock1Page.productVolumeTotal()).setValue(300);
    click(ProductRepeatingBlock1Page.submit());
  });

  it("Given I have a calculated summary using the repeating blocks, When I reach the Calculated Summary, Then I see the correct total and supplementary data labels", () => {
    click(ListCollectorProductsPage.submit());
    verifyUrlContains(CalculatedSummaryVolumeSalesPage.pageName);
    expect($(CalculatedSummaryVolumeSalesPage.calculatedSummaryTitle()).getText()).toBe(
      "We calculate the total volume of sales over the previous quarter to be 150 kg. Is this correct?",
    );
    assertSummaryItems([
      "Volume of sales for Articles and equipment for sports or outdoor games",
      "Volume of sales for Kitchen Equipment",
      "Total sales volume",
    ]);
    assertSummaryValues(["100 kg", "50 kg", "150 kg"]);
    click(CalculatedSummaryVolumeSalesPage.submit());
  });

  it("Given I have another calculated summary using the repeating blocks, When I reach the Calculated Summary, Then I see the correct total and supplementary data labels", () => {
    expect($(CalculatedSummaryVolumeTotalPage.calculatedSummaryTitle()).getText()).toBe(
      "We calculate the total volume produced over the previous quarter to be 500 kg. Is this correct?",
    );
    assertSummaryItems([
      "Total volume produced for Articles and equipment for sports or outdoor games",
      "Total volume produced for Kitchen Equipment",
      "Total volume produced",
    ]);
    assertSummaryValues(["200 kg", "300 kg", "500 kg"]);
    click(CalculatedSummaryVolumeTotalPage.submit());
  });

  it("Given I have dynamic answers using a supplementary list, When I reach the dynamic answer page, Then I see the correct supplementary data in the answer labels", () => {
    expect($$(DynamicProductsPage.labels())[0].getText()).toBe("Value of sales for Articles and equipment for sports or outdoor games");
    expect($$(DynamicProductsPage.labels())[1].getText()).toBe("Value of sales for Kitchen Equipment");
    expect($$(DynamicProductsPage.labels())[2].getText()).toBe("Value of sales from other categories");
    $$(DynamicProductsPage.inputs())[0].setValue(110);
    $$(DynamicProductsPage.inputs())[1].setValue(220);
    $$(DynamicProductsPage.inputs())[2].setValue(330);
    click(DynamicProductsPage.submit());
  });

  it("Given I have a calculated summary of dynamic answers for a supplementary list, When I reach the calculated summary, Then I see the correct supplementary data in the title and labels", () => {
    expect($(CalculatedSummaryValueSalesPage.calculatedSummaryTitle()).getText()).toBe(
      "We calculate the total value of sales over the previous quarter to be £660.00. Is this correct?",
    );
    assertSummaryItems([
      "Value of sales for Articles and equipment for sports or outdoor games",
      "Value of sales for Kitchen Equipment",
      "Value of sales from other categories",
      "Total sales value",
    ]);
    assertSummaryValues(["£110.00", "£220.00", "£330.00", "£660.00"]);
    click(CalculatedSummaryValueSalesPage.submit());
  });

  it("Given I have a section with repeating answers for a supplementary list, When I reach the section summary page, Then I see the supplementary data and my answers rendered correctly", () => {
    expect($$(summaryRowTitles)[0].getText()).toBe("Sales during the previous quarter");
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
    assertSummaryValues(["100 kg", "200 kg", "50 kg", "300 kg", "£110.00", "£220.00", "£330.00"]);
    click(Section6Page.submit());
    expect($(HubPage.summaryRowState("section-6")).getText()).toBe("Completed");
  });

  it("Given I am using a supplementary dataset where the size of one of the lists skips a question in a section, When I enter the section, Then I only see an interstitial block as the other block is skipped", () => {
    $(HubPage.summaryRowLink("section-8")).click();
    verifyUrlContains(ProductVolumeInterstitialPage.pageName);
    click(ProductVolumeInterstitialPage.submit());
    expect($(HubPage.summaryRowState("section-8")).getText()).toBe("Completed");
  });

  it("Given I relaunch the survey with new supplementary data and new list items for the repeating section, When I open the Hub page, Then I see the new supplementary list items as new incomplete sections and not any old ones", () => {
    browser.openQuestionnaire("test_supplementary_data.json", {
      version: "v2",
      sdsDatasetId: "3bb41d29-4daa-9520-82f0-cae365f390c6",
      responseId,
    });
    expect($(HubPage.summaryItems("section-4-1")).getText()).toContain("Harry Potter");
    expect($(HubPage.summaryItems("section-4-2")).getText()).toContain("Bruce Wayne");
    expect($(HubPage.summaryItems("section-5-1")).getText()).toContain("Jane Doe");
    expect($(HubPage.summaryItems("section-5-2")).getText()).toContain("John Smith");
    expect($(HubPage.summaryRowState("section-4-1")).getText()).toBe("Completed");
    expect($(HubPage.summaryRowState("section-4-2")).getText()).toBe("Not started");
    expect($(HubPage.summaryRowState("section-5-1")).getText()).toBe("Completed");
    expect($(HubPage.summaryRowState("section-5-2")).getText()).toBe("Completed");
    expect($("body").getText()).not.toContain("Clark Kent");
  });

  it("Given the survey has been relaunched with new data and more items in the products list, When I am on the Hub, Then I see the products section and section with a new block due to the product list size are both in progress", () => {
    expect($(HubPage.summaryRowState("section-6")).getText()).toBe("Partially completed");
    expect($(HubPage.summaryRowState("section-8")).getText()).toBe("Partially completed");
  });

  it("Given I am using a supplementary dataset with a product list size that skips a question in the sales target section, When I enter the section, Then I only see an interstitial block", () => {
    $(HubPage.summaryRowLink("section-7")).click();
    verifyUrlContains(ProductSalesInterstitialPage.pageName);
    click(ProductSalesInterstitialPage.submit());
    expect($(HubPage.summaryRowState("section-7")).getText()).toBe("Completed");
  });

  it("Given there is now an additional product, When I resume the Product Details Section, Then I start from the list collector content block and see the new product is incomplete", () => {
    $(HubPage.summaryRowLink("section-6")).click();
    verifyUrlContains(ListCollectorProductsPage.pageName);
    listItemComplete(`li[data-qa="list-item-1-label"]`, true);
    listItemComplete(`li[data-qa="list-item-2-label"]`, true);
    listItemComplete(`li[data-qa="list-item-3-label"]`, false);
    click(ListCollectorProductsPage.submit());
    verifyUrlContains(ProductRepeatingBlock1Page.pageName);
  });

  it("Given I complete the section and relaunch with the old data that has fewer items in the products list, When I am on the Hub, Then I see the products section and sales targets sections are now in progress", () => {
    $(ProductRepeatingBlock1Page.productVolumeSales()).setValue(40);
    $(ProductRepeatingBlock1Page.productVolumeTotal()).setValue(50);
    click(ProductRepeatingBlock1Page.submit());
    click(ListCollectorProductsPage.submit());
    click(CalculatedSummaryVolumeSalesPage.submit());
    click(CalculatedSummaryVolumeTotalPage.submit());
    $$(DynamicProductsPage.inputs())[2].setValue(115);
    click(DynamicProductsPage.submit());
    click(CalculatedSummaryValueSalesPage.submit());
    click(Section6Page.submit());
    expect($(HubPage.summaryRowState("section-6")).getText()).toBe("Completed");
    browser.openQuestionnaire("test_supplementary_data.json", {
      version: "v2",
      sdsDatasetId: "203b2f9d-c500-8175-98db-86ffcfdccfa3",
      responseId,
    });
    expect($(HubPage.summaryRowState("section-6")).getText()).toBe("Partially completed");
    expect($(HubPage.summaryRowState("section-7")).getText()).toBe("Partially completed");
  });

  it("Given I return to the new data resulting in a new incomplete section, When I start the section, Then I see the new supplementary data piped in accordingly", () => {
    browser.openQuestionnaire("test_supplementary_data.json", {
      version: "v2",
      sdsDatasetId: "3bb41d29-4daa-9520-82f0-cae365f390c6",
      responseId,
    });
    click(HubPage.submit());
    $(LengthOfEmploymentPage.day()).setValue(10);
    $(LengthOfEmploymentPage.month()).setValue(10);
    $(LengthOfEmploymentPage.year()).setValue(1999);
    click(LengthOfEmploymentPage.submit());
    expect($(Section4Page.lengthEmploymentQuestion()).getText()).toBe("When did Bruce Wayne start working for Lidl?");
    expect($(Section4Page.employmentStart()).getText()).toBe("10 October 1999");
    click(Section4Page.submit());
  });

  it("Given I can view my response after submission, When I submit the survey, Then I see the values I've entered and correct rendering with supplementary data", () => {
    click(HubPage.submit());
    click(ListCollectorProductsPage.submit());
    $(ProductRepeatingBlock1Page.productVolumeSales()).setValue(40);
    $(ProductRepeatingBlock1Page.productVolumeTotal()).setValue(50);
    click(ProductRepeatingBlock1Page.submit());
    click(ListCollectorProductsPage.submit());
    click(CalculatedSummaryVolumeSalesPage.submit());
    click(CalculatedSummaryVolumeTotalPage.submit());
    $$(DynamicProductsPage.inputs())[2].setValue(115);
    click(DynamicProductsPage.submit());
    click(CalculatedSummaryValueSalesPage.submit());
    click(Section6Page.submit());
    click(HubPage.submit());
    $(ProductQuestion3EnabledPage.yes()).click();
    click(ProductQuestion3EnabledPage.submit());
    click(HubPage.submit());
    $(ThankYouPage.savePrintAnswersLink()).click();

    assertSummaryTitles([
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
    expect($(ViewSubmittedResponsePage.emailQuestion()).getText()).toBe("Is contact@lidl.org still the correct contact email for Lidl?");
    expect($(ViewSubmittedResponsePage.sameEmailAnswer()).getText()).toBe("No");
    expect($(ViewSubmittedResponsePage.newEmailQuestion()).getText()).toBe("What is the new contact email for Lidl?");
    expect($(ViewSubmittedResponsePage.newEmailAnswer()).getText()).toBe("new.contact@gmail.com");
    expect($(ViewSubmittedResponsePage.tradingQuestion()).getText()).toBe("When did Lidl begin trading?");
    expect($(ViewSubmittedResponsePage.tradingAnswer()).getText()).toBe("Sunday 30 November 1947");
    expect($$(summaryRowTitles)[0].getText()).toBe("How much of the £555,000.00 total UK sales was from Bristol and London?");
    expect($(ViewSubmittedResponsePage.salesBristolAnswer()).getText()).toBe("£333,000.00");
    expect($(ViewSubmittedResponsePage.salesLondonAnswer()).getText()).toBe("£111,000.00");

    // Additional Employees
    expect($(ViewSubmittedResponsePage.anyAdditionalEmployeeQuestion()).getText()).toBe("Do you have any additional employees to report on?");
    expect($(ViewSubmittedResponsePage.anyAdditionalEmployeeAnswer()).getText()).toBe("Yes");
    expect($(ViewSubmittedResponsePage.additionalEmployeeReportingContent(1)).$$(summaryItems)[0].getText()).toBe("Jane Doe");
    expect($(ViewSubmittedResponsePage.additionalEmployeeReportingContent(1)).$$(summaryItems)[1].getText()).toBe("John Smith");

    // Harry Potter
    expect($(ViewSubmittedResponsePage.employeeDetailQuestionsContent(0)).$$(summaryItems)[0].getText()).toBe(
      "When did Harry Potter start working for Lidl?",
    );
    expect($(ViewSubmittedResponsePage.employeeDetailQuestionsContent(0)).$$(summaryValues)[0].getText()).toBe("1 January 1990");

    // Bruce Wayne
    expect($(ViewSubmittedResponsePage.employeeDetailQuestionsContent("0-1")).$$(summaryItems)[0].getText()).toBe(
      "When did Bruce Wayne start working for Lidl?",
    );
    expect($(ViewSubmittedResponsePage.employeeDetailQuestionsContent("0-1")).$$(summaryValues)[0].getText()).toBe("10 October 1999");

    // Jane Doe
    expect($(ViewSubmittedResponsePage.additionalEmployeeDetailQuestionsContent(0)).$$(summaryItems)[0].getText()).toBe(
      "When did Jane Doe start working for Lidl?",
    );
    expect($(ViewSubmittedResponsePage.additionalEmployeeDetailQuestionsContent(0)).$$(summaryValues)[0].getText()).toBe("1 January 2000");

    // John Smith
    expect($(ViewSubmittedResponsePage.additionalEmployeeDetailQuestionsContent("0-2")).$$(summaryItems)[0].getText()).toBe(
      "When did John Smith start working for Lidl?",
    );
    expect($(ViewSubmittedResponsePage.additionalEmployeeDetailQuestionsContent("0-2")).$$(summaryValues)[0].getText()).toBe("3 March 2010");

    // Product details
    expect($(ViewSubmittedResponsePage.productReportingContent(0)).$$(summaryItems)[0].getText()).toBe(
      "Articles and equipment for sports or outdoor games",
    );
    expect($(ViewSubmittedResponsePage.productReportingContent(0)).$$(summaryItems)[1].getText()).toBe(
      "Volume of sales for Articles and equipment for sports or outdoor games",
    );
    expect($(ViewSubmittedResponsePage.productReportingContent(0)).$$(summaryItems)[2].getText()).toBe(
      "Total volume produced for Articles and equipment for sports or outdoor games",
    );
    expect($(ViewSubmittedResponsePage.productReportingContent(0)).$$(summaryValues)[0].getText()).toBe("100 kg");
    expect($(ViewSubmittedResponsePage.productReportingContent(0)).$$(summaryValues)[1].getText()).toBe("200 kg");
    expect($(ViewSubmittedResponsePage.productReportingContent(0)).$$(summaryItems)[3].getText()).toBe("Kitchen Equipment");
    expect($(ViewSubmittedResponsePage.productReportingContent(0)).$$(summaryItems)[4].getText()).toBe("Volume of sales for Kitchen Equipment");
    expect($(ViewSubmittedResponsePage.productReportingContent(0)).$$(summaryItems)[5].getText()).toBe(
      "Total volume produced for Kitchen Equipment",
    );
    expect($(ViewSubmittedResponsePage.productReportingContent(0)).$$(summaryValues)[2].getText()).toBe("50 kg");
    expect($(ViewSubmittedResponsePage.productReportingContent(0)).$$(summaryValues)[3].getText()).toBe("300 kg");
    expect($(ViewSubmittedResponsePage.productReportingContent(0)).$$(summaryItems)[6].getText()).toBe("Groceries");
    expect($(ViewSubmittedResponsePage.productReportingContent(0)).$$(summaryItems)[7].getText()).toBe("Volume of sales for Groceries");
    expect($(ViewSubmittedResponsePage.productReportingContent(0)).$$(summaryItems)[8].getText()).toBe("Total volume produced for Groceries");
    expect($(ViewSubmittedResponsePage.productReportingContent(0)).$$(summaryValues)[4].getText()).toBe("40 kg");
    expect($(ViewSubmittedResponsePage.productReportingContent(0)).$$(summaryValues)[5].getText()).toBe("50 kg");
    expect($(ViewSubmittedResponsePage.productReportingContent(1)).$$(summaryRowTitles)[0].getText()).toBe("Sales during the previous quarter");
    expect($(ViewSubmittedResponsePage.productReportingContent(1)).$$(summaryItems)[0].getText()).toBe(
      "Value of sales for Articles and equipment for sports or outdoor games",
    );
    expect($(ViewSubmittedResponsePage.productReportingContent(1)).$$(summaryItems)[1].getText()).toBe("Value of sales for Kitchen Equipment");
    expect($(ViewSubmittedResponsePage.productReportingContent(1)).$$(summaryItems)[2].getText()).toBe("Value of sales for Groceries");
    expect($(ViewSubmittedResponsePage.productReportingContent(1)).$$(summaryItems)[3].getText()).toBe("Value of sales from other categories");
    expect($(ViewSubmittedResponsePage.productReportingContent(1)).$$(summaryValues)[0].getText()).toBe("£110.00");
    expect($(ViewSubmittedResponsePage.productReportingContent(1)).$$(summaryValues)[1].getText()).toBe("£220.00");
    expect($(ViewSubmittedResponsePage.productReportingContent(1)).$$(summaryValues)[2].getText()).toBe("£115.00");
    expect($(ViewSubmittedResponsePage.productReportingContent(1)).$$(summaryValues)[3].getText()).toBe("£330.00");
  });
});
