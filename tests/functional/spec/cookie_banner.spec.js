import InitialPage from "../generated_pages/checkbox/mandatory-checkbox.page";

describe('Given I open runner"', () => {
  it("When I visit the root address then the cookie banner shouldn‘t be displayed", () => {
    browser.url("/");
    expect($(InitialPage.acceptCookies()).isDisplayed()).to.be.false;
  });
});

describe('Given I start a survey"', () => {
  beforeEach(() => {
    browser.openQuestionnaire("test_checkbox.json");
  });
  it("When I open the initial page then the cookie banner should be displayed", () => {
    expect($(InitialPage.acceptCookies()).isDisplayed()).to.be.true;
  });
  it("When I delete all cookies from the browser and refresh the page then the cookie banner shouldn‘t be displayed", () => {
    browser.deleteAllCookies();
    browser.refresh();
    expect($(InitialPage.acceptCookies()).isDisplayed()).to.be.false;
  });
  it("When I sign out on the initial page then go back the cookie banner should be displayed", () => {
    $(InitialPage.saveSignOut()).click();
    browser.back();
    expect($(InitialPage.acceptCookies()).isDisplayed()).to.be.true;
  });
  it("When I accept the cookies and refresh the page then the cookie banner shouldn‘t be displayed", () => {
    $(InitialPage.acceptCookies()).click();
    browser.refresh();
    expect($(InitialPage.acceptCookies()).isDisplayed()).to.be.false;
  });
});
