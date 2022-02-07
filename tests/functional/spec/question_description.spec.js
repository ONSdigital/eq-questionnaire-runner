import NameBlockPage from "../generated_pages/question_description/name-block.page.js";

describe("Question description", () => {
  it("Given a question description has been set in the schema as an array, it is displayed correctly as a newline-separated string", () => {
    browser.openQuestionnaire("test_question_description.json");
    expect($(NameBlockPage.questionTitle()).getHTML()).to.contain("<p>Answer the question</p><p>Go on</p>");
  });
});
