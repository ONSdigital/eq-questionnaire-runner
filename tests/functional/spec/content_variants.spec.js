import ageQuestionBlock from "../generated_pages/variants_content/age-question-block.page.js";

describe("QuestionVariants", () => {
  beforeEach(async () => {
    await browser.openQuestionnaire("test_variants_content.json");
  });

  it("Given I am completing the survey, then the correct content is shown based on my previous answers when i am under 16", async () => {
    await $(ageQuestionBlock.age()).setValue(12);
    await $(ageQuestionBlock.submit()).click();
    await expect(await $("main.ons-page__main h1").getText()).to.contain("You are 16 or younger");
  });

  it("Given I am completing the survey, then the correct content is shown based on my previous answers when i am under 16", async () => {
    await $(ageQuestionBlock.age()).setValue(22);
    await $(ageQuestionBlock.submit()).click();
    await expect(await $("main.ons-page__main h1").getText()).to.contain("You are 16 or older");
  });
});
