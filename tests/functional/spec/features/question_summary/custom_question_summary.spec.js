import AddressBlockPage from "../../../generated_pages/custom_question_summary/address.page.js";
import AgeBlock from "../../../generated_pages/custom_question_summary/age.page.js";
import NameBlockPage from "../../../generated_pages/custom_question_summary/name.page.js";
import SubmitPage from "../../../generated_pages/custom_question_summary/submit.page.js";

describe("Summary Screen", () => {
  beforeEach("Load the survey", () => {
    browser.openQuestionnaire("test_custom_question_summary.json");
  });

  it("Given a survey has question summary concatenations and has been completed when on the summary page then the correct response should be displayed formatted correctly", () => {
    completeAllQuestions();
    expect($(SubmitPage.summaryRowState("name-question-concatenated-answer")).getText()).to.contain("John Smith");
    expect($(SubmitPage.summaryRowState("address-question-concatenated-answer")).getText()).to.contain("Cardiff Road\nNewport\nNP10 8XG");
    expect($(SubmitPage.summaryRowState("age-question-concatenated-answer")).getText()).to.contain("7\nThis age is an estimate");
  });

  it("Given no values are entered in a question with multiple answers and concatenation set, when on the summary screen then the correct response should be displayed", () => {
    $(NameBlockPage.submit()).click();
    $(AddressBlockPage.submit()).click();
    $(AgeBlock.submit()).click();
    expect(browser.getUrl()).to.contain(SubmitPage.pageName);
    expect($(SubmitPage.summaryRowState("name-question-concatenated-answer")).getText()).to.contain("No answer provided");
  });

  function completeAllQuestions() {
    $(NameBlockPage.first()).setValue("John");
    $(NameBlockPage.last()).setValue("Smith");
    $(NameBlockPage.submit()).click();
    $(AddressBlockPage.line1()).setValue("Cardiff Road");
    $(AddressBlockPage.townCity()).setValue("Newport");
    $(AddressBlockPage.postcode()).setValue("NP10 8XG");
    $(AddressBlockPage.submit()).click();
    $(AgeBlock.number()).setValue(7);
    $(AgeBlock.singleCheckboxThisAgeIsAnEstimate()).click();
    $(AgeBlock.submit()).click();
  }
});
