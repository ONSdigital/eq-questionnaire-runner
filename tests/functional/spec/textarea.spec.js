import TextareaBlock from "../generated_pages/textarea/textarea-block.page.js";
import TextareaSummary from "../generated_pages/textarea/summary.page.js";

describe("Textarea", () => {
  const textareaSchema = "test_textarea.json";
  const textareaLimit = `${TextareaBlock.answer()} + [data-charcount-singular]`;

  beforeEach(() => {
    browser.openQuestionnaire(textareaSchema);
  });
  it("Given a textarea option, a user should be able to click the label of the textarea to focus", () => {
    $(TextareaBlock.answerLabel()).click();
    expect($(TextareaBlock.answer()).isFocused()).to.be.true;
  });

  it('Given a textarea option, When no text is entered, Then the summary should display "No answer provided"', () => {
    $(TextareaBlock.submit()).click();
    expect($(TextareaSummary.answer()).getText()).to.contain("No answer provided");
  });

  it("Given a textarea option, When some text is entered, Then the summary should display the text", () => {
    $(TextareaBlock.answer()).setValue("Some text");
    $(TextareaBlock.submit()).click();
    expect($(TextareaSummary.answer()).getText()).to.contain("Some text");
  });

  it("Given a text entered in textarea , When user submits and revisits the textarea, Then the textarea must contain the text entered previously", () => {
    $(TextareaBlock.answer()).setValue("'Twenty><&Five'");
    $(TextareaBlock.submit()).click();
    expect($(TextareaSummary.answer()).getText()).to.contain("'Twenty><&Five'");
    $(TextareaSummary.answerEdit()).click();
    $(TextareaBlock.answer()).getValue();
  });

  it("Displays the number of characters remaining", () => {
    expect($(textareaLimit).getText()).to.contain("20");
  });

  it("Updates the number of characters remaining when the user adds content", () => {
    $(TextareaBlock.answer()).setValue("Banjo");
    expect($(textareaLimit).getText()).to.contain("15");
  });

  it("The user is unable to add more characters when the limit is reached", () => {
    $(TextareaBlock.answer()).setValue("This sentence is over twenty characters long");
    expect($(textareaLimit).getText()).to.contain("0");
    $(TextareaBlock.answer()).getValue();
  });
});
