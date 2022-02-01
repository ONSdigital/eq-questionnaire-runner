import MandatoryRadioPage from "../../../generated_pages/placeholder_metadata/mandatory-radio.page";
import SubmitPage from "../../../generated_pages/placeholder_metadata/submit.page";

describe("Place holder metadata check", () => {
  beforeEach("Load the survey", () => {
    browser.openQuestionnaire("test_placeholder_metadata.json");
  });
  it("Given when i launch survey, then i see radio option with first option as metadata placeholder (ru_name)", () => {
    expect($(MandatoryRadioPage.answerRuNameLabel()).getText()).to.equal("Apple");
  });
  it("When i select placeholder metadata (1st option), then i see confirmation page with my selected place holder metadata option (ru_name)", () => {
    $(MandatoryRadioPage.answerRuName()).click();
    $(MandatoryRadioPage.submit()).click();

    expect($(SubmitPage.mandatoryRadioAnswer()).getText()).to.equal("Apple");
    expect($(SubmitPage.guidance()).getText()).to.contain("Please submit this survey to complete it");
  });
});
