import { TimeoutModalPage } from "../../base_pages/timeout-modal.page.js";
import { click } from "../../helpers";

class TestCase {
  testCaseExpired(page) {
    it("When the timeout modal is displayed, and I do not extend my session, Then I will be redirected to the session expired page", async () => {
      await this.checkTimeoutModal();
      await browser.pause(65000); // We are waiting for the session to expire
      await expect(browser).toHaveUrlContaining("/session-expired");
      await expect(await $("body").getHTML()).toContain(
        "Sorry, you need to sign in again",
        "This is because you have either:",
        "been inactive for 45 minutes and your session has timed out to protect your information",
        "followed a link to a page you are not signed in to",
        "followed a link to a survey that has already been submitted",
      );
      await expect(await $("body").getHTML()).not.toContain("To protect your information, your progress will be saved and you will be signed out in");
    }).timeout(140000);
  }

  testCaseExtended(page) {
    it("When the timeout modal is displayed, and I click the “Continue survey” button, Then my session will be extended", async () => {
      await this.checkTimeoutModal();
      await click(TimeoutModalPage.submit());
      await expect(await $(TimeoutModalPage.timer()).getText()).toBe("");
      await browser.pause(65000); // Waiting 65 seconds to sanity check that it hasn’t expired
      await browser.refresh();
      await expect(browser).toHaveUrlContaining(await page.pageName);
      await expect(await $("body").getHTML()).not.toContain("Sorry, you need to sign in again");
    }).timeout(140000);
  }

  testCaseExtendedNewWindow(page) {
    it("When the timeout modal is displayed, but I open a new window and then focus back on the timeout modal window, Then my session will be extended", async () => {
      await this.checkTimeoutModal();
      await browser.newWindow("");
      await browser.switchWindow(await page.pageName);
      await browser.refresh();
      await browser.pause(65000); // Waiting 65 seconds to sanity check that it hasn’t expired
      await expect(browser).toHaveUrlContaining(await page.pageName);
    }).timeout(140000);
  }

  async checkTimeoutModal() {
    await $(TimeoutModalPage.timer()).waitForDisplayed({ timeout: 70000 });
    await expect(await $(TimeoutModalPage.timer()).getText()).toBe(
      "To protect your information, your progress will be saved and you will be signed out in 59 seconds.",
    );
  }
}

export const TimeoutModalTestCase = new TestCase();
