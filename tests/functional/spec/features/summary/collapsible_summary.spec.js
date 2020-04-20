const InsuranceAddressPage = require('../../../generated_pages/section_summary/insurance-address.page.js');
const InsuranceTypePage = require('../../../generated_pages/section_summary/insurance-type.page.js');;
const HouseType = require('../../../generated_pages/section_summary/house-type.page.js');
const QuestionnaireSummaryPage = require('../../../generated_pages/section_summary/summary.page.js');


const SectionSummaryPage = require('../../../base_pages/section-summary.page.js');

describe('Collapsible Summary', function() {
  describe('Given I start a Test Section Summary survey and complete to Final Summary', function() {
    beforeEach(function() {
      browser.openQuestionnaire('test_section_summary.json');
      $(InsuranceTypePage.both()).click();
      $(InsuranceTypePage.submit()).click();
      $(InsuranceAddressPage.submit()).click();
      $(SectionSummaryPage.submit()).click();
      $(HouseType.submit()).click();
      $(SectionSummaryPage.submit()).click();
    });

    it('When I am on the Final Summary, Then the group titles should be displayed', function() {
      expect($(QuestionnaireSummaryPage.collapsibleSummary()).getText()).to.contain('Property Details');
      expect($(QuestionnaireSummaryPage.collapsibleSummary()).getText()).to.contain('House Details');
    });
  });
});
