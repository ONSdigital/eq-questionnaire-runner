import TimeoutBlockPage from "../generated_pages/timeout/timeout-block.page.js";

function assertTimeoutText() {
  expect($("body").getHTML()).to.include(
    "Sorry, you need to sign in again",
    "This is because you have either:",
    "been inactive for 45 minutes and your session has timed out to protect your information",
    "followed a link to a page you are not signed in to",
    "followed a link to a survey that has already been submitted"
  );
}

describe("Timeout", () => {
  beforeEach("Open Survey", () => {
    browser.openQuestionnaire("test_timeout.json");
  });

  it("Given I am completing an electronic questionnaire, when I have been inactive for the timeout period and attempt to submit data, then I will be redirected to a page confirming my session has timed out", () => {
    browser.pause(6000);
    $(TimeoutBlockPage.submit()).click();
    const expectedPageTitle = browser.getTitle();
    expect(expectedPageTitle).to.equal("Page is not available - Timeout test");
    assertTimeoutText();
  });

  it("Given I am trying to access a survey , when i have no session cookies, then i get redirected to a page confirming my session is not valid", () => {
    browser.deleteAllCookies();
    $(TimeoutBlockPage.submit()).click();
    const expectedPageTitle = browser.getTitle();
    expect(expectedPageTitle).to.equal("Page is not available - ONS Business Surveys");
    assertTimeoutText();
  });
});
