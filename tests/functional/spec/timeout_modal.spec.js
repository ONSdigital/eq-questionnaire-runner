describe("Timeout Modal", () => {
  beforeEach("Open Survey", () => {
    browser.openQuestionnaire("test_timeout_modal.json");
  });

  it("Given I am completing the survey, when session time out is set to same amount as the showModalTimeInSeconds of timeout modal I will be able to see timeout modal with the option to extend the session instantly", () => {
    expect($("body").getHTML()).to.include(
      '<p class="ons-js-timeout-timer" aria-hidden="true" aria-relevant="additions">To protect your information, your progress will be saved and you will be signed out in <span class="ons-u-fw-b">1 minute</span>'
    );
  });
});
