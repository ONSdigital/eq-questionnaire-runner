const InsuranceAddressPage = require('../../../generated_pages/section_summary/insurance-address.page.js');
const InsuranceTypePage = require('../../../generated_pages/section_summary/insurance-type.page.js');
const PropertyDetailsSummaryPage = require('../../../generated_pages/section_summary/property-details-summary.page.js');
const HouseType = require('../../../generated_pages/section_summary/house-type.page.js');
const HouseholdDetailsSummaryPage = require('../../../generated_pages/section_summary/household-details-summary.page.js');
const FinalSummaryPage = require('../../../generated_pages/section_summary/summary.page.js');

describe('Collapsible Summary', function() {

  describe('Given I start a Test Section Summary survey and complete to Final Summary', function() {
    beforeEach(function() {
      browser.openQuestionnaire('test_section_summary.json');
      $(InsuranceTypePage.both()).click();
      $(InsuranceTypePage.submit()).click();
      $(InsuranceAddressPage.submit()).click();
      $(PropertyDetailsSummaryPage.submit()).click();
      $(HouseType.submit()).click();
      $(HouseholdDetailsSummaryPage.submit()).click();
    });

    it('When I am on the Final Summary, Then the group titles should be displayed', function() {
      expect($(FinalSummaryPage.collapsibleSummary()).getText()).to.contain('Property Details');
      expect($(FinalSummaryPage.collapsibleSummary()).getText()).to.contain('House Details');
    });

  });
});
