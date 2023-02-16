import TextareaBlock from "../generated_pages/textarea/textarea-block.page.js";
import TextareaSummary from "../generated_pages/textarea/submit.page.js";

describe("Textarea", () => {
  const textareaSchema = "test_textarea.json";
  const textareaLimit = `${TextareaBlock.answer()} + [data-charcount-singular]`;

  beforeEach(async ()=> {
    await browser.openQuestionnaire(textareaSchema);
  });
  it("Given a textarea option, a user should be able to click the label of the textarea to focus", async ()=> {
    await $(await TextareaBlock.answerLabel()).click();
    await expect(await $(await TextareaBlock.answer()).isFocused()).to.be.true;
  });

  it('Given a textarea option, When no text is entered, Then the summary should display "No answer provided"', async ()=> {
    await $(await TextareaBlock.submit()).click();
    await expect(await $(await TextareaSummary.answer()).getText()).to.contain("No answer provided");
  });

  it("Given a textarea option, When some text is entered, Then the summary should display the text", async ()=> {
    await $(await TextareaBlock.answer()).setValue("Some text");
    await $(await TextareaBlock.submit()).click();
    await expect(await $(await TextareaSummary.answer()).getText()).to.contain("Some text");
  });

  it("Given a text entered in textarea , When user submits and revisits the textarea, Then the textarea must contain the text entered previously", async ()=> {
    await $(await TextareaBlock.answer()).setValue("'Twenty><&Five'");
    await $(await TextareaBlock.submit()).click();
    await expect(await $(await TextareaSummary.answer()).getText()).to.contain("'Twenty><&Five'");
    await $(await TextareaSummary.answerEdit()).click();
    await $(await TextareaBlock.answer()).getValue();
  });

  it("Displays the number of characters remaining", async ()=> {
    await expect(await $(await textareaLimit).getText()).to.contain("20");
  });

  it("Updates the number of characters remaining when the user adds content", async ()=> {
    await $(await TextareaBlock.answer()).setValue("Banjo");
    await expect(await $(await textareaLimit).getText()).to.contain("15");
  });

  it("The user is unable to add more characters when the limit is reached", async ()=> {
    await $(await TextareaBlock.answer()).setValue("This sentence is over twenty characters long");
    await expect(await $(await textareaLimit).getText()).to.contain("0");
    await $(await TextareaBlock.answer()).getValue();
  });
});
