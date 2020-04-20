const InsuranceAddressPage = require('../../../generated_pages/section_summary/insurance-address.page.js');
const InsuranceTypePage = require('../../../generated_pages/section_summary/insurance-type.page.js');
const AddressDurationPage = require('../../../generated_pages/section_summary/address-duration.page.js');
const HouseType = require('../../../generated_pages/section_summary/house-type.page.js');
const QuestionnaireSummaryPage = require('../../../generated_pages/section_summary/summary.page.js');

const SectionSummaryPage = require('../../../base_pages/section-summary.page.js');

describe('Section Summary', function() {
  describe('Given I start a Test Section Summary survey and complete to Section Summary', function() {
    beforeEach(function() {
      browser.openQuestionnaire('test_section_summary.json');
      $(InsuranceTypePage.both()).click();
      $(InsuranceTypePage.submit()).click();
      $(InsuranceAddressPage.submit()).click();
      expect($(SectionSummaryPage.summaryRowValues(1)).getText()).to.contain('Both');
    });

    it('When I have selected an answer to edit and edit it, Then I should return to the section summary with new value displayed', function() {
      $(SectionSummaryPage.summaryRowAction(2)).click();
      $(InsuranceAddressPage.answer()).setValue('Test Address');
      $(InsuranceAddressPage.submit()).click();
      expect($(SectionSummaryPage.summaryRowValues(2)).getText()).to.contain('Test Address');
    });

    it('When I continue on the section summary page, Then I should be taken to the next section', function() {
      $(SectionSummaryPage.submit()).click();
      expect(browser.getUrl()).to.contain(HouseType.pageName);
    });

    it('When I select edit from Section Summary but change routing, Then I should be stepped through the section', function() {
      $(SectionSummaryPage.summaryRowAction(1)).click();
      $(InsuranceTypePage.contents()).click();
      $(InsuranceTypePage.submit()).click();
      expect(browser.getUrl()).to.contain(InsuranceAddressPage.pageName);
      $(InsuranceAddressPage.submit()).click();
      expect(browser.getUrl()).to.contain(AddressDurationPage.pageName);
    });
  });

  describe.only('Given I start a Test Section Summary survey and complete to Final Summary', function() {
    beforeEach(function() {
      browser.openQuestionnaire('test_section_summary.json');
      $(InsuranceTypePage.both()).click();
      $(InsuranceTypePage.submit()).click();
      $(InsuranceAddressPage.submit()).click();
      $(SectionSummaryPage.submit()).click();
      $(HouseType.submit()).click();
      $(SectionSummaryPage.submit()).click();
      expect(browser.getUrl()).to.contain('/questionnaire/summary/');
    });

    it('When I select edit from Final Summary and don\'t change an answer, Then I should be taken to the Section Summary', function() {
      $(QuestionnaireSummaryPage.summaryShowAllButton()).click();
      $(QuestionnaireSummaryPage.insuranceAddressAnswerEdit()).click();
      $(InsuranceAddressPage.submit()).click();
      expect(browser.getUrl()).to.contain('/sections/property-details-section/');
    });

    it('When I select edit from Final Summary and change an answer that doesn\'t affect completeness, Then I should be taken to the Section Summary', function() {
      $(QuestionnaireSummaryPage.summaryShowAllButton()).click();
      $(QuestionnaireSummaryPage.insuranceAddressAnswerEdit()).click();
      $(InsuranceAddressPage.answer()).setValue('Test Address');
      $(InsuranceAddressPage.submit()).click();
      expect(browser.getUrl()).to.contain('/sections/property-details-section/');
    });

    it('When I select edit from Final Summary and change an answer that affects completeness, Then I should be stepped through the section', function() {
      $(QuestionnaireSummaryPage.summaryShowAllButton()).click();
      $(QuestionnaireSummaryPage.insuranceTypeAnswerEdit()).click();
      $(InsuranceTypePage.contents()).click();
      $(InsuranceTypePage.submit()).click();
      expect(browser.getUrl()).to.contain(InsuranceAddressPage.pageName);
      $(InsuranceAddressPage.submit()).click();
      expect(browser.getUrl()).to.contain(AddressDurationPage.pageName);
    });

    it('When I change an answer, Then the final summary should display the updated value', function() {
      $(QuestionnaireSummaryPage.summaryShowAllButton()).click();
      expect($(QuestionnaireSummaryPage.insuranceAddressAnswer()).getText()).to.contain('No answer provided');
      $(QuestionnaireSummaryPage.insuranceAddressAnswerEdit()).click();
      expect(browser.getUrl()).to.contain(InsuranceAddressPage.pageName);
      $(InsuranceAddressPage.answer()).setValue('Test Address');
      $(InsuranceAddressPage.submit()).click();
      expect($(QuestionnaireSummaryPage.insuranceAddressAnswer()).getText()).to.contain('Test Address');
    });
  });
});
