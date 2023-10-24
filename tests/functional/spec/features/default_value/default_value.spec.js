import QuestionPageOne from "../../../generated_pages/default/number-question-one.page.js";
import QuestionPageTwo from "../../../generated_pages/default/number-question-two.page.js";
import SubmitPage from "../../../generated_pages/default/submit.page.js";
import QuestionPageOneSkip from "../../../generated_pages/default_with_skip/number-question-one.page.js";
import QuestionPageThreeSkip from "../../../generated_pages/default_with_skip/number-question-three.page.js";
import { click } from "../../../helpers";
describe("Feature: Default Value", () => {
  it('Given I start default schema, When I do not answer a question, Then "no answer provided" is displayed on the Summary page', async () => {
    await browser.openQuestionnaire("test_default.json");
    await click(QuestionPageOne.submit());
    await expect(await browser.getUrl()).toContain(QuestionPageTwo.pageName);
    await $(QuestionPageTwo.two()).setValue(123);
    await click(QuestionPageTwo.submit());
    await expect(await browser.getUrl()).toContain(SubmitPage.pageName);
    await expect(await $(SubmitPage.answerOne()).getText()).toBe("0");
  });

  it("Given I have not answered a question containing a default value, When I return to the question, Then no value should be displayed", async () => {
    await browser.openQuestionnaire("test_default.json");
    await click(QuestionPageOne.submit());
    await expect(await browser.getUrl()).toContain(QuestionPageTwo.pageName);
    await $(QuestionPageTwo.two()).setValue(123);
    await click(QuestionPageTwo.submit());
    await expect(await browser.getUrl()).toContain(SubmitPage.pageName);
    await $(SubmitPage.previous()).click();
    await expect(await browser.getUrl()).toContain(QuestionPageTwo.pageName);
    await $(QuestionPageTwo.previous()).click();
    await expect(await browser.getUrl()).toContain(QuestionPageOne.pageName);
    await expect(await $(QuestionPageOne.one()).getValue()).toBe("");
  });

  it("Given I have not answered a question containing a default value, When a skip condition checks for the default value, Then I should skip the next question", async () => {
    await browser.openQuestionnaire("test_default_with_skip.json");
    await click(QuestionPageOneSkip.submit());
    await expect(await browser.getUrl()).toContain(QuestionPageThreeSkip.pageName);
    await expect(await $(QuestionPageThreeSkip.questionText()).getText()).toBe("Question Three");
  });
});
