import { SubmitPage } from "../base_pages/submit.page.js";
import HubPage from "../base_pages/hub.page";
import CheckboxPage from "../generated_pages/title/single-title-block.page";
import ThankYouPage from "../base_pages/thank-you.page";

describe("Thank You Social", () => {
  describe("Given I launch a social theme schema", () => {
    beforeEach(() => {
      browser.openQuestionnaire("test_theme_social.json");
    });

    it("When I navigate to the thank you page, Then I should see social theme content", () => {
      $(SubmitPage.submit()).click();
      $(HubPage.submit()).click();
      expect(browser.getUrl()).to.contain(ThankYouPage.pageName);
      expect($(ThankYouPage.title()).getHTML()).to.contain("Thank you for submitting the Test Social Survey");
      expect($(ThankYouPage.guidance()).getHTML()).to.contain("Your answers have been submitted");
      expect($(ThankYouPage.metadata()).getHTML()).to.contain("Submitted on:");
      expect($(ThankYouPage.metadata()).getHTML()).to.not.contain("Submission reference:");
    });
  });
});

describe("Thank You Business", () => {
  describe("Given I launch a business theme schema", () => {
    beforeEach(() => {
      browser.openQuestionnaire("test_title.json");
    });

    it("When I navigate to the thank you page, Then I should see default theme content", () => {
      $(CheckboxPage.good()).click();
      $(SubmitPage.submit()).click();
      $(HubPage.submit()).click();
      expect(browser.getUrl()).to.contain(ThankYouPage.pageName);
      expect($(ThankYouPage.title()).getHTML()).to.contain("Thank you for submitting the Question Title Test");
      expect($(ThankYouPage.guidance()).getHTML()).to.contain("Your answers have been submitted for");
      expect($(ThankYouPage.metadata()).getHTML()).to.contain("Submitted on:");
      expect($(ThankYouPage.metadata()).getHTML()).to.contain("Submission reference:");
    });
  });
});
