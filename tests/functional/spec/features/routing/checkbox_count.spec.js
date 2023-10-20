import ToppingCheckboxPage from "../../../generated_pages/routing_checkbox_count/topping-checkbox.page.js";
import CorrectAnswerPage from "../../../generated_pages/routing_checkbox_count/correct-answer.page";
import IncorrectAnswerPage from "../../../generated_pages/routing_checkbox_count/incorrect-answer.page";
import { click } from "../../../helpers";
describe("Test routing using count of checkboxes checked", () => {
  beforeEach(async () => {
    await browser.openQuestionnaire("test_routing_checkbox_count.json");
  });

  it("Given a user selects 2 checkboxes, When they submit, Then they should be routed to the correct page", async () => {
    await $(ToppingCheckboxPage.cheese()).click();
    await $(ToppingCheckboxPage.ham()).click();
    await click(ToppingCheckboxPage.submit());

    await expect(await browser.getUrl()).toContain(CorrectAnswerPage.pageName);
    await expect(await $(CorrectAnswerPage.questionText()).getText()).toContain("You selected 2 or more toppings");
  });

  it("Given a user selects no checkboxes, When they submit, Then they should be routed to the incorrect page", async () => {
    await click(ToppingCheckboxPage.submit());

    await expect(await browser.getUrl()).toContain(IncorrectAnswerPage.pageName);
    await expect(await $(IncorrectAnswerPage.questionText()).getText()).toContain("You did not select 2 or more toppings");
  });

  it("Given a user selects 1 checkbox, When they submit, Then they should be routed to the incorrect page", async () => {
    await $(ToppingCheckboxPage.cheese()).click();
    await click(ToppingCheckboxPage.submit());

    await expect(await browser.getUrl()).toContain(IncorrectAnswerPage.pageName);
    await expect(await $(IncorrectAnswerPage.questionText()).getText()).toContain("You did not select 2 or more toppings");
  });

  it("Given a user selects 3 checkbox, When they submit, Then they should be routed to the correct page", async () => {
    await $(ToppingCheckboxPage.cheese()).click();
    await $(ToppingCheckboxPage.ham()).click();
    await $(ToppingCheckboxPage.pineapple()).click();
    await click(ToppingCheckboxPage.submit());

    await expect(await browser.getUrl()).toContain(CorrectAnswerPage.pageName);
    await expect(await $(CorrectAnswerPage.questionText()).getText()).toContain("You selected 2 or more toppings");
  });
});
