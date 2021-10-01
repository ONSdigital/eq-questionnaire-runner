import ToppingCheckboxPage from "../../../generated_pages/new_routing_checkbox_count/topping-checkbox.page.js";
import CorrectAnswerPage from "../../../generated_pages/new_routing_checkbox_count/correct-answer.page";
import IncorrectAnswerPage from "../../../generated_pages/new_routing_checkbox_count/incorrect-answer.page";

describe("Test routing using count of checkboxes checked", () => {
  beforeEach(() => {
    browser.openQuestionnaire("test_new_routing_checkbox_count.json");
  });

  it("Given a user selects 2 checkboxes, When they submit, Then they should be routed to the correct page", () => {
    $(ToppingCheckboxPage.cheese()).click();
    $(ToppingCheckboxPage.ham()).click();
    $(ToppingCheckboxPage.submit()).click();

    expect(browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
    expect($("body").getText()).to.have.string("You were asked to select 2 toppings and you selected 2.");
  });

  it("Given a user selects no checkboxes, When they submit, Then they should be routed to the incorrect page", () => {
    $(ToppingCheckboxPage.submit()).click();

    expect(browser.getUrl()).to.contain(IncorrectAnswerPage.pageName);
    expect($("body").getText()).to.have.string("You were asked to select 2 toppings but you actually selected 0.");
  });

  it("Given a user selects 1 checkbox, When they submit, Then they should be routed to the incorrect page", () => {
    $(ToppingCheckboxPage.cheese()).click();
    $(ToppingCheckboxPage.submit()).click();

    expect(browser.getUrl()).to.contain(IncorrectAnswerPage.pageName);
    expect($("body").getText()).to.have.string("You were asked to select 2 toppings but you actually selected 1.");
  });

  it("Given a user selects 3 checkbox, When they submit, Then they should be routed to the incorrect page", () => {
    $(ToppingCheckboxPage.cheese()).click();
    $(ToppingCheckboxPage.ham()).click();
    $(ToppingCheckboxPage.pineapple()).click();
    $(ToppingCheckboxPage.submit()).click();

    expect(browser.getUrl()).to.contain(IncorrectAnswerPage.pageName);
    expect($("body").getText()).to.have.string("You were asked to select 2 toppings but you actually selected 3.");
  });
});
