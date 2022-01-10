import TimeoutBlockPage from "../generated_pages/timeout/timeout-block.page.js";

describe("Timeout", () => {
  beforeEach("Open Survey", () => {
    browser.openQuestionnaire("test_timeout.json");
  });

  it("Given I am trying to access a survey , when i have no session cookies, then i get redirected to a page confirming my session is not valid", () => {
    browser.deleteAllCookies();
    const expectedPageTitle = browser.getTitle();
    expect(expectedPageTitle).to.equal("Timeout title - Timeout test");
    $(TimeoutBlockPage.submit()).click();
    expect($("body").getHTML()).to.include(
      "Sorry, you need to sign in again",
      "This is because you have either:",
      "been inactive for 45 minutes and your session has timed out to protect your information",
      "followed a link to a page you are not signed in to",
      "followed a link to a survey that has already been submitted"
    );
  });
});
