import ConfirmationQuestionRadioBlockPage from "../generated_pages/placeholder_option_label_from_value/mandatory-radio.page";
import MandatoryRadioPage from "../generated_pages/placeholder_option_label_from_value/mandatory-radio.page";

describe("Option label value check", () => {
  beforeEach("Load the survey", () => {
    browser.openQuestionnaire("test_placeholder_option_label_from_value.json");
  });
  it("Given a radio options are provided and I subsequently select a single answer from the displayed list, when I select first answer (piped from metadata) and go to the next page, then the question title contains the label text of the answer I selected", () => {
    $(MandatoryRadioPage.answerBusinessNamePiped()).click();
    $(MandatoryRadioPage.submit()).click();
    expect($(ConfirmationQuestionRadioBlockPage.questionText()).getText()).to.contain("Apple (piped)");
  });
  it("Given a radio option, when I select a single (static) answer and go to the next page, then the question title contains the label text of the answer I selected", () => {
    $(MandatoryRadioPage.googleLtd()).click();
    $(MandatoryRadioPage.submit()).click();
    expect($(ConfirmationQuestionRadioBlockPage.questionText()).getText()).to.contain("Google LTD");
  });
});
