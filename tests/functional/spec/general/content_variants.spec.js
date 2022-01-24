import ageQuestionBlock from "../generated_pages/variants_content/age-question-block.page.js";

describe("QuestionVariants", () => {
  beforeEach(() => {
    browser.openQuestionnaire("test_new_variants_content.json");
  });

  it("Given I am completing the survey, then the correct content is shown based on my previous answers when i am under 16", () => {
    $(ageQuestionBlock.age()).setValue(12);
    $(ageQuestionBlock.submit()).click();
    expect($("main.ons-page__main h1").getText()).to.contain("You are 16 or younger");
  });

  it("Given I am completing the survey, then the correct content is shown based on my previous answers when i am under 16", () => {
    $(ageQuestionBlock.age()).setValue(22);
    $(ageQuestionBlock.submit()).click();
    expect($("main.ons-page__main h1").getText()).to.contain("You are 16 or older");
  });
});
