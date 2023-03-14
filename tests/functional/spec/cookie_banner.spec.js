import InitialPage from "../generated_pages/checkbox/mandatory-checkbox.page";

describe("Given I am not authenticated and have no cookie,", () => {
  it("When I visit a page in runner, Then the cookie banner shouldn‘t be displayed", async () => {
    await browser.url("/");
    await expect(await $(InitialPage.acceptCookies()).isDisplayed()).to.be.false;
  });
});

describe("Given I start a survey,", () => {
  beforeEach(async () => {
    await browser.openQuestionnaire("test_checkbox.json");
  });
  it("When I open the page, Then the cookie banner should be displayed", async () => {
    await expect(await $(InitialPage.acceptCookies()).isDisplayed()).to.be.true;
  });
  it("When I delete all cookies from the browser and refresh the page, Then the cookie banner shouldn‘t be displayed", async () => {
    await browser.deleteAllCookies();
    await browser.refresh();
    await expect(await $(InitialPage.acceptCookies()).isDisplayed()).to.be.false;
  });
  it("When I sign out and click the browser back button, Then the cookie banner should be displayed", async () => {
    await $(InitialPage.saveSignOut()).click();
    await browser.back();
    await expect(await $(InitialPage.acceptCookies()).isDisplayed()).to.be.true;
  });
  it("When I accept the cookies and refresh the page, Then the cookie banner shouldn‘t be displayed", async () => {
    await $(InitialPage.acceptCookies()).click();
    await browser.refresh();
    await expect(await $(InitialPage.acceptCookies()).isDisplayed()).to.be.false;
  });
});
