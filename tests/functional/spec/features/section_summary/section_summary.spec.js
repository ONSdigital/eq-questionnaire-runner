import AddressDurationPage from "../../../generated_pages/section_summary/address-duration.page.js";
import HouseholdCountSectionSummaryPage from "../../../generated_pages/section_summary/household-count-section-summary.page.js";
import HouseholdDetailsSummaryPage from "../../../generated_pages/section_summary/house-details-section-summary.page.js";
import HouseType from "../../../generated_pages/section_summary/house-type.page.js";
import InsuranceAddressPage from "../../../generated_pages/section_summary/insurance-address.page.js";
import InsuranceTypePage from "../../../generated_pages/section_summary/insurance-type.page.js";
import NumberOfPeoplePage from "../../../generated_pages/section_summary/number-of-people.page.js";
import PropertyDetailsSummaryPage from "../../../generated_pages/section_summary/property-details-section-summary.page.js";
import SubmitPage from "../../../generated_pages/section_summary/submit.page.js";

describe("Section Summary", () => {
  describe("Given I start a Test Section Summary survey and complete to Section Summary", () => {
    beforeEach(() => {
      browser.openQuestionnaire("test_section_summary.json");
      $(InsuranceTypePage.both()).click();
      $(InsuranceTypePage.submit()).click();
      $(InsuranceAddressPage.submit()).click();
      expect($(PropertyDetailsSummaryPage.insuranceTypeAnswer()).getText()).to.contain("Both");
    });

    it("When I get to the section summary page, Then the submit button should read 'Continue'", () => {
      expect($(PropertyDetailsSummaryPage.submit()).getText()).to.contain("Continue");
    });

    it("When I have selected an answer to edit and edit it, Then I should return to the section summary with new value displayed", () => {
      $(PropertyDetailsSummaryPage.insuranceAddressAnswerEdit()).click();
      $(InsuranceAddressPage.answer()).setValue("Test Address");
      $(InsuranceAddressPage.submit()).click();
      expect($(PropertyDetailsSummaryPage.insuranceAddressAnswer()).getText()).to.contain("Test Address");
    });

    it("When I select edit from the section summary and click previous on the question page, Then I should be taken back to the section summary", () => {
      $(PropertyDetailsSummaryPage.insuranceAddressAnswerEdit()).click();
      $(InsuranceAddressPage.previous()).click();
      expect(browser.getUrl()).to.contain(PropertyDetailsSummaryPage.url());
    });

    it("When I continue on the section summary page, Then I should be taken to the next section", () => {
      $(PropertyDetailsSummaryPage.submit()).click();
      expect(browser.getUrl()).to.contain(HouseType.pageName);
    });

    it("When I select edit from Section Summary but change routing, Then I should be stepped through the section", () => {
      $(PropertyDetailsSummaryPage.insuranceTypeAnswerEdit()).click();
      $(InsuranceTypePage.contents()).click();
      $(InsuranceTypePage.submit()).click();
      expect(browser.getUrl()).to.contain(InsuranceAddressPage.pageName);
      $(InsuranceAddressPage.submit()).click();
      expect(browser.getUrl()).to.contain(AddressDurationPage.pageName);
    });
  });

  describe("Given I start a Test Section Summary survey and complete to Final Summary", () => {
    beforeEach(() => {
      browser.openQuestionnaire("test_section_summary.json");
      $(InsuranceTypePage.both()).click();
      $(InsuranceTypePage.submit()).click();
      $(InsuranceAddressPage.submit()).click();
      $(PropertyDetailsSummaryPage.submit()).click();
      $(HouseType.submit()).click();
      $(HouseholdDetailsSummaryPage.submit()).click();
      $(NumberOfPeoplePage.answer()).setValue(3);
      $(NumberOfPeoplePage.submit()).click();
      $(HouseholdCountSectionSummaryPage.submit()).click();
      expect(browser.getUrl()).to.contain(SubmitPage.url());
    });

    it("When I select edit from Final Summary and don't change an answer, Then I should be taken to the Final Summary", () => {
      $(SubmitPage.summaryShowAllButton()).click();
      $(SubmitPage.insuranceAddressAnswerEdit()).click();
      $(InsuranceAddressPage.submit()).click();
      expect(browser.getUrl()).to.contain(SubmitPage.url());
    });

    it("When I select edit from Final Summary and change an answer that doesn't affect completeness, Then I should be taken to the Final Summary", () => {
      $(SubmitPage.summaryShowAllButton()).click();
      $(SubmitPage.insuranceAddressAnswerEdit()).click();
      $(InsuranceAddressPage.answer()).setValue("Test Address");
      $(InsuranceAddressPage.submit()).click();
      expect(browser.getUrl()).to.contain(SubmitPage.url());
    });

    it("When I select edit from Final Summary and change an answer that affects completeness, Then I should be stepped through the section", () => {
      $(SubmitPage.summaryShowAllButton()).click();
      $(SubmitPage.insuranceTypeAnswerEdit()).click();
      $(InsuranceTypePage.contents()).click();
      $(InsuranceTypePage.submit()).click();
      expect(browser.getUrl()).to.contain(InsuranceAddressPage.pageName);
      $(InsuranceAddressPage.submit()).click();
      expect(browser.getUrl()).to.contain(AddressDurationPage.pageName);
    });

    it("When I select edit from Final Summary and change an answer and then go to the next question and click previous, Then I should return to the question I originally edited", () => {
      $(SubmitPage.summaryShowAllButton()).click();
      $(SubmitPage.insuranceTypeAnswerEdit()).click();
      $(InsuranceTypePage.contents()).click();
      $(InsuranceTypePage.submit()).click();
      $(InsuranceAddressPage.previous()).click();
      expect(browser.getUrl()).to.contain(InsuranceTypePage.pageName);
    });

    it("When I change an answer, Then the final summary should display the updated value", () => {
      $(SubmitPage.summaryShowAllButton()).click();
      expect($(SubmitPage.insuranceAddressAnswer()).getText()).to.contain("No answer provided");
      $(SubmitPage.insuranceAddressAnswerEdit()).click();
      expect(browser.getUrl()).to.contain(InsuranceAddressPage.pageName);
      $(InsuranceAddressPage.answer()).setValue("Test Address");
      $(InsuranceAddressPage.submit()).click();
      $(SubmitPage.summaryShowAllButton()).click();
      expect($(SubmitPage.insuranceAddressAnswer()).getText()).to.contain("Test Address");
    });
  });
  describe("Given I start the Test Section Summary questionnaire", () => {
    before(() => {
      browser.openQuestionnaire("test_section_summary.json");
    });
    it("When there is no title set in the sections summary, the section title is used for the section summary title", () => {
      $(InsuranceTypePage.both()).click();
      $(InsuranceTypePage.submit()).click();
      $(InsuranceAddressPage.submit()).click();
      expect($(PropertyDetailsSummaryPage.heading()).getText()).to.contain("Property Details Section");
    });
    it("When there is a title set in the sections summary, it is used for the section summary title", () => {
      $(PropertyDetailsSummaryPage.submit()).click();
      $(HouseType.semiDetached()).click();
      $(HouseType.submit()).click();
      expect($(HouseholdDetailsSummaryPage.heading()).getText()).to.contain("Household Summary - Semi-detached");
    });
  });
});
