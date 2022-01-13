import TimeoutInterstitialPage from "../generated_pages/timeout_modal/timeout-modal-interstitial.page";
import TimeoutSubmitPage from "../generated_pages/timeout_modal/submit.page";
import { TimeoutModalPage } from "../base_pages/timeout-modal.page.js";

describe("Timeout Modal", () => {
  beforeEach("Load the survey", () => {
    browser.openQuestionnaire("test_timeout_modal.json");
    browser.setTimeout({ script: 70000 });
  });

  describe("Given I am completing the survey, when the session timeout is set to 2 minutes", () => {
    it("I will be able to see the timeout modal with the option to extend the session after 60 seconds", () => {
      checkTimeoutModal();
    });
  });

  describe("Given I am completing the survey, when I click on “Continue survey” button of the timeout modal", () => {
    it("I will be able to extend the session", () => {
      checkTimeoutModal();
      $(TimeoutModalPage.submit()).click();
      expect($(TimeoutModalPage.timer()).getText()).to.equal("");
    });
  });
  describe("Given I am completing the survey, when I open a new window and then focus on the modal window ", () => {
    it("I will extend the session", () => {
      checkTimeoutModal();
      browser.newWindow("");
      browser.switchWindow("http://localhost:5000/questionnaire/timeout-modal-interstitial/");
      expect($(TimeoutModalPage.timer()).getText()).to.equal(
        "To protect your information, your progress will be saved and you will be signed out in 1 minute."
      );
    });
  });

  describe("Given I am completing the survey, when I get to post submission page", () => {
    it("I should be able see the timeout modal 60 seconds before session expiry", () => {
      $(TimeoutInterstitialPage.submit()).click();
      $(TimeoutSubmitPage.submit()).click();
      checkTimeoutModal();
    });
  });

  function checkTimeoutModal() {
    $(TimeoutModalPage.timer()).waitForDisplayed({ timeout: 70000 });
    expect($(TimeoutModalPage.timer()).getText()).to.equal("To protect your information, your progress will be saved and you will be signed out in 1 minute.");
  }
});
