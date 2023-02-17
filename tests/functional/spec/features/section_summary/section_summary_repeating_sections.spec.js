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
    before("Open survey and add household members", async () => {
      await browser.openQuestionnaire("test_repeating_section_summaries.json");
      // Ensure we are on the Hub
      await expect(browser.getUrl()).to.contain(HubPage.url());
      // Start first section to add household members
      await $(HubPage.summaryRowLink("section")).click();

      // Add a primary person
      await $(PrimaryPersonPage.yes()).click();
      await $(PrimaryPersonPage.submit()).click();
      await $(PrimaryPersonAddPage.firstName()).setValue("Mark");
      await $(PrimaryPersonAddPage.lastName()).setValue("Twain");
      await $(PrimaryPersonPage.submit()).click();

      // Add other household members

      await $(FirstListCollectorPage.yes()).click();
      await $(FirstListCollectorPage.submit()).click();
      await $(FirstListCollectorAddPage.firstName()).setValue("Jean");
      await $(FirstListCollectorAddPage.lastName()).setValue("Clemens");
      await $(FirstListCollectorAddPage.submit()).click();

      await $(FirstListCollectorPage.no()).click();
      await $(FirstListCollectorPage.submit()).click();
    });

    describe("When the user finishes a repeating section", () => {
      before("Enter information for a repeating section", async () => {
        await $(HubPage.summaryRowLink("personal-details-section-1")).click();
        await $(ProxyPage.yes()).click();
        await $(ProxyPage.submit()).click();

        await $(DateOfBirthPage.day()).setValue("30");
        await $(DateOfBirthPage.month()).setValue("11");
        await $(DateOfBirthPage.year()).setValue("1835");
        await $(DateOfBirthPage.submit()).click();
      });

      beforeEach("Navigate to the Section Summary", async () => {
        browser.url(HubPage.url());
        await $(HubPage.summaryRowLink("personal-details-section-1")).click();
      });

      it("the title set in the repeating block is used for the section summary title", async () => {
        await expect(await $(PersonalSummaryPage.heading()).getText()).to.contain("Mark Twain");
      });

      it("renders their name as part of the question title on the section summary", async () => {
        await expect(await $(PersonalSummaryPage.dateOfBirthQuestion()).getText()).to.contain("Mark Twain’s");
      });

      it("renders the correct date of birth answer", async () => {
        await expect(await $(PersonalSummaryPage.dateOfBirthAnswer()).getText()).to.contain("30 November 1835");
      });
    });
  });
});
