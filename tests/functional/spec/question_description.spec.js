import NameBlockPage from "../generated_pages/question_description/name-block.page.js";
import DescriptionBlockPage from "../generated_pages/optional_guidance_and_description/description-block.page";
import RadioPage from "../generated_pages/optional_guidance_and_description/mandatory-radio.page";
import RadioPageTwo from "../generated_pages/optional_guidance_and_description/mandatory-radio-two.page";

describe("Question description", () => {
  it("Given a question description has been set in the schema as an array, When it is rendered, Then it is displayed correctly as multiple paragraph attributes", async () => {
    await browser.openQuestionnaire("test_question_description.json");
    await expect(await $(NameBlockPage.questionTitle()).getHTML()).to.contain("<p>Answer the question</p><p>Go on</p>");
  });
});

describe("Optional question description and guidance", () => {
  it("Given a question description has been set in the schema, When the value to be displayed is None, Then it is not rendered on the page", async () => {
    await browser.openQuestionnaire("test_optional_guidance_and_description.json");
    await $(DescriptionBlockPage.submit()).click();
    await expect(await $(RadioPage.questionTitle()).getHTML()).to.not.contain("<p>''</p>");
    await expect(await $(RadioPage.guidance()).isExisting()).to.be.false;
    await $(RadioPage.no()).click();
    await $(RadioPage.submit()).click();
    await expect(await $(RadioPageTwo.questionTitle()).getHTML()).to.contain("<li>List item one</li>");
    await expect(await $(RadioPageTwo.questionTitle()).getHTML()).to.not.contain("<li></li>");
  });
});
