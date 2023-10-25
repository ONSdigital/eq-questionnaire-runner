import AddressBlockPage from "../../../generated_pages/custom_question_summary/address.page.js";
import AgeBlock from "../../../generated_pages/custom_question_summary/age.page.js";
import NameBlockPage from "../../../generated_pages/custom_question_summary/name.page.js";
import SubmitPage from "../../../generated_pages/custom_question_summary/submit.page.js";
import { click } from "../../../helpers";
describe("Summary Screen", () => {
  beforeEach("Load the survey", async () => {
    await browser.openQuestionnaire("test_custom_question_summary.json");
  });

  it("Given a survey has question summary concatenations and has been completed when on the summary page then the correct response should be displayed formatted correctly", async () => {
    completeAllQuestions();
    await expect(await $(SubmitPage.summaryRowState("name-question-concatenated-answer")).getText()).toBe("John Smith");
    await expect(await $(SubmitPage.summaryRowState("address-question-concatenated-answer")).getText()).toBe("Cardiff Road\nNewport\nNP10 8XG");
    await expect(await $(SubmitPage.summaryRowState("age-question-concatenated-answer")).getText()).toBe("7\nThis age is an estimate");
  });

  it("Given no values are entered in a question with multiple answers and concatenation set, when on the summary screen then the correct response should be displayed", async () => {
    await click(NameBlockPage.submit());
    await click(AddressBlockPage.submit());
    await click(AgeBlock.submit());
    await expect(browser).toHaveUrlContaining(SubmitPage.pageName);
    await expect(await $(SubmitPage.summaryRowState("name-question-concatenated-answer")).getText()).toBe("No answer provided");
  });

  async function completeAllQuestions() {
    await $(NameBlockPage.first()).setValue("John");
    await $(NameBlockPage.last()).setValue("Smith");
    await click(NameBlockPage.submit());
    await $(AddressBlockPage.line1()).setValue("Cardiff Road");
    await $(AddressBlockPage.townCity()).setValue("Newport");
    await $(AddressBlockPage.postcode()).setValue("NP10 8XG");
    await click(AddressBlockPage.submit());
    await $(AgeBlock.number()).setValue(7);
    await $(AgeBlock.singleCheckboxThisAgeIsAnEstimate()).click();
    await click(AgeBlock.submit());
  }
});
