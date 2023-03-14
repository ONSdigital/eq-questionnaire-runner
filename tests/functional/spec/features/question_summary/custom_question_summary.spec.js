import AddressBlockPage from "../../../generated_pages/custom_question_summary/address.page.js";
import AgeBlock from "../../../generated_pages/custom_question_summary/age.page.js";
import NameBlockPage from "../../../generated_pages/custom_question_summary/name.page.js";
import SubmitPage from "../../../generated_pages/custom_question_summary/submit.page.js";

describe("Summary Screen", () => {
  beforeEach("Load the survey", async () => {
    await browser.openQuestionnaire("test_custom_question_summary.json");
  });

  it("Given a survey has question summary concatenations and has been completed when on the summary page then the correct response should be displayed formatted correctly", async () => {
    completeAllQuestions();
    await expect(await $(SubmitPage.summaryRowState("name-question-concatenated-answer")).getText()).to.contain("John Smith");
    await expect(await $(SubmitPage.summaryRowState("address-question-concatenated-answer")).getText()).to.contain("Cardiff Road\nNewport\nNP10 8XG");
    await expect(await $(SubmitPage.summaryRowState("age-question-concatenated-answer")).getText()).to.contain("7\nThis age is an estimate");
  });

  it("Given no values are entered in a question with multiple answers and concatenation set, when on the summary screen then the correct response should be displayed", async () => {
    await $(NameBlockPage.submit()).click();
    await $(AddressBlockPage.submit()).click();
    await $(AgeBlock.submit()).click();
    await expect(await browser.getUrl()).to.contain(SubmitPage.pageName);
    await expect(await $(SubmitPage.summaryRowState("name-question-concatenated-answer")).getText()).to.contain("No answer provided");
  });

  async function completeAllQuestions() {
    await $(NameBlockPage.first()).setValue("John");
    await $(NameBlockPage.last()).setValue("Smith");
    await $(NameBlockPage.submit()).click();
    await $(AddressBlockPage.line1()).setValue("Cardiff Road");
    await $(AddressBlockPage.townCity()).setValue("Newport");
    await $(AddressBlockPage.postcode()).setValue("NP10 8XG");
    await $(AddressBlockPage.submit()).click();
    await $(AgeBlock.number()).setValue(7);
    await $(AgeBlock.singleCheckboxThisAgeIsAnEstimate()).click();
    await $(AgeBlock.submit()).click();
  }
});
