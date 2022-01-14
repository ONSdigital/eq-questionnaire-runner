import TimeoutInterstitialPage from "../generated_pages/timeout_modal/timeout-modal-interstitial.page";
import TimeoutSubmitPage from "../generated_pages/timeout_modal/submit.page";
import { TimeoutModalPage } from "../base_pages/timeout-modal.page.js";

describe("Timeout", () => {
  describe("Given I am completing the survey, when the session timeout is set to 5 seconds", () => {
    before(() => {
      browser.openQuestionnaire("test_timeout.json");
    });

    it("It will redirect to signed-out page after session expires", () => {
      browser.pause(25000);
      expect(browser.getUrl()).to.equal("http://localhost:5000/signed-out");
      expect($("body").getHTML())
        .to.include("Your survey answers have been saved. You are now signed out.")
        .to.not.include("To protect your information, your progress will be saved and you will be signed out in");
    });
  });
});

describe("Timeout Modal", () => {
  beforeEach("Load the survey", () => {
    browser.openQuestionnaire("test_timeout_modal.json");
  });

  describe("Given I am completing the survey, when the session timeout is set to 125 seconds", () => {
    it("It will make the timeout modal with the option to extend the session visible after 65 seconds", () => {
      checkTimeoutModal();
    });
  });

  describe("Given I am completing the survey, when I click on “Continue survey” button of the timeout modal", () => {
    it("It will extend the session and modal won‘t reappear in the next 15 seconds, no redirect will happen", () => {
      checkTimeoutModal();
      $(TimeoutModalPage.submit()).click();
      expect($(TimeoutModalPage.timer()).getText()).to.equal("");
      browser.pause(15000);
      expect(browser.getUrl()).to.contain(TimeoutInterstitialPage.pageName);
    });
  });
  describe("Given I am completing the survey, when I open a new window and then focus on the modal window", () => {
    it("It will extend the session", () => {
      checkTimeoutModal();
      browser.newWindow("");
      browser.switchWindow("http://localhost:5000/questionnaire/timeout-modal-interstitial/");
      browser.pause(10000);
      expect(browser.getUrl()).to.contain(TimeoutInterstitialPage.pageName);
    });
  });

  describe("Given I am completing the survey, when I get to post submission page", () => {
    it("It will make the timeout modal visible 60 seconds before session expiry", () => {
      $(TimeoutInterstitialPage.submit()).click();
      $(TimeoutSubmitPage.submit()).click();
      checkTimeoutModal();
    });
  });

  function checkTimeoutModal() {
    $(TimeoutModalPage.timer()).waitForDisplayed({ timeout: 80000 });
    expect($(TimeoutModalPage.timer()).getText()).to.equal("To protect your information, your progress will be saved and you will be signed out in 1 minute.");
  }
});
