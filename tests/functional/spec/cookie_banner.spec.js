import InitialPage from "../generated_pages/checkbox/mandatory-checkbox.page";

describe('Given I start a survey"', () => {
  before(() => {
    browser.openQuestionnaire("test_checkbox.json");
  });
  it("When I open the initial page then the cookie banner should be displayed", () => {
    expect($(InitialPage.acceptCookies()).isDisplayed()).to.be.true;
  });

  it("When I delete all cookies from the browser and refresh the page then the cookie banner shouldnt be displayed", () => {
    browser.deleteAllCookies();
    browser.refresh();
    expect($(InitialPage.acceptCookies()).isDisplayed()).to.be.false;
  });
});
