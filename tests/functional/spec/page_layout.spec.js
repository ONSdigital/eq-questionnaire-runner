import HubPage from "../base_pages/hub.page";

describe("Page Layout", () => {
  it("Given a page in the questionnaire, When I visit the page, Then the page width should be as expected", () => {
    browser.url(HubPage.url());

    const cssWidthSelector = $('div[class*="ons-col-"][class*="@m"]').getAttribute("class");
    expect(cssWidthSelector).to.contain("ons-col-8@m");
  });
});
