import MandatoryRadioPage from "../../../generated_pages/placeholder_option_label_from_value/mandatory-radio.page";
import ConfirmationQuestionRadioBlockPage from "../../../generated_pages/placeholder_option_label_from_value/confirmation-question-radio-block.page";
import { click } from "../../../helpers";
describe("Option label value check", () => {
  beforeEach("Load the survey", async () => {
    await browser.openQuestionnaire("test_placeholder_option_label_from_value.json");
  });

  it("Given radio options are provided, when I select first answer (piped from metadata) and go to the next page, then the question title contains the label text of the answer I selected", async () => {
    await expect(await $(MandatoryRadioPage.answerBusinessNamePipedLabel()).getText()).to.contain("Apple (piped)");
    await $(MandatoryRadioPage.answerBusinessNamePiped()).click();
    await $(MandatoryRadioPage.submit()).scrollIntoView();
    await click(MandatoryRadioPage.submit());
    await expect(await $(ConfirmationQuestionRadioBlockPage.questionText()).getText()).to.contain("Apple (piped)");
  });

  it("Given radio options are provided, when I select an answer (static) and go to the next page, then the question title contains the label text of the answer I selected", async () => {
    await $(MandatoryRadioPage.googleLtd()).click();
    await $(MandatoryRadioPage.submit()).scrollIntoView();
    await click(MandatoryRadioPage.submit());
    await expect(await $(ConfirmationQuestionRadioBlockPage.questionText()).getText()).to.contain("Google LTD");
  });
});
