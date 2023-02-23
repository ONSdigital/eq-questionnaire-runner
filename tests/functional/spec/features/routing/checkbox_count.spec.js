import ToppingCheckboxPage from "../../../generated_pages/new_routing_checkbox_count/topping-checkbox.page.js";
import CorrectAnswerPage from "../../../generated_pages/new_routing_checkbox_count/correct-answer.page";
import IncorrectAnswerPage from "../../../generated_pages/new_routing_checkbox_count/incorrect-answer.page";

describe("Test routing using count of checkboxes checked", () => {
  beforeEach(async () => {
    await browser.openQuestionnaire("test_new_routing_checkbox_count.json");
  });

  it("Given a user selects 2 checkboxes, When they submit, Then they should be routed to the correct page", async () => {
    await $(ToppingCheckboxPage.cheese()).click();
    await $(ToppingCheckboxPage.ham()).click();
    await $(ToppingCheckboxPage.submit()).click();

    await expect(await browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
    await expect(await $(CorrectAnswerPage.questionText()).getText()).to.have.string("You selected 2 or more toppings");
  });

  it("Given a user selects no checkboxes, When they submit, Then they should be routed to the incorrect page", async () => {
    await $(ToppingCheckboxPage.submit()).click();

    await expect(await browser.getUrl()).to.contain(IncorrectAnswerPage.pageName);
    await expect(await $(IncorrectAnswerPage.questionText()).getText()).to.have.string("You did not select 2 or more toppings");
  });

  it("Given a user selects 1 checkbox, When they submit, Then they should be routed to the incorrect page", async () => {
    await $(ToppingCheckboxPage.cheese()).click();
    await $(ToppingCheckboxPage.submit()).click();

    await expect(await browser.getUrl()).to.contain(IncorrectAnswerPage.pageName);
    await expect(await $(IncorrectAnswerPage.questionText()).getText()).to.have.string("You did not select 2 or more toppings");
  });

  it("Given a user selects 3 checkbox, When they submit, Then they should be routed to the correct page", async () => {
    await $(ToppingCheckboxPage.cheese()).click();
    await $(ToppingCheckboxPage.ham()).click();
    await $(ToppingCheckboxPage.pineapple()).click();
    await $(ToppingCheckboxPage.submit()).click();

    await expect(await browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
    await expect(await $(CorrectAnswerPage.questionText()).getText()).to.have.string("You selected 2 or more toppings");
  });
});
