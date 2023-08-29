import MandatoryRadioPage from "../../../generated_pages/placeholder_metadata/mandatory-radio.page";
import SubmitPage from "../../../generated_pages/placeholder_metadata/submit.page";
import { click } from "../../../helpers";
describe("Placeholder metadata check", () => {
  describe("Given I launch placeholder metadata question", () => {
    before("Load the survey", async () => {
      await browser.openQuestionnaire("test_placeholder_metadata.json");
    });
    it("When I see responding unit question, Then I see radio options with first option as metadata placeholder (ru_name)", async () => {
      await expect(await $(MandatoryRadioPage.answerRuNameLabel()).getText()).to.equal("Apple");
    });
    it("When I answer responding unit question, Then I see confirmation page with my selected placeholder metadata option (ru_name)", async () => {
      await $(MandatoryRadioPage.answerRuName()).click();
      await click(MandatoryRadioPage.submit());

      await expect(await $(SubmitPage.mandatoryRadioAnswer()).getText()).to.equal("Apple");
      await expect(await $(SubmitPage.guidance()).getText()).to.contain("Please submit this survey to complete it");
    });
  });
});
