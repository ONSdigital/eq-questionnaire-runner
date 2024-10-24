import AddressDurationPage from "../../../generated_pages/section_summary/address-duration.page.js";
import HouseholdCountSectionSummaryPage from "../../../generated_pages/section_summary/household-count-section-summary.page.js";
import HouseholdDetailsSummaryPage from "../../../generated_pages/section_summary/house-details-section-summary.page.js";
import HouseType from "../../../generated_pages/section_summary/house-type.page.js";
import InsuranceAddressPage from "../../../generated_pages/section_summary/insurance-address.page.js";
import InsuranceTypePage from "../../../generated_pages/section_summary/insurance-type.page.js";
import ListedPage from "../../../generated_pages/section_summary/listed.page.js";
import NumberOfPeoplePage from "../../../generated_pages/section_summary/number-of-people.page.js";
import PropertyDetailsSummaryPage from "../../../generated_pages/section_summary/property-details-section-summary.page.js";
import SubmitPage from "../../../generated_pages/section_summary/submit.page.js";
import { click } from "../../../helpers";

describe("Section Summary", () => {
  describe("Given I start a Test Section Summary survey and complete to Section Summary", () => {
    beforeEach(async () => {
      await browser.openQuestionnaire("test_section_summary.json");
      await $(InsuranceTypePage.both()).click();
      await click(InsuranceTypePage.submit());
      await click(InsuranceAddressPage.submit());
      await click(ListedPage.submit());
      await expect(await $(PropertyDetailsSummaryPage.insuranceTypeAnswer()).getText()).toBe("Both");
    });

    it("When I get to the section summary page, Then the submit button should read 'Continue'", async () => {
      await expect(await $(PropertyDetailsSummaryPage.submit()).getText()).toBe("Continue");
    });

    it("When I have selected an answer to edit and edit it, Then I should return to the section summary with new value displayed", async () => {
      await $(PropertyDetailsSummaryPage.insuranceAddressAnswerEdit()).click();
      await $(InsuranceAddressPage.answer()).setValue("Test Address");
      await click(InsuranceAddressPage.submit());
      await expect(await $(PropertyDetailsSummaryPage.insuranceAddressAnswer()).getText()).toBe("Test Address");
    });

    it("When I select edit from the section summary and click previous on the question page, Then I should be taken back to the section summary", async () => {
      await $(PropertyDetailsSummaryPage.insuranceAddressAnswerEdit()).click();
      await $(InsuranceAddressPage.previous()).click();
      await expect(browser).toHaveUrl(expect.stringContaining(PropertyDetailsSummaryPage.url()));
    });

    it("When I continue on the section summary page, Then I should be taken to the next section", async () => {
      await click(PropertyDetailsSummaryPage.submit());
      await expect(browser).toHaveUrl(expect.stringContaining(HouseType.pageName));
    });

    it("When I select edit from Section Summary but change routing, Then I should step through the section and be returned to the Section Summary once all new questions have been answered", async () => {
      await $(PropertyDetailsSummaryPage.insuranceTypeAnswerEdit()).click();
      await $(InsuranceTypePage.contents()).click();
      await click(InsuranceTypePage.submit());
      await expect(browser).toHaveUrl(expect.stringContaining(AddressDurationPage.pageName));
      await click(AddressDurationPage.submit());
      await expect(browser).toHaveUrl(expect.stringContaining(PropertyDetailsSummaryPage.pageName));
    });

    it("When I select edit from Section Summary but change routing, Then using previous should not prevent me returning to the section summary once all new questions have been answered", async () => {
      await $(PropertyDetailsSummaryPage.insuranceTypeAnswerEdit()).click();
      await $(InsuranceTypePage.contents()).click();
      await click(InsuranceTypePage.submit());
      await expect(browser).toHaveUrl(expect.stringContaining(AddressDurationPage.pageName));
      await $(AddressDurationPage.previous()).click();
      await expect(browser).toHaveUrl(expect.stringContaining(InsuranceAddressPage.pageName));
      await click(InsuranceAddressPage.submit());
      await click(AddressDurationPage.submit());
      await expect(browser).toHaveUrl(expect.stringContaining(PropertyDetailsSummaryPage.pageName));
    });
  });

  describe("Given I start a Test Section Summary survey and complete to Final Summary", () => {
    beforeEach(async () => {
      await browser.openQuestionnaire("test_section_summary.json");
      await $(InsuranceTypePage.both()).click();
      await click(InsuranceTypePage.submit());
      await click(InsuranceAddressPage.submit());
      await click(ListedPage.submit());
      await click(PropertyDetailsSummaryPage.submit());
      await click(HouseType.submit());
      await click(HouseholdDetailsSummaryPage.submit());
      await $(NumberOfPeoplePage.answer()).setValue(3);
      await click(NumberOfPeoplePage.submit());
      await click(HouseholdCountSectionSummaryPage.submit());
      await expect(browser).toHaveUrl(expect.stringContaining(SubmitPage.url()));
    });

    it("When I select edit from Final Summary and don't change an answer, Then I should be taken to the Final Summary", async () => {
      await $(SubmitPage.summaryShowAllButton()).click();
      await $(SubmitPage.insuranceAddressAnswerEdit()).click();
      await click(InsuranceAddressPage.submit());
      await expect(browser).toHaveUrl(expect.stringContaining(SubmitPage.url()));
    });

    it("When I select edit from Final Summary and change an answer that doesn't affect completeness, Then I should be taken to the Final Summary", async () => {
      await $(SubmitPage.summaryShowAllButton()).click();
      await $(SubmitPage.insuranceAddressAnswerEdit()).click();
      await $(InsuranceAddressPage.answer()).setValue("Test Address");
      await click(InsuranceAddressPage.submit());
      await expect(browser).toHaveUrl(expect.stringContaining(SubmitPage.url()));
    });

    it("When I select edit from Final Summary but change routing, Then I should step through the section and be returned to the Final Summary once all new questions have been answered", async () => {
      await $(SubmitPage.summaryShowAllButton()).click();
      await $(SubmitPage.insuranceTypeAnswerEdit()).click();
      await $(InsuranceTypePage.contents()).click();
      await click(InsuranceTypePage.submit());
      await expect(browser).toHaveUrl(expect.stringContaining(AddressDurationPage.pageName));
      await click(AddressDurationPage.submit());
      await expect(browser).toHaveUrl(expect.stringContaining(SubmitPage.pageName));
    });

    it("When I select edit from Final Summary but change routing, Then using previous should not prevent me returning to the section summary once all new questions have been answered", async () => {
      await $(SubmitPage.summaryShowAllButton()).click();
      await $(SubmitPage.insuranceTypeAnswerEdit()).click();
      await $(InsuranceTypePage.contents()).click();
      await click(InsuranceTypePage.submit());
      await expect(browser).toHaveUrl(expect.stringContaining(AddressDurationPage.pageName));
      await $(AddressDurationPage.previous()).click();
      await expect(browser).toHaveUrl(expect.stringContaining(InsuranceAddressPage.pageName));
      await click(InsuranceAddressPage.submit());
      await click(AddressDurationPage.submit());
      await expect(browser).toHaveUrl(expect.stringContaining(SubmitPage.pageName));
    });
    it("When I select edit from Final Summary and change an answer and then go to the next question and click previous, Since I cannot return to the section summary yet I return to the previous block in the section", async () => {
      await $(SubmitPage.summaryShowAllButton()).click();
      await $(SubmitPage.insuranceTypeAnswerEdit()).click();
      await $(InsuranceTypePage.contents()).click();
      await click(InsuranceTypePage.submit());
      await $(AddressDurationPage.previous()).click();
      await expect(browser).toHaveUrl(expect.stringContaining(InsuranceAddressPage.pageName));
    });

    it("When I change an answer, Then the final summary should display the updated value", async () => {
      await $(SubmitPage.summaryShowAllButton()).click();
      await expect(await $(SubmitPage.insuranceAddressAnswer()).getText()).toBe("No answer provided");
      await $(SubmitPage.insuranceAddressAnswerEdit()).click();
      await expect(browser).toHaveUrl(expect.stringContaining(InsuranceAddressPage.pageName));
      await $(InsuranceAddressPage.answer()).setValue("Test Address");
      await click(InsuranceAddressPage.submit());
      await $(SubmitPage.summaryShowAllButton()).click();
      await expect(await $(SubmitPage.insuranceAddressAnswer()).getText()).toBe("Test Address");
    });
  });
  describe("Given I start the Test Section Summary questionnaire", () => {
    before(async () => {
      await browser.openQuestionnaire("test_section_summary.json");
    });
    it("When there is no title set in the sections summary, the section title is used for the section summary title", async () => {
      await $(InsuranceTypePage.both()).click();
      await click(InsuranceTypePage.submit());
      await click(InsuranceAddressPage.submit());
      await click(ListedPage.submit());
      await expect(await $(PropertyDetailsSummaryPage.heading()).getText()).toBe("Property Details Section");
    });
    it("When there is a title set in the sections summary, it is used for the section summary title", async () => {
      await click(PropertyDetailsSummaryPage.submit());
      await $(HouseType.semiDetached()).click();
      await click(HouseType.submit());
      await expect(await $(HouseholdDetailsSummaryPage.heading()).getText()).toBe("Household Summary - Semi-detached");
    });
  });
});
