import CheckboxNumericDetailPage from "../../../generated_pages/checkbox_detail_answer_numeric/checkbox-numeric-detail.page";
import SubmitPage from "../../../generated_pages/checkbox_detail_answer_numeric/submit.page";

describe('Checkbox with a numeric "detail_answer" option', () => {
  beforeEach(async () => {
    await browser.openQuestionnaire("test_checkbox_detail_answer_numeric.json");
    await $(CheckboxNumericDetailPage.other()).click();
  });

  it("Given a numeric detail answer options are available, When the user clicks an option, Then the detail answer input should be visible.", async () => {
    await expect(await $(CheckboxNumericDetailPage.otherDetail()).isDisplayed()).to.be.true;
  });

  it("Given a numeric detail answer, When the user does not provide any text, Then just the option value should be displayed on the summary screen", async () => {
    // When
    await expect(await $(CheckboxNumericDetailPage.otherDetail()).isDisplayed()).to.be.true;
    await $(CheckboxNumericDetailPage.submit()).click();
    // Then
    await expect(await $(SubmitPage.checkboxNumericDetailAnswer()).getText()).to.contain("Other");
  });

  it("Given a numeric detail answer, When the user provides text, Then that text should be displayed on the summary screen", async () => {
    // When
    await $(CheckboxNumericDetailPage.otherDetail()).setValue("15");
    await $(CheckboxNumericDetailPage.submit()).click();
    // Then
    await expect(await $(SubmitPage.checkboxNumericDetailAnswer()).getText()).to.contain("15");
  });

  it("Given a numeric detail answer, When the user provides text, An error should be displayed", async () => {
    // When
    await $(CheckboxNumericDetailPage.otherDetail()).setValue("fhdjkshfjkds");
    await $(CheckboxNumericDetailPage.submit()).click();
    // Then
    await expect(await $(CheckboxNumericDetailPage.error()).isDisplayed()).to.be.true;
    await expect(await $(CheckboxNumericDetailPage.errorNumber(1)).getText()).to.contain("Please enter an integer");
  });

  it("Given a numeric detail answer, When the user provides a number larger than 20, An error should be displayed", async () => {
    // When
    await $(CheckboxNumericDetailPage.otherDetail()).setValue("250");
    await $(CheckboxNumericDetailPage.submit()).click();
    // Then
    await expect(await $(CheckboxNumericDetailPage.error()).isDisplayed()).to.be.true;
    await expect(await $(CheckboxNumericDetailPage.errorNumber(1)).getText()).to.contain("Number is too large");
  });

  it("Given a numeric detail answer, When the user provides a number less than 0, An error should be displayed", async () => {
    // When
    await $(CheckboxNumericDetailPage.otherDetail()).setValue("-1");
    await $(CheckboxNumericDetailPage.submit()).click();
    // Then
    await expect(await $(CheckboxNumericDetailPage.error()).isDisplayed()).to.be.true;
    await expect(await $(CheckboxNumericDetailPage.errorNumber(1)).getText()).to.contain("Number cannot be less than zero");
  });

  it("Given a numeric detail answer, When the user provides text, An error should be displayed and the text in the textbox should be kept", async () => {
    // When
    await $(CheckboxNumericDetailPage.otherDetail()).setValue("biscuits");
    await $(CheckboxNumericDetailPage.submit()).click();
    // Then
    await expect(await $(CheckboxNumericDetailPage.error()).isDisplayed()).to.be.true;
    await expect(await $(CheckboxNumericDetailPage.errorNumber(1)).getText()).to.contain("Please enter an integer");
    await browser.pause(1000);
    await expect(await $(CheckboxNumericDetailPage.otherDetail()).getValue()).to.equal("biscuits");
  });

  it('Given a numeric detail answer, When the user enters "0" and submits, Then "0" should be displayed on the summary screen', async () => {
    // When
    await $(CheckboxNumericDetailPage.otherDetail()).setValue("0");
    await $(CheckboxNumericDetailPage.submit()).click();
    // Then
    await expect(await $(SubmitPage.checkboxNumericDetailAnswer()).getText()).to.contain("0");
  });
});
