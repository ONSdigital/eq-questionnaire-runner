import NameBlockPage from "../generated_pages/question_description/name-block.page.js";

describe("Question description", () => {
  it("Given a question description has been set in the schema as an array, When it is rendered, Then it is displayed correctly as multiple paragraph attributes", async ()=> {
    await browser.openQuestionnaire("test_question_description.json");
    await expect(await $(await NameBlockPage.questionTitle()).getHTML()).to.contain("<p>Answer the question</p><p>Go on</p>");
  });
});
