import MandatoryRadioPage from "../../../generated_pages/placeholder_metadata/mandatory-radio.page";
import SubmitPage from "../../../generated_pages/placeholder_metadata/submit.page";

describe("Placeholder metadata check", () => {
  describe("Given I launch placeholder metadata question", () => {
    before("Load the survey", () => {
      browser.openQuestionnaire("test_placeholder_metadata.json");
    });
    it("When I see responding unit question, Then I see radio options with first option as metadata placeholder (ru_name)", () => {
      expect($(MandatoryRadioPage.answerRuNameLabel()).getText()).to.equal("Apple");
    });
    it("When I answer responding unit question, then I see confirmation page with my selected placeholder metadata option (ru_name)", () => {
      $(MandatoryRadioPage.answerRuName()).click();
      $(MandatoryRadioPage.submit()).click();

      expect($(SubmitPage.mandatoryRadioAnswer()).getText()).to.equal("Apple");
      expect($(SubmitPage.guidance()).getText()).to.contain("Please submit this survey to complete it");
    });
  });
});
