import RadioNumericDetailPage from "../../../generated_pages/radio_detail_answer_numeric/radio-numeric-detail.page";
import SubmitPage from "../../../generated_pages/radio_detail_answer_numeric/submit.page";

describe('Radio with a numeric "detail_answer" option', () => {
  beforeEach(async ()=> {
    await browser.openQuestionnaire("test_radio_detail_answer_numeric.json");
    await $(await RadioNumericDetailPage.other()).click();
  });

  it("Given a numeric detail answer options are available, When the user clicks an option, Then the detail answer input should be visible.", async ()=> {
    await expect(await $(await RadioNumericDetailPage.otherDetail()).isDisplayed()).to.be.true;
  });

  it("Given a numeric detail answer, When the user does not provide any text, Then just the option value should be displayed on the summary screen", async ()=> {
    // When
    await expect(await $(await RadioNumericDetailPage.otherDetail()).isDisplayed()).to.be.true;
    await $(await RadioNumericDetailPage.submit()).click();
    // Then
    await expect(await $(await SubmitPage.radioAnswerNumericDetail()).getText()).to.contain("Other");
  });

  it("Given a numeric detail answer, When the user provides text, Then that text should be displayed on the summary screen", async ()=> {
    // When
    await $(await RadioNumericDetailPage.otherDetail()).setValue("15");
    await $(await RadioNumericDetailPage.submit()).click();
    // Then
    await expect(await $(await SubmitPage.radioAnswerNumericDetail()).getText()).to.contain("15");
  });

  it("Given a numeric detail answer, When the user provides text, An error should be displayed", async ()=> {
    // When
    await $(await RadioNumericDetailPage.otherDetail()).setValue("fhdjkshfjkds");
    await $(await RadioNumericDetailPage.submit()).click();
    // Then
    await expect(await $(await RadioNumericDetailPage.error()).isDisplayed()).to.be.true;
    await expect(await $(await RadioNumericDetailPage.errorNumber(1)).getText()).to.contain("Please enter an integer");
  });

  it("Given a numeric detail answer, When the user provides a number larger than 20, An error should be displayed", async ()=> {
    // When
    await $(await RadioNumericDetailPage.otherDetail()).setValue("250");
    await $(await RadioNumericDetailPage.submit()).click();
    // Then
    await expect(await $(await RadioNumericDetailPage.error()).isDisplayed()).to.be.true;
    await expect(await $(await RadioNumericDetailPage.errorNumber(1)).getText()).to.contain("Number is too large");
  });

  it("Given a numeric detail answer, When the user provides a number less than 0, An error should be displayed", async ()=> {
    // When
    await $(await RadioNumericDetailPage.otherDetail()).setValue("-1");
    await $(await RadioNumericDetailPage.submit()).click();
    // Then
    await expect(await $(await RadioNumericDetailPage.error()).isDisplayed()).to.be.true;
    await expect(await $(await RadioNumericDetailPage.errorNumber(1)).getText()).to.contain("Number cannot be less than zero");
  });

  it("Given a numeric detail answer, When the user provides text, An error should be displayed and the text in the textbox should be kept", async ()=> {
    // When
    await $(await RadioNumericDetailPage.otherDetail()).setValue("biscuits");
    await $(await RadioNumericDetailPage.submit()).click();
    // Then
    await expect(await $(await RadioNumericDetailPage.error()).isDisplayed()).to.be.true;
    await expect(await $(await RadioNumericDetailPage.errorNumber(1)).getText()).to.contain("Please enter an integer");
    await expect(await $(await RadioNumericDetailPage.otherDetail()).getValue()).to.contain("biscuits");
  });

  it('Given a numeric detail answer, When the user enters "0" and submits, Then "0" should be displayed on the summary screen', async ()=> {
    // When
    await $(await RadioNumericDetailPage.otherDetail()).setValue("0");
    await $(await RadioNumericDetailPage.submit()).click();
    // Then
    await expect(await $(await SubmitPage.radioAnswerNumericDetail()).getText()).to.contain("0");
  });
});
