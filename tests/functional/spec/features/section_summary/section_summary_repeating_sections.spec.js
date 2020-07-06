import PrimaryPersonPage from "../../../generated_pages/repeating_section_summaries/primary-person-list-collector.page";
import PrimaryPersonAddPage from "../../../generated_pages/repeating_section_summaries/primary-person-list-collector-add.page";
import FirstListCollectorPage from "../../../generated_pages/repeating_section_summaries/list-collector.page";
import FirstListCollectorAddPage from "../../../generated_pages/repeating_section_summaries/list-collector-add.page";
import PersonalSummaryPage from "../../../generated_pages/repeating_section_summaries/personal-details-section-summary.page";
import ProxyPage from "../../../generated_pages/repeating_section_summaries/proxy.page";
import DateOfBirthPage from "../../../generated_pages/repeating_section_summaries/date-of-birth.page";
import HubPage from "../../../base_pages/hub.page.js";

describe("Feature: Repeating Section Summaries", () => {
  describe("Given the user has added some members to the household and is on the Hub", () => {
    before("Open survey and add household members", () => {
      browser.openQuestionnaire("test_repeating_section_summaries.json");
      // Ensure we are on the Hub
      expect(browser.getUrl()).to.contain(HubPage.url());
      // Start first section to add household members
      $(HubPage.summaryRowLink("section")).click();

      // Add a primary person
      $(PrimaryPersonPage.yes()).click();
      $(PrimaryPersonPage.submit()).click();
      $(PrimaryPersonAddPage.firstName()).setValue("Mark");
      $(PrimaryPersonAddPage.lastName()).setValue("Twain");
      $(PrimaryPersonPage.submit()).click();

      // Add other household members

      $(FirstListCollectorPage.yes()).click();
      $(FirstListCollectorPage.submit()).click();
      $(FirstListCollectorAddPage.firstName()).setValue("Jean");
      $(FirstListCollectorAddPage.lastName()).setValue("Clemens");
      $(FirstListCollectorAddPage.submit()).click();

      $(FirstListCollectorPage.no()).click();
      $(FirstListCollectorPage.submit()).click();
    });

    describe("When the user finishes a repeating section", () => {
      before("Enter information for a repeating section", () => {
        $(HubPage.summaryRowLink("personal-details-section-1")).click();
        $(ProxyPage.yes()).click();
        $(ProxyPage.submit()).click();

        $(DateOfBirthPage.day()).setValue("30");
        $(DateOfBirthPage.month()).setValue("11");
        $(DateOfBirthPage.year()).setValue("1835");
        $(DateOfBirthPage.submit()).click();
      });

      beforeEach("Navigate to the Section Summary", () => {
        browser.url(HubPage.url());
        $(HubPage.summaryRowLink("personal-details-section-1")).click();
      });

      it("the title set in the repeating block is used for the section summary title", () => {
        expect($(PersonalSummaryPage.questionText()).getText()).to.contain("Mark Twain");
      });

      it("renders their name as part of the question title on the section summary", () => {
        expect($(PersonalSummaryPage.dateOfBirthQuestion()).getText()).to.contain("Mark Twain’s");
      });

      it("renders the correct date of birth answer", () => {
        expect($(PersonalSummaryPage.dateOfBirthAnswer()).getText()).to.contain("30 November 1835");
      });
    });
  });
});
