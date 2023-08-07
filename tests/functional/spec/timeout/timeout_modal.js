import { TimeoutModalPage } from "../../base_pages/timeout-modal.page.js";

class TestCase {
  testCaseExpired(page) {
    it("When the timeout modal is displayed, and I do not extend my session, Then I will be redirected to the session expired page", async () => {
      await this.checkTimeoutModal();
      await browser.pause(65000); // We are waiting for the session to expire
      await expect(await browser.getUrl()).to.contain("/session-expired");
      await expect(await $("body").getHTML())
        .to.include(
          "Sorry, you need to sign in again",
          "This is because you have either:",
          "been inactive for 45 minutes and your session has timed out to protect your information",
          "followed a link to a page you are not signed in to",
          "followed a link to a survey that has already been submitted",
        )
        .to.not.include("To protect your information, your progress will be saved and you will be signed out in");
    }).timeout(140000);
  }

  testCaseExtended(page) {
    it("When the timeout modal is displayed, and I click the “Continue survey” button, Then my session will be extended", async () => {
      await this.checkTimeoutModal();
      await $(TimeoutModalPage.submit()).click();
      await expect(await $(TimeoutModalPage.timer()).getText()).to.equal("");
      await browser.pause(65000); // Waiting 65 seconds to sanity check that it hasn’t expired
      await browser.refresh();
      await expect(await browser.getUrl()).to.contain(await page.pageName);
      await expect(await $("body").getHTML()).to.not.include("Sorry, you need to sign in again");
    }).timeout(140000);
  }

  testCaseExtendedNewWindow(page) {
    it("When the timeout modal is displayed, but I open a new window and then focus back on the timeout modal window, Then my session will be extended", async () => {
      await this.checkTimeoutModal();
      await browser.newWindow("");
      await browser.switchWindow(await page.pageName);
      await browser.refresh();
      await browser.pause(65000); // Waiting 65 seconds to sanity check that it hasn’t expired
      await expect(await browser.getUrl()).to.contain(await page.pageName);
    }).timeout(140000);
  }

  async checkTimeoutModal() {
    await $(TimeoutModalPage.timer()).waitForDisplayed({ timeout: 70000 });
    await expect(await $(TimeoutModalPage.timer()).getText()).to.equal(
      "To protect your information, your progress will be saved and you will be signed out in 59 seconds.",
    );
  }
}

export const TimeoutModalTestCase = new TestCase();
