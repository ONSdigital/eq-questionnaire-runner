import MandatoryRadioPage from "../../../generated_pages/placeholder_option_label_from_value/mandatory-radio.page";
import ConfirmationQuestionRadioBlockPage from "../../../generated_pages/placeholder_option_label_from_value/confirmation-question-radio-block.page";

describe("Option label value check", () => {
  beforeEach("Load the survey", () => {
    browser.openQuestionnaire("test_placeholder_option_label_from_value.json");
  });

  it("Given radio options are provided and I subsequently select a single answer from the displayed list, when I select first answer (piped from metadata) and go to the next page, then the question title contains the label text of the answer I selected", () => {
    expect($(MandatoryRadioPage.answerBusinessNamePipedLabel()).getText()).to.contain("Apple (piped)");
    $(MandatoryRadioPage.answerBusinessNamePiped()).click();
    $(MandatoryRadioPage.submit()).click();
    expect($(ConfirmationQuestionRadioBlockPage.questionText()).getText()).to.contain("Apple (piped)");
  });

  it("Given radio options are provided, when I select a single (static) answer and go to the next page, then the question title contains the label text of the answer I selected", () => {
    $(MandatoryRadioPage.googleLtd()).click();
    $(MandatoryRadioPage.submit()).click();
    expect($(ConfirmationQuestionRadioBlockPage.questionText()).getText()).to.contain("Google LTD");
  });
});
