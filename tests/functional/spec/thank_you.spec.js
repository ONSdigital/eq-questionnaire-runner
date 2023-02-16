import { SubmitPage } from "../base_pages/submit.page.js";
import HubPage from "../base_pages/hub.page";
import CheckboxPage from "../generated_pages/title/single-title-block.page";
import ThankYouPage from "../base_pages/thank-you.page";
import DidYouKnowPage from "../generated_pages/thank_you/did-you-know.page";
import ThankYouSubmitPage from "../generated_pages/thank_you/submit.page";

describe("Thank You Social", () => {
  describe("Given I launch a social themed questionnaire", () => {
    beforeEach(async ()=> {
      await browser.openQuestionnaire("test_theme_social.json", { version: "v2", theme: "social" });
    });

    it("When I navigate to the thank you page, Then I should see social theme content", async ()=> {
      await $(SubmitPage.submit()).click();
      await $(HubPage.submit()).click();
      await expect(browser.getUrl()).to.contain(ThankYouPage.pageName);
      await expect(await $(ThankYouPage.title()).getHTML()).to.contain("Thank you for completing the Test Social Survey");
      await expect(await $(ThankYouPage.guidance()).getHTML()).to.contain("Your answers have been submitted");
      await expect(await $(ThankYouPage.metadata()).getHTML()).to.contain("Submitted on:");
      await expect(await $(ThankYouPage.metadata()).getHTML()).to.not.contain("Submission reference:");
    });
  });
});

describe("Thank You Default", () => {
  describe("Given I launch a default themed questionnaire", () => {
    beforeEach(async ()=> {
      await browser.openQuestionnaire("test_title.json");
    });

    it("When I navigate to the thank you page, Then I should see default theme content", async ()=> {
      await $(CheckboxPage.good()).click();
      await $(SubmitPage.submit()).click();
      await $(HubPage.submit()).click();
      await expect(browser.getUrl()).to.contain(ThankYouPage.pageName);
      await expect(await $(ThankYouPage.title()).getHTML()).to.contain("Thank you for completing the Question Title Test");
      await expect(await $(ThankYouPage.guidance()).getHTML()).to.contain("Your answers have been submitted for");
      await expect(await $(ThankYouPage.metadata()).getHTML()).to.contain("Submitted on:");
      await expect(await $(ThankYouPage.metadata()).getHTML()).to.contain("Submission reference:");
    });
  });
});

describe("Thank You Default View Response Enabled", () => {
  describe("Given I launch a questionnaire where view response is enabled", () => {
    beforeEach(async ()=> {
      await browser.openQuestionnaire("test_thank_you.json");
      await $(DidYouKnowPage.yes()).click();
      await $(DidYouKnowPage.submit()).click();
      await $(ThankYouSubmitPage.submit()).click();
      await expect(browser.getUrl()).to.contain(ThankYouPage.pageName);
    });

    it("When I navigate to the thank you page, and I have submitted less than 40 seconds ago, Then I should see the countdown timer and option to view my answers", async ()=> {
      await expect(await $(ThankYouPage.viewSubmittedGuidance()).isDisplayed()).to.be.false;
      await expect(await $(ThankYouPage.title()).getHTML()).to.contain("Thank you for completing the Test Thank You");
      await expect(await $(ThankYouPage.viewAnswersTitle()).getHTML()).to.contain("Get a copy of your answers");
      await expect(await $(ThankYouPage.viewAnswersLink()).getText()).to.contain("save or print your answers");
      await expect(await $(ThankYouPage.viewSubmittedCountdown()).getHTML()).to.contain("For security, your answers will only be available to view for another");
    });

    it("When I navigate to the thank you page, and I have submitted more than 40 seconds ago, Then I shouldn't see the option to view my answers", async ()=> {
      await expect(await $(ThankYouPage.viewSubmittedGuidance()).isDisplayed()).to.be.false;
      browser.pause(46000); // Waiting 40 seconds for the timeout to expire (45 minute timeout changed to 35 seconds by overriding VIEW_SUBMITTED_RESPONSE_EXPIRATION_IN_SECONDS for the purpose of the functional test)
      await expect(await $(ThankYouPage.viewSubmittedGuidance()).isDisplayed()).to.be.true;
      await expect(await $(ThankYouPage.viewSubmittedGuidance()).getHTML()).to.contain("For security, you can no longer view or get a copy of your answers");
    });
  });
});
