import TimeoutBlockPage from "../generated_pages/timeout/timeout-block.page.js";

describe("Timeout", () => {
  before("Open Survey", () => {
    browser.openQuestionnaire("test_timeout.json");
  });

  it("Given I am completing an electronic questionnaire, when I have been inactive for the timeout period and attempt to submit data, then I will be redirected to a page confirming my session has timed out", () => {
    browser.pause(6000);
    $(TimeoutBlockPage.submit()).click();

    expect($("body").getHTML()).to.contain("Your session has timed out due to inactivity");
  });
});
