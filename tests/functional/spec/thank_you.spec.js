import { SubmitPage } from "../base_pages/submit.page.js";
import HubPage from "../base_pages/hub.page";
import CheckboxPage from "../generated_pages/title/single-title-block.page";
import ThankYouPage from "../base_pages/thank-you.page";
import DidYouKnowPage from "../generated_pages/thank_you/did-you-know.page";
import ThankYouSubmitPage from "../generated_pages/thank_you/submit.page";

describe("Thank You Social", () => {
  describe("Given I launch a social themed questionnaire", () => {
    beforeEach(() => {
      browser.openQuestionnaire("test_theme_social.json");
    });

    it("When I navigate to the thank you page, Then I should see social theme content", () => {
      $(SubmitPage.submit()).click();
      $(HubPage.submit()).click();
      expect(browser.getUrl()).to.contain(ThankYouPage.pageName);
      expect($(ThankYouPage.title()).getHTML()).to.contain("Thank you for completing the Test Social Survey");
      expect($(ThankYouPage.guidance()).getHTML()).to.contain("Your answers have been submitted");
      expect($(ThankYouPage.metadata()).getHTML()).to.contain("Submitted on:");
      expect($(ThankYouPage.metadata()).getHTML()).to.not.contain("Submission reference:");
    });
  });
});

describe("Thank You Default", () => {
  describe("Given I launch a default themed questionnaire", () => {
    beforeEach(() => {
      browser.openQuestionnaire("test_title.json");
    });

    it("When I navigate to the thank you page, Then I should see default theme content", () => {
      $(CheckboxPage.good()).click();
      $(SubmitPage.submit()).click();
      $(HubPage.submit()).click();
      expect(browser.getUrl()).to.contain(ThankYouPage.pageName);
      expect($(ThankYouPage.title()).getHTML()).to.contain("Thank you for completing the Question Title Test");
      expect($(ThankYouPage.guidance()).getHTML()).to.contain("Your answers have been submitted for");
      expect($(ThankYouPage.metadata()).getHTML()).to.contain("Submitted on:");
      expect($(ThankYouPage.metadata()).getHTML()).to.contain("Submission reference:");
    });
  });
});

describe("Thank You Default View Response Enabled", () => {
  describe("Given I launch a questionnaire where view response is enabled", () => {
    beforeEach(() => {
      browser.openQuestionnaire("test_thank_you.json");
      $(DidYouKnowPage.yes()).click();
      $(DidYouKnowPage.submit()).click();
      $(ThankYouSubmitPage.submit()).click();
      expect(browser.getUrl()).to.contain(ThankYouPage.pageName);
    });

    it("When I navigate to the thank you page, and I have submitted less than 45 minutes ago, Then I should see the option to view my answers", () => {
      expect($(ThankYouPage.viewSubmittedGuidance()).isDisplayed()).to.be.false;
      expect($(ThankYouPage.title()).getHTML()).to.contain("Thank you for completing the Test Thank You");
      expect($(ThankYouPage.viewAnswersTitle()).getHTML()).to.contain("Get a copy of your answers");
      expect($(ThankYouPage.viewAnswersLink()).getText()).to.contain("save or print your answers");
      expect($(ThankYouPage.viewSubmittedWarning()).getHTML()).to.contain("For security your answers will only be available to view for 45 minutes");
    });

    it("When I navigate to the thank you page, and I have submitted more than 45 minutes ago, Then I shouldn't see the option to view my answers", () => {
      expect($(ThankYouPage.viewSubmittedGuidance()).isDisplayed()).to.be.false;
      browser.pause(45000); // Waiting 45 seconds for the timeout to expire (45 minute timeout changed to 45 seconds by overriding VIEW_SUBMITTED_RESPONSE_EXPIRATION_IN_SECONDS for the purpose of the functional test)
      browser.refresh();
      expect($(ThankYouPage.viewSubmittedGuidance()).isDisplayed()).to.be.true;
      expect($(ThankYouPage.viewSubmittedGuidance()).getHTML()).to.contain("For security, you can no longer view your answers");
    });
  });
});
