import MandatoryCheckboxPage from "../generated_pages/placeholder_option_label_from_value/mandatory-checkbox.page";
import RecoveryQuestionCheckboxBlockPage from "../generated_pages/placeholder_option_label_from_value/recovery-question-checkbox-block.page";
import MandatoryRadioPage from "../generated_pages/placeholder_option_label_from_value/mandatory-radio.page";
import RecoveryQuestionRadioBlockPage from "../generated_pages/placeholder_option_label_from_value/recovery-question-radio-block.page";

describe("Option label value check", () => {
  beforeEach("Load the survey", () => {
    browser.openQuestionnaire("test_placeholder_option_label_from_value.json");
  });

  it("Given multiple checkbox options are provided, when I select a single answer and go to the next page, then the question title contains the label text of the answer I selected", () => {
    $(MandatoryCheckboxPage.head()).click();
    $(MandatoryCheckboxPage.submit()).click();

    expect($(RecoveryQuestionCheckboxBlockPage.questionText()).getText()).to.contain("Head");
  });

  it("Given multiple checkbox options are provided, when I select more than one answer and go to the next page, then first option in radio is piped from checkbox", () => {
    $(MandatoryCheckboxPage.head()).click();
    $(MandatoryCheckboxPage.body()).click();
    $(MandatoryCheckboxPage.submit()).click();
    expect($("#mandatory-radio-answer-0-label").getText()).to.contain("Head (piped)");
  });

  it("Given multiple checkbox options are provided and I subsequently select a single answer from the next displayed list, when I select one answer (piped from checkbox) and go to the next page, then the placeholder contains the label text of the answer I selected", () => {
    $(MandatoryCheckboxPage.head()).click();
    $(MandatoryCheckboxPage.body()).click();
    $(MandatoryCheckboxPage.submit()).click();
    $(MandatoryRadioPage.answerBodyPart()).click();
    $(MandatoryRadioPage.submit()).click();

    expect($(RecoveryQuestionRadioBlockPage.questionText()).getText()).to.contain("Head (piped)");
  });
});
