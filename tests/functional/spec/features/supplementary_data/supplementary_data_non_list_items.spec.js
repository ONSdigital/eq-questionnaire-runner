import HubPage from "../../../base_pages/hub.page";
import IntroductionBlockPage from "../../../generated_pages/supplementary_data_non_list_items/introduction-block.page.js";
import Section1Page from "../../../generated_pages/supplementary_data_non_list_items/section-1-summary.page.js";
import EmailBlockPage from "../../../generated_pages/supplementary_data_non_list_items/email-block.page.js";
import NewEmailPage from "../../../generated_pages/supplementary_data_non_list_items/new-email.page.js";
import SalesBreakdownBlockPage from "../../../generated_pages/supplementary_data_non_list_items/sales-breakdown-block.page.js";
import CalculatedSummarySalesPage from "../../../generated_pages/supplementary_data_non_list_items/calculated-summary-sales.page.js";
import Section1InterstitialPage from "../../../generated_pages/supplementary_data_non_list_items/section-1-interstitial.page.js";

describe("Using supplementary data non list items", () => {
  before("Starting the survey", async () => {
    await browser.openQuestionnaire("test_supplementary_data_non_list_items.json", {
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
  });
});
