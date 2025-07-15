import InitialPage from "../generated_pages/checkbox/mandatory-checkbox.page";
import HubPage from "../base_pages/hub.page.js";

describe("Given I am not authenticated and have no cookie,", () => {
  it("When I visit a page in runner, Then the cookie banner shouldn‘t be displayed", async () => {
    await browser.url("/");
    await expect(await $(InitialPage.acceptCookies()).isDisplayed()).toBe(false);
  });
});

describe("Given I start a survey,", () => {
  beforeEach(async () => {
    await browser.openQuestionnaire("test_checkbox.json");
  });
  it("When I open the page, Then the cookie banner should be displayed", async () => {
    await expect(await $(InitialPage.acceptCookies()).isDisplayed()).toBe(true);
  });
  it.skip("When I delete all cookies from the browser and refresh the page, Then the cookie banner shouldn‘t be displayed", async () => {
    await browser.deleteAllCookies();
    await browser.refresh();
    await browser.pause(1000); // Wait for the page to load after refresh
    await expect(await $(InitialPage.acceptCookies()).isDisplayed()).toBe(false);
  });
  it("When I sign out and click the browser back button, Then the cookie banner should be displayed", async () => {
    await $(InitialPage.saveSignOut()).click();
    await browser.back();
    await expect(await $(InitialPage.acceptCookies()).isDisplayed()).toBe(true);
  });
  it("When I accept the cookies and refresh the page, Then the cookie banner shouldn‘t be displayed", async () => {
    await $(InitialPage.acceptCookies()).click();
    await browser.refresh();
    await expect(await $(InitialPage.acceptCookies()).isDisplayed()).toBe(false);
  });
});

describe("Given I start a survey with multiple languages,", () => {
  beforeEach(async () => {
    await browser.deleteAllCookies();
  });
  it("When I open the page in english, Then the cookie banner should be displayed in english", async () => {
    await browser.openQuestionnaire("test_language.json", {
      language: "en",
    });
    await expect(await $(HubPage.acceptCookies()).getText()).toBe("Accept additional cookies");
  });
  it("When I open the page in welsh, Then the cookie banner should be displayed in welsh", async () => {
    await browser.openQuestionnaire("test_language.json", {
      language: "cy",
    });
    await expect(await $(HubPage.acceptCookies()).getText()).toBe("Derbyn cwcis ychwanegol");
  });
  it("When I open the page in english, Then change the language to welsh the cookie banner should be displayed in welsh", async () => {
    await browser.openQuestionnaire("test_language.json", {
      language: "en",
    });
    await expect(await $(HubPage.acceptCookies()).getText()).toBe("Accept additional cookies");
    await $(HubPage.switchLanguage("cy")).click();
    await expect(await $(HubPage.acceptCookies()).getText()).toBe("Derbyn cwcis ychwanegol");
  });
});
