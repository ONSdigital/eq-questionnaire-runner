import TextFieldPage from "../generated_pages/textfield/name-block.page.js";
import SummaryPage from "../generated_pages/textfield/summary.page.js";

describe("Textfield", () => {
  it("Given a textfield option, a user should be able to click the label of the textfield to focus", () => {
    browser.openQuestionnaire("test_textfield.json");
    $(TextFieldPage.nameLabel()).click();
    expect($(TextFieldPage.name()).isFocused()).to.be.true;
  });

  it("Given a text entered in textfield , When user submits and revisits the textfield, Then the textfield must contain the text entered previously", () => {
    browser.openQuestionnaire("test_textfield.json");
    $(TextFieldPage.name()).setValue("'Twenty><&Five'");
    $(TextFieldPage.submit()).click();
    expect(browser.getUrl()).to.contain(SummaryPage.pageName);
    expect($(SummaryPage.nameAnswer()).getText()).to.contain("Twenty><&Five'");
    $(SummaryPage.nameAnswerEdit()).click();
    $(TextFieldPage.name()).getValue();
  });

  it("Given the string entered to the textfield is too long, When the user submits, then the correct error message is displayed", () => {
    browser.openQuestionnaire("test_textfield.json");
    $(TextFieldPage.name()).setValue("This string is too long");
    $(TextFieldPage.submit()).click();
    expect($(TextFieldPage.errorNumber(1)).getText()).to.contain("You have entered too many characters. Enter up to 20 characters");
  });
});
