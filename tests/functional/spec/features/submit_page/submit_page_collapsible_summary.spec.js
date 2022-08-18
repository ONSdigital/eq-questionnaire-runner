import HouseholdCountSectionSummaryPage from "../../../generated_pages/section_summary/household-count-section-summary.page.js";
import HouseholdDetailsSummaryPage from "../../../generated_pages/section_summary/house-details-section-summary.page.js";
import HouseType from "../../../generated_pages/section_summary/house-type.page.js";
import InsuranceAddressPage from "../../../generated_pages/section_summary/insurance-address.page.js";
import InsuranceTypePage from "../../../generated_pages/section_summary/insurance-type.page.js";
import ListedPage from "../../../generated_pages/section_summary/listed.page.js";
import NumberOfPeoplePage from "../../../generated_pages/section_summary/number-of-people.page.js";
import PropertyDetailsSummaryPage from "../../../generated_pages/section_summary/property-details-section-summary.page.js";
import SubmitPage from "../../../generated_pages/section_summary/submit.page.js";

describe("Collapsible Summary", () => {
  describe("Given I complete a questionnaire with collapsible summary enabled", () => {
    beforeEach(() => {
      browser.openQuestionnaire("test_section_summary.json");
      $(InsuranceTypePage.both()).click();
      $(InsuranceTypePage.submit()).click();
      $(InsuranceAddressPage.submit()).click();
      $(ListedPage.submit()).click();
      $(PropertyDetailsSummaryPage.submit()).click();
      $(HouseType.submit()).click();
      $(HouseholdDetailsSummaryPage.submit()).click();
      $(NumberOfPeoplePage.answer()).setValue(3);
      $(NumberOfPeoplePage.submit()).click();
      $(HouseholdCountSectionSummaryPage.submit()).click();
    });

    it("When I am on the submit page, Then a collapsed summary should be displayed with the group title and questions should not be displayed", () => {
      expect($(SubmitPage.collapsibleSummary()).isDisplayed()).to.be.true;

      expect($(SubmitPage.collapsibleSummary()).getText()).to.contain("Property Details");
      expect($(SubmitPage.collapsibleSummary()).getText()).to.contain("House Details");

      expect($(SubmitPage.insuranceAddressQuestion()).getText()).to.contain("");
      expect($(SubmitPage.numberOfPeopleQuestion()).getText()).to.contain("");
    });

    it("When I click the Show all button, Then the summary should be expanded and questions should be displayed", () => {
      $(SubmitPage.summaryShowAllButton()).click();

      expect($(SubmitPage.insuranceAddressQuestion()).isDisplayed()).to.be.true;
      expect($(SubmitPage.numberOfPeopleQuestion()).isDisplayed()).to.be.true;
    });
  });
});
