import HubPage from "../base_pages/hub.page";

describe("Page Layout", () => {
  it("Given a page in the questionnaire, When I visit the page, Then the page width should be as expected", async () => {
    await browser.url(HubPage.url());

    const cssWidthSelector = await $('div[class*="ons-col-"][class*="@m"]').getAttribute("class");
    await expect(cssWidthSelector).toContain("ons-col-8@m");
  });
});
