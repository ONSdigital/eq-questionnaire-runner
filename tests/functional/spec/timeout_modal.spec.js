import TimeoutInterstitialPage from "../generated_pages/timeout_modal/timeout-modal-interstitial.page";
import TimeoutSubmitPage from "../generated_pages/timeout_modal/submit.page";
import { TimeoutModalPage } from "../base_pages/timeout-modal.page.js";
import ThankYouPage from "../base_pages/thank-you.page.js";

describe("Timeout", () => {
  describe("Given I am completing the survey, ", () => {
    before(() => {
      browser.openQuestionnaire("test_timeout.json");
    });

    it("When the session timeout is set to 5 seconds, Then it will redirect to session expired page after session expires", () => {
      browser.pause(25000);
      expect(browser.getUrl()).to.contain("/session-expired");
      expect($("body").getHTML())
        .to.include(
          "Sorry, you need to sign in again",
          "This is because you have either:",
          "been inactive for 45 minutes and your session has timed out to protect your information",
          "followed a link to a page you are not signed in to",
          "followed a link to a survey that has already been submitted"
        )
        .to.not.include("To protect your information, your progress will be saved and you will be signed out in");
    });
  });
});

describe("Timeout Modal", () => {
  describe("Given I am completing the survey, ", () => {
    beforeEach(() => {
      browser.openQuestionnaire("test_timeout_modal.json");
    });

    it("When the session timeout is set to 125 seconds, Then it will make the timeout modal with the option to extend the session visible after 65 seconds", () => {
      checkTimeoutModal();
    });

    it("When I click “Continue survey” button of the timeout modal, Then it will extend the session and modal won‘t reappear in the next 15 seconds, no redirect will happen", () => {
      checkTimeoutModal();
      $(TimeoutModalPage.submit()).click();
      expect($(TimeoutModalPage.timer()).getText()).to.equal("");
      browser.pause(15000);
      expect(browser.getUrl()).to.contain(TimeoutInterstitialPage.pageName);
    });

    it("When I open a new window and then focus on the modal window, Then it will extend the session", () => {
      checkTimeoutModal();
      browser.newWindow("");
      browser.switchWindow(TimeoutInterstitialPage.pageName);
      browser.pause(10000);
      expect(browser.getUrl()).to.contain(TimeoutInterstitialPage.pageName);
    });
  });
});

describe("Timeout Modal Post Submission", () => {
  describe("Given I am completing the survey and get to post submission page, ", () => {
    beforeEach(() => {
      browser.openQuestionnaire("test_timeout_modal.json");
      $(TimeoutInterstitialPage.submit()).click();
      $(TimeoutSubmitPage.submit()).click();
    });

    it("When the session timeout is set to 125 seconds, Then it will make the timeout modal with the option to extend the session visible after 65 seconds", () => {
      checkTimeoutModal();
    });

    it("When I click “Continue survey” button of the timeout modal, Then it will extend the session and modal won‘t reappear in the next 15 seconds, no redirect will happen", () => {
      checkTimeoutModal();
      $(TimeoutModalPage.submit()).click();
      expect($(TimeoutModalPage.timer()).getText()).to.equal("");
      browser.pause(15000);
      expect(browser.getUrl()).to.contain(ThankYouPage.pageName);
    });

    it("When I open a new window and then focus on the modal window, Then it will extend the session", () => {
      checkTimeoutModal();
      browser.newWindow("");
      browser.switchWindow(ThankYouPage.pageName);
      browser.pause(10000);
      expect(browser.getUrl()).to.contain(ThankYouPage.pageName);
    });
  });
});

function checkTimeoutModal() {
  $(TimeoutModalPage.timer()).waitForDisplayed({ timeout: 80000 });
  expect($(TimeoutModalPage.timer()).getText()).to.equal("To protect your information, your progress will be saved and you will be signed out in 1 minute.");
}
