import MandatoryRadioLabel1Page from "../generated_pages/option_label_from_value/mandatory-radio-label-1.page";
import MandatoryRadioLabel2Page from "../generated_pages/option_label_from_value/mandatory-radio-label-2.page";
import MandatoryCheckboxPage from "../generated_pages/option_label_from_value/mandatory-checkbox.page";
import RecoveryQuestionCheckboxBlockPage from "../generated_pages/option_label_from_value/recovery-question-checkbox-block.page";
import MandatoryRadioPage from "../generated_pages/option_label_from_value/mandatory-radio.page";
import RecoveryQuestionRadioBlockPage from "../generated_pages/option_label_from_value/recovery-question-radio-block.page";

describe("Date checks", () => {
  beforeEach("Load the survey", () => {
    browser.openQuestionnaire("test_option_label_from_value.json");
  });

  it("Given multiple checkbox options are provided, when I select a single answer and go to the next page, then the placeholder contains the label text of the answer I selected", () => {
    $(MandatoryRadioLabel1Page.head()).click();
    $(MandatoryRadioLabel1Page.submit()).click();

    $(MandatoryRadioLabel2Page.label()).click();
    $(MandatoryRadioLabel2Page.submit()).click();
    $(MandatoryCheckboxPage.answerHeadLabel()).click();

    $(MandatoryCheckboxPage.submit()).click();

    expect($(RecoveryQuestionCheckboxBlockPage.questionText()).getText()).to.contain("Head");
  });

  it("Given multiple checkbox options are provided, when I select more than one answer and go to the next page, then I am asked to select only one answer from a list", () => {
    $(MandatoryRadioLabel1Page.head()).click();
    $(MandatoryRadioLabel1Page.submit()).click();

    $(MandatoryRadioLabel2Page.label()).click();
    $(MandatoryRadioLabel2Page.submit()).click();

    $(MandatoryCheckboxPage.answerHeadLabel()).click();
    $(MandatoryCheckboxPage.body()).click();

    $(MandatoryCheckboxPage.submit()).click();

    expect($(MandatoryRadioPage.questionText()).getText()).to.contain(
      "If you suffered any one injury from the options below, please select the most serious one"
    );
  });

  it("Given multiple checkbox options are provided and I subsequently select a single answer from the next displayed list, when I select one answer and go to the next page, then the placeholder contains the label text of the answer I selected", () => {
    $(MandatoryRadioLabel1Page.head()).click();
    $(MandatoryRadioLabel1Page.submit()).click();

    $(MandatoryRadioLabel2Page.label()).click();
    $(MandatoryRadioLabel2Page.submit()).click();

    $(MandatoryCheckboxPage.answerHeadLabel()).click();
    $(MandatoryCheckboxPage.body()).click();

    $(MandatoryCheckboxPage.submit()).click();

    $(MandatoryRadioPage.nose()).click();

    $(MandatoryRadioPage.submit()).click();

    expect($(RecoveryQuestionRadioBlockPage.questionText()).getText()).to.contain("Nose");
  });
});
