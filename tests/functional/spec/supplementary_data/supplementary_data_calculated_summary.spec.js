import { assertSummaryItems, assertSummaryTitles, assertSummaryValues, listItemComplete, click, verifyUrlContains } from "../../helpers";
import { expect } from "@wdio/globals";
import { getRandomString } from "../../jwt_helper";
import CalculatedSummaryValueSalesPage from "../../generated_pages/supplementary_data/calculated-summary-value-sales.page.js";
import CalculatedSummaryVolumeSalesPage from "../../generated_pages/supplementary_data/calculated-summary-volume-sales.page.js";
import CalculatedSummaryVolumeTotalPage from "../../generated_pages/supplementary_data/calculated-summary-volume-total.page.js";
import DynamicProductsPage from "../../generated_pages/supplementary_data/dynamic-products.page.js";
import HubPage from "../../base_pages/hub.page";
import LengthOfEmploymentPage from "../../generated_pages/supplementary_data/length-of-employment.page.js";
import ListCollectorProductsPage from "../../generated_pages/supplementary_data/list-collector-products.page.js";
import ProductQuestion3EnabledPage from "../../generated_pages/supplementary_data/product-question-3-enabled.page";
import ProductRepeatingBlock1Page from "../../generated_pages/supplementary_data/product-repeating-block-1-repeating-block.page.js";
import ProductSalesInterstitialPage from "../../generated_pages/supplementary_data/product-sales-interstitial.page";
import ProductVolumeInterstitialPage from "../../generated_pages/supplementary_data/product-volume-interstitial.page";
import Section4Page from "../../generated_pages/supplementary_data/section-4-summary.page.js";
import Section6Page from "../../generated_pages/supplementary_data/section-6-summary.page.js";
import ThankYouPage from "../../base_pages/thank-you.page";
import ViewSubmittedResponsePage from "../../generated_pages/supplementary_data/view-submitted-response.page.js";

describe("Using supplementary data", () => {
  const responseId = getRandomString(16);
  const summaryItems = ".ons-summary__item--text";
  const summaryValues = ".ons-summary__values";
  const summaryRowTitles = ".ons-summary__row-title";

  before("Starting the survey", async () => {
    await browser.openQuestionnaire("test_supplementary_data_with_skip_conditions_and_calculated_summary.json", {
      version: "v2",
      sdsDatasetId: "203b2f9d-c500-8175-98db-86ffcfdccfa3",
      responseId,
    });
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
    await verifyUrlContains(CalculatedSummaryVolumeSalesPage.pageName);
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
    await verifyUrlContains(ProductVolumeInterstitialPage.pageName);
    await click(ProductVolumeInterstitialPage.submit());
    await expect(await $(HubPage.summaryRowState("section-8")).getText()).toBe("Completed");
  });

  it("Given I relaunch the survey with new supplementary data and new list items for the repeating section, When I open the Hub page, Then I see the new supplementary list items as new incomplete sections and not any old ones", async () => {
    await browser.openQuestionnaire("test_supplementary_data.json", {
      version: "v2",
      sdsDatasetId: "3bb41d29-4daa-9520-82f0-cae365f390c6",
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
    await verifyUrlContains(ProductSalesInterstitialPage.pageName);
    await click(ProductSalesInterstitialPage.submit());
    await expect(await $(HubPage.summaryRowState("section-7")).getText()).toBe("Completed");
  });

  it("Given there is now an additional product, When I resume the Product Details Section, Then I start from the list collector content block and see the new product is incomplete", async () => {
    await $(HubPage.summaryRowLink("section-6")).click();
    await verifyUrlContains(ListCollectorProductsPage.pageName);
    await listItemComplete(`li[data-qa="list-item-1-label"]`, true);
    await listItemComplete(`li[data-qa="list-item-2-label"]`, true);
    await listItemComplete(`li[data-qa="list-item-3-label"]`, false);
    await click(ListCollectorProductsPage.submit());
    await verifyUrlContains(ProductRepeatingBlock1Page.pageName);
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
      sdsDatasetId: "203b2f9d-c500-8175-98db-86ffcfdccfa3",
      responseId,
    });
    await expect(await $(HubPage.summaryRowState("section-6")).getText()).toBe("Partially completed");
    await expect(await $(HubPage.summaryRowState("section-7")).getText()).toBe("Partially completed");
  });

  it("Given I return to the new data resulting in a new incomplete section, When I start the section, Then I see the new supplementary data piped in accordingly", async () => {
    await browser.openQuestionnaire("test_supplementary_data.json", {
      version: "v2",
      sdsDatasetId: "3bb41d29-4daa-9520-82f0-cae365f390c6",
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
