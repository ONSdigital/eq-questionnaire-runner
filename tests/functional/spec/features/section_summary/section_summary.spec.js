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
import AddressBlockPage from "../../../generated_pages/view_submitted_response/address.page.js";
import NameBlockPage from "../../../generated_pages/view_submitted_response/name.page.js";
import ViewSubmittedResponseSubmitPage from "../../../generated_pages/view_submitted_response/submit.page.js";
import ThankYouPage from "../../../base_pages/thank-you.page";
import ViewSubmittedResponsePage from "../../../generated_pages/view_submitted_response/view-submitted-response.page.js";

describe("Section Summary", () => {
  describe("Given I start a Test Section Summary survey and complete to Section Summary", () => {
    beforeEach(() => {
      browser.openQuestionnaire("test_section_summary.json");
      $(InsuranceTypePage.both()).click();
      $(InsuranceTypePage.submit()).click();
      $(InsuranceAddressPage.submit()).click();
      $(ListedPage.submit()).click();
      expect($(PropertyDetailsSummaryPage.insuranceTypeAnswer()).getText()).to.contain("Both");
    });

    it("When I get to the section summary page, Then the submit button should read 'Continue'", () => {
      expect($(PropertyDetailsSummaryPage.submit()).getText()).to.contain("Continue");
    });

    it("When I get to the section summary page, Then it should have the correct table headers set'", () => {
      expect($(PropertyDetailsSummaryPage.propertyDetailsSummaryTableHead()).getHTML()).to.contain("Question");
      expect($(PropertyDetailsSummaryPage.propertyDetailsSummaryTableHead()).getHTML()).to.contain("Answer given");
      expect($(PropertyDetailsSummaryPage.propertyDetailsSummaryTableHead()).getHTML()).to.contain("Change answer");
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

    it("When I select edit from Section Summary but change routing, Then I should step through the section and be returned to the Section Summary once all new questions have been answered", () => {
      $(PropertyDetailsSummaryPage.insuranceTypeAnswerEdit()).click();
      $(InsuranceTypePage.contents()).click();
      $(InsuranceTypePage.submit()).click();
      expect(browser.getUrl()).to.contain(InsuranceAddressPage.pageName);
      $(InsuranceAddressPage.submit()).click();
      expect(browser.getUrl()).to.contain(AddressDurationPage.pageName);
      $(AddressDurationPage.submit()).click();
      expect(browser.getUrl()).to.contain(PropertyDetailsSummaryPage.pageName);
    });

    it("When I select edit from Section Summary but change routing, Then using previous should not prevent me returning to the section summary once all new questions have been answered", () => {
      $(PropertyDetailsSummaryPage.insuranceTypeAnswerEdit()).click();
      $(InsuranceTypePage.contents()).click();
      $(InsuranceTypePage.submit()).click();
      expect(browser.getUrl()).to.contain(InsuranceAddressPage.pageName);
      $(InsuranceAddressPage.submit()).click();
      expect(browser.getUrl()).to.contain(AddressDurationPage.pageName);
      $(AddressDurationPage.previous()).click();
      expect(browser.getUrl()).to.contain(InsuranceAddressPage.pageName);
      $(InsuranceAddressPage.submit()).click();
      $(AddressDurationPage.submit()).click();
      expect(browser.getUrl()).to.contain(PropertyDetailsSummaryPage.pageName);
    });
  });

  describe("Given I start a Test Section Summary survey and complete to Final Summary", () => {
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

    it("When I select edit from Final Summary but change routing, Then I should step through the section and be returned to the Final Summary once all new questions have been answered", () => {
      $(SubmitPage.summaryShowAllButton()).click();
      $(SubmitPage.insuranceTypeAnswerEdit()).click();
      $(InsuranceTypePage.contents()).click();
      $(InsuranceTypePage.submit()).click();
      expect(browser.getUrl()).to.contain(InsuranceAddressPage.pageName);
      $(InsuranceAddressPage.submit()).click();
      expect(browser.getUrl()).to.contain(AddressDurationPage.pageName);
      $(AddressDurationPage.submit()).click();
      expect(browser.getUrl()).to.contain(SubmitPage.pageName);
    });

    it("When I select edit from Final Summary but change routing, Then using previous should not prevent me returning to the section summary once all new questions have been answered", () => {
      $(SubmitPage.summaryShowAllButton()).click();
      $(SubmitPage.insuranceTypeAnswerEdit()).click();
      $(InsuranceTypePage.contents()).click();
      $(InsuranceTypePage.submit()).click();
      expect(browser.getUrl()).to.contain(InsuranceAddressPage.pageName);
      $(InsuranceAddressPage.submit()).click();
      expect(browser.getUrl()).to.contain(AddressDurationPage.pageName);
      $(AddressDurationPage.previous()).click();
      expect(browser.getUrl()).to.contain(InsuranceAddressPage.pageName);
      $(InsuranceAddressPage.submit()).click();
      $(AddressDurationPage.submit()).click();
      expect(browser.getUrl()).to.contain(SubmitPage.pageName);
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
      $(ListedPage.submit()).click();
      expect($(PropertyDetailsSummaryPage.heading()).getText()).to.contain("Property Details Section");
    });
    it("When there is a title set in the sections summary, it is used for the section summary title", () => {
      $(PropertyDetailsSummaryPage.submit()).click();
      $(HouseType.semiDetached()).click();
      $(HouseType.submit()).click();
      expect($(HouseholdDetailsSummaryPage.heading()).getText()).to.contain("Household Summary - Semi-detached");
    });
  });
  describe("Given I start a questionnaire that has a summary with no change links", () => {
    it.only("When I then navigate to that summary, then the correct headers should be set", () => {
      browser.openQuestionnaire("test_view_submitted_response.json");
      $(NameBlockPage.answer()).setValue("John Smith");
      $(NameBlockPage.submit()).click();
      $(AddressBlockPage.answer()).setValue("NP10 8XG");
      $(AddressBlockPage.submit()).click();
      $(ViewSubmittedResponseSubmitPage.submit()).click();
      expect(browser.getUrl()).to.contain(ThankYouPage.pageName);
      expect($(ThankYouPage.title()).getHTML()).to.contain("Thank you for completing the Test");
      $(ThankYouPage.savePrintAnswersLink()).click();
      expect(browser.getUrl()).to.contain(ViewSubmittedResponsePage.pageName);
      expect($(ViewSubmittedResponsePage.addressDetailsGroupSummaryTableHead()).getHTML()).to.contain("Question");
      expect($(ViewSubmittedResponsePage.addressDetailsGroupSummaryTableHead()).getHTML()).to.contain("Answer given");
      expect($(ViewSubmittedResponsePage.addressDetailsGroupSummaryTableHead()).getHTML()).to.not.contain("Change answer");
    });
  });
});
