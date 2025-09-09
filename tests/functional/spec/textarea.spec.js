import TextareaBlock from "../generated_pages/textarea/textarea-block.page.js";
import TextareaSummary from "../generated_pages/textarea/submit.page.js";
import { click } from "../helpers";
describe("Textarea", () => {
  const textareaSchema = "test_textarea.json";
  const textareaLimit = `${TextareaBlock.answer()}-check[data-message-singular]`;

  beforeEach(async () => {
    await browser.openQuestionnaire(textareaSchema);
  });
  it("Given a textarea option, a user should be able to click the label of the textarea to focus", async () => {
    await $(TextareaBlock.answerLabel()).click();
    await expect(await $(TextareaBlock.answer()).isFocused()).toBe(true);
  });

  it('Given a textarea option, When no text is entered, Then the summary should display "No answer provided"', async () => {
    await click(TextareaBlock.submit());
    await expect(await $(TextareaSummary.answer()).getText()).toBe("No answer provided");
  });

  it("Given a textarea option, When some text is entered, Then the summary should display the text", async () => {
    await $(TextareaBlock.answer()).setValue("Some text");
    await click(TextareaBlock.submit());
    await expect(await $(TextareaSummary.answer()).getText()).toBe("Some text");
  });

  it("Given a text entered in textarea , When user submits and revisits the textarea, Then the textarea must contain the text entered previously", async () => {
    await $(TextareaBlock.answer()).setValue("'Twenty><&Five'");
    await click(TextareaBlock.submit());
    await expect(await $(TextareaSummary.answer()).getText()).toBe("'Twenty><&Five'");
    await $(TextareaSummary.answerEdit()).click();
    await $(TextareaBlock.answer()).getValue();
  });

  it("Displays the number of characters remaining", async () => {
    await expect(await $(textareaLimit).getText()).toContain("20");
  });

  it("Updates the number of characters remaining when the user adds content", async () => {
    await $(TextareaBlock.answer()).setValue("Banjo");
    await expect(await $(textareaLimit).getText()).toContain("15");
  });

  it("Displays the number of characters entered over the limit when the user exceeds the character limit", async () => {
    await $(TextareaBlock.answer()).setValue("This sentence is over twenty characters long");
    await expect(await $(textareaLimit).getText()).toContain("24");
    await $(TextareaBlock.answer()).getValue();
  });
});
