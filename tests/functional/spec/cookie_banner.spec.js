import InitialPage from "../generated_pages/checkbox/mandatory-checkbox.page";

describe("Given I am not authenticated and have no cookie,", () => {
  it("When I visit a page in runner, Then the cookie banner shouldn‘t be displayed", () => {
    browser.url("/");
    expect($(InitialPage.acceptCookies()).isDisplayed()).to.be.false;
  });
});

describe("Given I start a survey,", () => {
  beforeEach(() => {
    browser.openQuestionnaire("test_checkbox.json");
  });
  it("When I open the page, Then the cookie banner should be displayed", () => {
    expect($(InitialPage.acceptCookies()).isDisplayed()).to.be.true;
  });
  it("When I delete all cookies from the browser and refresh the page, Then the cookie banner shouldn‘t be displayed", () => {
    browser.deleteAllCookies();
    browser.refresh();
    expect($(InitialPage.acceptCookies()).isDisplayed()).to.be.false;
  });
  it("When I sign out on the page, Then go back the cookie banner should be displayed", () => {
    $(InitialPage.saveSignOut()).click();
    browser.back();
    expect($(InitialPage.acceptCookies()).isDisplayed()).to.be.true;
  });
  it("When I accept the cookies and refresh the page, Then the cookie banner shouldn‘t be displayed", () => {
    $(InitialPage.acceptCookies()).click();
    browser.refresh();
    expect($(InitialPage.acceptCookies()).isDisplayed()).to.be.false;
  });
});
