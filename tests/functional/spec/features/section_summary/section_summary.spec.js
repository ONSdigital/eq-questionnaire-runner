import AddressDurationPage from "../../../generated_pages/section_summary/address-duration.page.js";
import HouseholdCountSectionSummaryPage from "../../../generated_pages/section_summary/household-count-section-summary.page.js";
import HouseholdDetailsSummaryPage from "../../../generated_pages/section_summary/house-details-section-summary.page.js";
import HouseType from "../../../generated_pages/section_summary/house-type.page.js";
import InsuranceAddressPage from "../../../generated_pages/section_summary/insurance-address.page.js";
import InsuranceTypePage from "../../../generated_pages/section_summary/insurance-type.page.js";
import NumberOfPeoplePage from "../../../generated_pages/section_summary/number-of-people.page.js";
import PropertyDetailsSummaryPage from "../../../generated_pages/section_summary/property-details-section-summary.page.js";
import QuestionnaireSummaryPage from "../../../generated_pages/section_summary/summary.page.js";

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
      expect(browser.getUrl()).to.contain(QuestionnaireSummaryPage.url());
    });

    it("When I select edit from Final Summary and don't change an answer, Then I should be taken to the Final Summary", () => {
      $(QuestionnaireSummaryPage.summaryShowAllButton()).click();
      $(QuestionnaireSummaryPage.insuranceAddressAnswerEdit()).click();
      $(InsuranceAddressPage.submit()).click();
      expect(browser.getUrl()).to.contain(QuestionnaireSummaryPage.url());
    });

    it("When I select edit from Final Summary and change an answer that doesn't affect completeness, Then I should be taken to the Final Summary", () => {
      $(QuestionnaireSummaryPage.summaryShowAllButton()).click();
      $(QuestionnaireSummaryPage.insuranceAddressAnswerEdit()).click();
      $(InsuranceAddressPage.answer()).setValue("Test Address");
      $(InsuranceAddressPage.submit()).click();
      expect(browser.getUrl()).to.contain(QuestionnaireSummaryPage.url());
    });

    it("When I select edit from Final Summary and change an answer that affects completeness, Then I should be stepped through the section", () => {
      $(QuestionnaireSummaryPage.summaryShowAllButton()).click();
      $(QuestionnaireSummaryPage.insuranceTypeAnswerEdit()).click();
      $(InsuranceTypePage.contents()).click();
      $(InsuranceTypePage.submit()).click();
      expect(browser.getUrl()).to.contain(InsuranceAddressPage.pageName);
      $(InsuranceAddressPage.submit()).click();
      expect(browser.getUrl()).to.contain(AddressDurationPage.pageName);
    });

    it("When I change an answer, Then the final summary should display the updated value", () => {
      $(QuestionnaireSummaryPage.summaryShowAllButton()).click();
      expect($(QuestionnaireSummaryPage.insuranceAddressAnswer()).getText()).to.contain("No answer provided");
      $(QuestionnaireSummaryPage.insuranceAddressAnswerEdit()).click();
      expect(browser.getUrl()).to.contain(InsuranceAddressPage.pageName);
      $(InsuranceAddressPage.answer()).setValue("Test Address");
      $(InsuranceAddressPage.submit()).click();
      $(QuestionnaireSummaryPage.summaryShowAllButton()).click();
      expect($(QuestionnaireSummaryPage.insuranceAddressAnswer()).getText()).to.contain("Test Address");
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
      expect($(PropertyDetailsSummaryPage.questionText()).getText()).to.contain("Property Details Section");
    });
    it("When there is a title set in the sections summary, it is used for the section summary title", () => {
      $(PropertyDetailsSummaryPage.submit()).click();
      $(HouseType.semiDetached()).click();
      $(HouseType.submit()).click();
      expect($(HouseholdDetailsSummaryPage.questionText()).getText()).to.contain("Household Summary - Semi-detached");
    });
  });
});
