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
    beforeEach(async ()=> {
      await browser.openQuestionnaire("test_section_summary.json");
      await $(InsuranceTypePage.both()).click();
      await $(InsuranceTypePage.submit()).click();
      await $(InsuranceAddressPage.submit()).click();
      await $(ListedPage.submit()).click();
      await $(PropertyDetailsSummaryPage.submit()).click();
      await $(HouseType.submit()).click();
      await $(HouseholdDetailsSummaryPage.submit()).click();
      await $(NumberOfPeoplePage.answer()).setValue(3);
      await $(NumberOfPeoplePage.submit()).click();
      await $(HouseholdCountSectionSummaryPage.submit()).click();
    });

    it("When I am on the submit page, Then a collapsed summary should be displayed with the group title and questions should not be displayed", async ()=> {
      await expect(await $(SubmitPage.collapsibleSummary()).isDisplayed()).to.be.true;

      await expect(await $(SubmitPage.collapsibleSummary()).getText()).to.contain("Property Details");
      await expect(await $(SubmitPage.collapsibleSummary()).getText()).to.contain("House Details");

      await expect(await $(SubmitPage.insuranceAddressQuestion()).getText()).to.equal("");
      await expect(await $(SubmitPage.numberOfPeopleQuestion()).getText()).to.equal("");
    });

    it("When I click the Show all button, Then the summary should be expanded and questions should be displayed", async ()=> {
      await $(SubmitPage.summaryShowAllButton()).click();

      await expect(await $(SubmitPage.insuranceAddressQuestion()).getText()).to.contain("What is the address you would like to insure?");
      await expect(await $(SubmitPage.numberOfPeopleQuestion()).getText()).to.contain("Title");
    });
  });
});
