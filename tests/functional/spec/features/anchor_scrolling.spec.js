import InsuranceAddressPage from "../../generated_pages/anchor_scrolling/insurance-address.page.js";
import InsuranceTypePage from "../../generated_pages/anchor_scrolling/insurance-type.page.js";
import PropertyDetailsSummaryPage from "../../generated_pages/anchor_scrolling/property-details-section-summary.page.js";
import HouseType from "../../generated_pages/anchor_scrolling/house-type.page.js";
import HouseholdDetailsSummaryPage from "../../generated_pages/anchor_scrolling/house-details-section-summary.page.js";
import SubmitPage from "../../generated_pages/anchor_scrolling/submit.page.js";

describe("Summary Anchor Scrolling", () => {
  describe("Given I start a Test Section Summary survey", () => {
    beforeEach(() => {
      browser.openQuestionnaire("test_anchor_scrolling.json");
      $(InsuranceTypePage.both()).click();
      $(InsuranceTypePage.submit()).click();
    });

    it("When I have provided an answer and click through to the next question, Then the Previous link url shouldn't contain any anchors or reference to return_to or return_to_answer_id", () => {
      expect($(InsuranceAddressPage.previous()).getAttribute("href")).not.to.contain("#");
      expect($(InsuranceAddressPage.previous()).getAttribute("href")).not.to.contain("return_to");
      expect($(InsuranceAddressPage.previous()).getAttribute("href")).not.to.contain("return_to_answer_id");
    });

    it("When I reach the section summary page, Then the Change link url should contain return_to, return_to_answer_id query params", () => {
      $(InsuranceAddressPage.submit()).click();
      $(ListedPage.submit()).click();
      expect($(PropertyDetailsSummaryPage.insuranceAddressAnswer2Edit()).getAttribute("href")).to.contain(
        "/questionnaire/insurance-address/?return_to=section-summary&return_to_answer_id=insurance-address-answer2#insurance-address-answer2"
      );
    });

    it("When I edit an answer from the section summary page, Then the Previous link url should contain an anchor referencing the answer id of the answer I am changing", () => {
      $(InsuranceAddressPage.submit()).click();
      $(ListedPage.submit()).click();
      $(PropertyDetailsSummaryPage.insuranceAddressAnswer2Edit()).click();
      expect($(InsuranceAddressPage.previous()).getAttribute("href")).to.contain("/questionnaire/sections/property-details-section/#insurance-address-answer2");
    });

    it("When I edit an answer from the section summary page and click the Previous link, Then the browser url should contain an anchor referencing the answer id of the answer I am changing", () => {
      $(InsuranceAddressPage.submit()).click();
      $(ListedPage.submit()).click();
      $(PropertyDetailsSummaryPage.insuranceAddressAnswer2Edit()).click();
      $(InsuranceAddressPage.previous()).click();
      expect(browser.getUrl()).to.contain("/questionnaire/sections/property-details-section/#insurance-address-answer2");
    });

    it("When I edit an answer from the final summary page, Then the Change link url should contain return_to, return_to_answer_id query params", () => {
      $(InsuranceAddressPage.submit()).click();
      $(ListedPage.submit()).click();
      $(InsuranceAddressPage.submit()).click();
      $(ListedPage.submit()).click();
      $(PropertyDetailsSummaryPage.submit()).click();
      $(HouseType.submit()).click();
      $(HouseholdDetailsSummaryPage.submit()).click();
      $(NumberOfPeoplePage.answer()).setValue(3);
      $(NumberOfPeoplePage.submit()).click();
      $(HouseholdCountSectionSummaryPage.submit()).click();
      $(SubmitPage.summaryShowAllButton()).click();
      expect($(SubmitPage.insuranceAddressAnswer2Edit()).getAttribute("href")).to.contain(
        "/questionnaire/insurance-address/?return_to=final-summary&return_to_answer_id=insurance-address-answer2#insurance-address-answer2"
      );
    });

    it("When I edit an answer from the final summary page, Then the browser url contains return_to, return_to_answer_id query params", () => {
      $(InsuranceAddressPage.submit()).click();
      $(ListedPage.submit()).click();
      $(InsuranceAddressPage.submit()).click();
      $(ListedPage.submit()).click();
      $(PropertyDetailsSummaryPage.submit()).click();
      $(HouseType.submit()).click();
      $(HouseholdDetailsSummaryPage.submit()).click();
      $(NumberOfPeoplePage.answer()).setValue(3);
      $(NumberOfPeoplePage.submit()).click();
      $(HouseholdCountSectionSummaryPage.submit()).click();
      $(SubmitPage.summaryShowAllButton()).click();
      $(SubmitPage.insuranceAddressAnswer2Edit()).click();
      expect(browser.getUrl()).to.contain(
        "/questionnaire/insurance-address/?return_to=final-summary&return_to_answer_id=insurance-address-answer2#insurance-address-answer2"
      );
    });
  });
});
