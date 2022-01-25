import InsuranceAddressPage from "../../generated_pages/section_summary/insurance-address.page.js";
import InsuranceTypePage from "../../generated_pages/section_summary/insurance-type.page.js";
import ListedPage from "../../generated_pages/section_summary/listed.page.js";
import PropertyDetailsSummaryPage from "../../generated_pages/section_summary/property-details-section-summary.page.js";

describe("Section Summary", () => {
  describe("Given I start a Test Section Summary survey", () => {
    beforeEach(() => {
      browser.openQuestionnaire("test_section_summary.json");
      $(InsuranceTypePage.both()).click();
      $(InsuranceTypePage.submit()).click();
    });

    it("When I have provided an answer and click through to the next question, the Previous button url shouldn't yet contain any anchors or reference to return_to or return_to_answer_id", () => {
      expect($(InsuranceAddressPage.previous()).getAttribute("href")).not.to.contain("#");
      expect($(InsuranceAddressPage.previous()).getAttribute("href")).not.to.contain("return_to");
      expect($(InsuranceAddressPage.previous()).getAttribute("href")).not.to.contain("return_to_answer_id");
    });

    it("When I reach the summary page, the Change button url should contain return_to, return_to_answer_id query params", () => {
      $(InsuranceAddressPage.submit()).click();
      $(ListedPage.submit()).click();
      expect($(PropertyDetailsSummaryPage.insuranceAddressAnswerEdit()).getAttribute("href")).to.contain(
        "/questionnaire/insurance-address/?return_to=section-summary&return_to_answer_id=insurance-address-answer#insurance-address-answer"
      );
    });

    it("When I edit an answer from the summary page, the Previous button url should contain an anchor referencing the answer id of the answer I am changing", () => {
      $(InsuranceAddressPage.submit()).click();
      $(ListedPage.submit()).click();
      $(PropertyDetailsSummaryPage.insuranceAddressAnswerEdit()).click();
      expect($(InsuranceAddressPage.previous()).getAttribute("href")).to.contain("/questionnaire/sections/property-details-section/#insurance-address-answer");
    });
  });
});
