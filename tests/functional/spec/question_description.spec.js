import NameBlockPage from "../generated_pages/question_description/name-block.page.js";
import DescriptionBlockPage from "../generated_pages/optional_guidance_and_description/description-block.page";
import RadioPage from "../generated_pages/optional_guidance_and_description/mandatory-radio.page";
import RadioPageTwo from "../generated_pages/optional_guidance_and_description/mandatory-radio-two.page";
import IntroductionPage from "../generated_pages/question_guidance/introduction.page";
import GuidancePage from "../generated_pages/question_guidance/block-test-guidance-title.page";
import { click } from "../helpers";

describe("Question description", () => {
  it("Given a question description has been set in the schema as an array, When it is rendered, Then it is displayed correctly as multiple paragraph attributes", async () => {
    await browser.openQuestionnaire("test_question_description.json");
    await expect(await $(NameBlockPage.questionTitle()).getHTML()).toContain("<p>Answer the question</p><p>Go on</p>");
  });
});

describe("Optional question description and guidance", () => {
  it("Given a question description has been set in the schema, When the value to be displayed is None, Then it is not rendered on the page", async () => {
    await browser.openQuestionnaire("test_optional_guidance_and_description.json");
    await click(DescriptionBlockPage.submit());
    await expect(await $(RadioPage.questionTitle()).getHTML()).not.toContain("<p>''</p>");
    await expect(await $(RadioPage.guidance()).isExisting()).toBe(false);
    await $(RadioPage.no()).click();
    await click(RadioPage.submit());
    await expect(await $(RadioPageTwo.questionTitle()).getHTML()).toContain("<li>List item one</li>");
    await expect(await $(RadioPageTwo.questionTitle()).getHTML()).not.toContain("<li></li>");
  });
});

describe("Question guidance", () => {
  it("Given a question guidance with multiple content items, When it is rendered, Then there should only be one guidance box", async () => {
    await browser.openQuestionnaire("test_question_guidance.json");
    await click(IntroductionPage.submit());
    await expect(browser).toHaveUrlContaining(GuidancePage.pageName);
    await expect(await $$("#question-guidance-question-test-guidance-title").length).toBe(1);
  });
});
