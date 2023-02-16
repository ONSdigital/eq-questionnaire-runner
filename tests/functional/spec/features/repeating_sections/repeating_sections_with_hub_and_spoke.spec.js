import ConfirmDateOfBirthPage from "../../../generated_pages/repeating_sections_with_hub_and_spoke/confirm-dob.page";
import DateOfBirthPage from "../../../generated_pages/repeating_sections_with_hub_and_spoke/date-of-birth.page";
import FirstListCollectorAddPage from "../../../generated_pages/repeating_sections_with_hub_and_spoke/list-collector-add.page";
import FirstListCollectorPage from "../../../generated_pages/repeating_sections_with_hub_and_spoke/list-collector.page";
import HubPage from "../../../base_pages/hub.page.js";
import PersonalDetailsSummaryPage from "../../../generated_pages/repeating_sections_with_hub_and_spoke/personal-details-section-summary.page";
import PrimaryPersonAddPage from "../../../generated_pages/repeating_sections_with_hub_and_spoke/primary-person-list-collector-add.page";
import PrimaryPersonPage from "../../../generated_pages/repeating_sections_with_hub_and_spoke/primary-person-list-collector.page";
import ProxyPage from "../../../generated_pages/repeating_sections_with_hub_and_spoke/proxy.page";
import SecondListCollectorAddPage from "../../../generated_pages/repeating_sections_with_hub_and_spoke/another-list-collector-block-add.page";
import SecondListCollectorInterstitialPage from "../../../generated_pages/repeating_sections_with_hub_and_spoke/next-interstitial.page";
import SecondListCollectorPage from "../../../generated_pages/repeating_sections_with_hub_and_spoke/another-list-collector-block.page";
import SectionSummaryPage from "../../../generated_pages/repeating_sections_with_hub_and_spoke/section-summary.page.js";
import SexPage from "../../../generated_pages/repeating_sections_with_hub_and_spoke/sex.page";
import VisitorsDateOfBirthPage from "../../../generated_pages/repeating_sections_with_hub_and_spoke/visitors-date-of-birth.page";
import VisitorsListCollectorAddPage from "../../../generated_pages/repeating_sections_with_hub_and_spoke/visitors-block-add.page";
import VisitorsListCollectorPage from "../../../generated_pages/repeating_sections_with_hub_and_spoke/visitors-block.page";
import VisitorsListCollectorRemovePage from "../../../generated_pages/repeating_sections_with_hub_and_spoke/visitors-block-remove.page";

describe("Feature: Repeating Sections with Hub and Spoke", () => {
  describe("Given the user has added some members to the household and is on the Hub", () => {
    before("Open survey and add household members", async ()=> {
      await browser.openQuestionnaire("test_repeating_sections_with_hub_and_spoke.json");
      // Accept cookies, this is done due to headless window size where cookie banner
      // is pushing the submit button outside window
      await $(await HubPage.acceptCookies()).click();
      // Ensure we are on the Hub
      await expect(browser.getUrl()).to.contain(HubPage.url());
      // Ensure the first section is not started
      await expect(await $(await HubPage.summaryRowState("section")).getText()).to.equal("Not started");
      // Start first section to add household members
      await $(await HubPage.summaryRowLink("section")).click();

      // Add a primary person
      await $(await PrimaryPersonPage.yes()).click();
      await $(await PrimaryPersonPage.submit()).click();
      await $(await PrimaryPersonAddPage.firstName()).setValue("Marcus");
      await $(await PrimaryPersonAddPage.lastName()).setValue("Twin");
      await $(await PrimaryPersonPage.submit()).click();

      // Add other household members (First list collector)
      await $(await FirstListCollectorPage.yes()).click();
      await $(await FirstListCollectorPage.submit()).click();
      await $(await FirstListCollectorAddPage.firstName()).setValue("Jean");
      await $(await FirstListCollectorAddPage.lastName()).setValue("Clemens");
      await $(await FirstListCollectorAddPage.submit()).click();

      await $(await FirstListCollectorPage.yes()).click();
      await $(await FirstListCollectorPage.submit()).click();
      await $(await FirstListCollectorAddPage.firstName()).setValue("Samuel");
      await $(await FirstListCollectorAddPage.lastName()).setValue("Clemens");
      await $(await FirstListCollectorAddPage.submit()).click();

      // Go to second list collector
      await $(await FirstListCollectorPage.no()).click();
      await $(await FirstListCollectorPage.submit()).click();
      await $(await SecondListCollectorInterstitialPage.submit()).click();

      // Add other household members (Second list collector)
      await $(await SecondListCollectorPage.yes()).click();
      await $(await SecondListCollectorPage.submit()).click();
      await $(await SecondListCollectorAddPage.firstName()).setValue("John");
      await $(await SecondListCollectorAddPage.lastName()).setValue("Doe");
      await $(await SecondListCollectorAddPage.submit()).click();

      // Go back to the Hub
      await $(await SecondListCollectorPage.no()).click();
      await $(await SecondListCollectorPage.submit()).click();
      await $(await VisitorsListCollectorPage.no()).click();
      await $(await VisitorsListCollectorPage.submit()).click();
    });

    beforeEach("Navigate to the Hub", async ()=> browser.url(HubPage.url()));

    it("Then a section for each household member should be displayed", async ()=> {
      await expect(browser.getUrl()).to.contain(HubPage.url());

      await expect(await $(await HubPage.summaryRowState("section")).getText()).to.equal("Completed");
      await expect(await $(await HubPage.summaryRowTitle("personal-details-section-1")).getText()).to.equal("Marcus Twin");
      await expect(await $(await HubPage.summaryRowState("personal-details-section-1")).getText()).to.equal("Not started");
      await expect(await $(await HubPage.summaryRowState("personal-details-section-2")).getText()).to.equal("Not started");
      await expect(await $(await HubPage.summaryRowTitle("personal-details-section-2")).getText()).to.equal("Jean Clemens");
      await expect(await $(await HubPage.summaryRowState("personal-details-section-3")).getText()).to.equal("Not started");
      await expect(await $(await HubPage.summaryRowTitle("personal-details-section-3")).getText()).to.equal("Samuel Clemens");
      await expect(await $(await HubPage.summaryRowState("personal-details-section-4")).getText()).to.equal("Not started");
      await expect(await $(await HubPage.summaryRowTitle("personal-details-section-4")).getText()).to.equal("John Doe");

      await expect(await $(await HubPage.summaryRowState("section-5")).isExisting()).to.be.false;
    });

    it("When the user starts a repeating section and clicks the Previous link on the first question, Then they should be taken back to the Hub", async ()=> {
      await $(await HubPage.summaryRowLink("personal-details-section-2")).click();
      await $(await ProxyPage.previous()).click();

      await expect(browser.getUrl()).to.contain(HubPage.url());
    });

    it("When the user partially completes a repeating section, Then that section should be marked as 'Partially completed' on the Hub", async ()=> {
      await $(await HubPage.summaryRowLink("personal-details-section-1")).click();
      await $(await ProxyPage.yes()).click();
      await $(await ProxyPage.submit()).click();

      await $(await DateOfBirthPage.day()).setValue("01");
      await $(await DateOfBirthPage.month()).setValue("03");
      await $(await DateOfBirthPage.year()).setValue("2000");
      await $(await DateOfBirthPage.submit()).click();

      await $(await ConfirmDateOfBirthPage.confirmDateOfBirthYesPersonNameIsAgeOld()).click();
      await $(await ConfirmDateOfBirthPage.submit()).click();

      browser.url(HubPage.url());

      await expect(browser.getUrl()).to.contain(HubPage.url());
      await expect(await $(await HubPage.summaryRowState("personal-details-section-1")).getText()).to.equal("Partially completed");
    });

    it("When the user continues with a partially completed repeating section, Then they are taken to the first incomplete block", async ()=> {
      await $(await HubPage.summaryRowLink("personal-details-section-1")).click();

      await expect(await $(await SexPage.questionText()).getText()).to.equal("What is Marcus Twin’s sex?");
    });

    it("When the user completes a repeating section, Then that section should be marked as 'Completed' on the Hub", async ()=> {
      await $(await HubPage.summaryRowLink("personal-details-section-2")).click();
      await $(await ProxyPage.yes()).click();
      await $(await ProxyPage.submit()).click();

      await $(await DateOfBirthPage.day()).setValue("09");
      await $(await DateOfBirthPage.month()).setValue("09");
      await $(await DateOfBirthPage.year()).setValue("1995");
      await $(await DateOfBirthPage.submit()).click();

      await $(await ConfirmDateOfBirthPage.confirmDateOfBirthYesPersonNameIsAgeOld()).click();
      await $(await ConfirmDateOfBirthPage.submit()).click();

      await $(await SexPage.female()).click();
      await $(await SexPage.submit()).click();

      await $(await PersonalDetailsSummaryPage.submit()).click();

      await expect(browser.getUrl()).to.contain(HubPage.url());
      await expect(await $(await HubPage.summaryRowState("personal-details-section-2")).getText()).to.equal("Completed");
    });

    it("When the user clicks 'View answers' for a completed repeating section, Then they are taken to the summary", async ()=> {
      await $(await HubPage.summaryRowLink("personal-details-section-2")).click();
      await expect(browser.getUrl()).to.contain("/sections/personal-details-section");
    });

    it("When the user views the summary for a repeating section, Then the page title is shown", async ()=> {
      await $(await HubPage.summaryRowLink("personal-details-section-2")).click();
      await expect(browser.getTitle()).to.equal("… - Hub & Spoke");
    });

    it("When the user adds 2 visitors to the household then a section for each visitor should be display on the hub", async ()=> {
      // Ensure no other sections exist
      await expect(await $(await HubPage.summaryRowState("personal-details-section-5")).isExisting()).to.be.false;
      await expect(await $(await HubPage.summaryRowState("visitors-section-1")).isExisting()).to.be.false;

      // Start section for first visitor
      await $(await HubPage.summaryRowLink("section")).click();

      // Add first visitor
      await $(await SectionSummaryPage.visitorListAddLink()).click();
      await $(await VisitorsListCollectorAddPage.firstName()).setValue("Joe");
      await $(await VisitorsListCollectorAddPage.lastName()).setValue("Public");
      await $(await VisitorsListCollectorAddPage.submit()).click();

      // Add second visitor
      await $(await SectionSummaryPage.visitorListAddLink()).click();
      await $(await VisitorsListCollectorAddPage.firstName()).setValue("Yvonne");
      await $(await VisitorsListCollectorAddPage.lastName()).setValue("Yoe");
      await $(await VisitorsListCollectorAddPage.submit()).click();
      await $(await SectionSummaryPage.submit()).click();

      await expect(await $(await HubPage.summaryRowState("visitors-section-1")).getText()).to.equal("Not started");
      await expect(await $(await HubPage.summaryRowTitle("visitors-section-1")).getText()).to.equal("Joe Public");
      await expect(await $(await HubPage.summaryRowState("visitors-section-2")).getText()).to.equal("Not started");
      await expect(await $(await HubPage.summaryRowTitle("visitors-section-2")).getText()).to.equal("Yvonne Yoe");

      await expect(await $(await HubPage.summaryRowState("visitors-section-3")).isExisting()).to.be.false;
    });

    it("When the user clicks 'Continue' from the Hub, Then they should progress to the first incomplete section", async ()=> {
      await $(await HubPage.submit()).click();
      await expect(await $(await ConfirmDateOfBirthPage.questionText()).getText()).to.equal("What is Marcus Twin’s sex?");
    });

    it("When the user answers on their behalf, Then they are shown the non proxy question variant", async ()=> {
      await $(await HubPage.summaryRowLink("personal-details-section-4")).click();
      await $(await ProxyPage.noIMAnsweringForMyself()).click();
      await $(await ProxyPage.submit()).click();

      await $(await DateOfBirthPage.day()).setValue("07");
      await $(await DateOfBirthPage.month()).setValue("07");
      await $(await DateOfBirthPage.year()).setValue("1970");
      await $(await DateOfBirthPage.submit()).click();

      await $(await ConfirmDateOfBirthPage.confirmDateOfBirthYesIAmAgeOld()).click();
      await $(await ConfirmDateOfBirthPage.submit()).click();

      await expect(await $(await SexPage.questionText()).getText()).to.equal("What is your sex?");
    });

    it("When the user answers on on behalf of someone else, Then they are shown the proxy question variant for the relevant repeating section", async ()=> {
      await $(await HubPage.summaryRowLink("personal-details-section-3")).click();
      await $(await ProxyPage.yes()).click();
      await $(await ProxyPage.submit()).click();

      await $(await DateOfBirthPage.day()).setValue("11");
      await $(await DateOfBirthPage.month()).setValue("11");
      await $(await DateOfBirthPage.year()).setValue("1990");
      await $(await DateOfBirthPage.submit()).click();

      await $(await ConfirmDateOfBirthPage.confirmDateOfBirthYesPersonNameIsAgeOld()).click();
      await $(await ConfirmDateOfBirthPage.submit()).click();
      await expect(await $(await SexPage.questionText()).getText()).to.equal("What is Samuel Clemens’ sex?");
    });

    it("When the user completes all sections, Then the Hub should be in the completed state", async ()=> {
      // Complete remaining sections
      await $(await HubPage.submit()).click();
      await $(await SexPage.male()).click();
      await $(await SexPage.submit()).click();
      await $(await PersonalDetailsSummaryPage.submit()).click();

      await $(await HubPage.submit()).click();
      await $(await SexPage.submit()).click();
      await $(await PersonalDetailsSummaryPage.submit()).click();

      await $(await HubPage.submit()).click();
      await $(await SexPage.female()).click();
      await $(await SexPage.submit()).click();
      await $(await PersonalDetailsSummaryPage.submit()).click();

      await $(await HubPage.submit()).click();
      await $(await VisitorsDateOfBirthPage.day()).setValue("03");
      await $(await VisitorsDateOfBirthPage.month()).setValue("09");
      await $(await VisitorsDateOfBirthPage.year()).setValue("1975");
      await $(await VisitorsDateOfBirthPage.submit()).click();

      await $(await HubPage.submit()).click();
      await $(await VisitorsDateOfBirthPage.day()).setValue("31");
      await $(await VisitorsDateOfBirthPage.month()).setValue("07");
      await $(await VisitorsDateOfBirthPage.year()).setValue("1999");
      await $(await VisitorsDateOfBirthPage.submit()).click();

      await expect(await $(await HubPage.submit()).getText()).to.equal("Submit survey");
      await expect(await $(await HubPage.heading()).getText()).to.equal("Submit survey");
    });

    it("When the user adds a new visitor, Then the Hub should not be in the completed state", async ()=> {
      await $(await HubPage.summaryRowLink("section")).click();

      // Add another visitor
      await $(await SectionSummaryPage.visitorListAddLink()).click();
      await $(await VisitorsListCollectorAddPage.firstName()).setValue("Anna");
      await $(await VisitorsListCollectorAddPage.lastName()).setValue("Doe");
      await $(await VisitorsListCollectorAddPage.submit()).click();
      await $(await SectionSummaryPage.submit()).click();

      // New visitor added to hub
      await expect(await $(await HubPage.summaryRowState("visitors-section-3")).getText()).to.equal("Not started");
      await expect(await $(await HubPage.summaryRowState("visitors-section-3")).isExisting()).to.be.true;

      await expect(await $(await HubPage.submit()).getText()).to.not.equal("Submit survey");
      await expect(await $(await HubPage.submit()).getText()).to.equal("Continue");

      await expect(await $(await HubPage.heading()).getText()).to.not.equal("Submit survey");
      await expect(await $(await HubPage.heading()).getText()).to.equal("Choose another section to complete");
    });

    it("When the user removes a visitor, Then their section is not longer displayed on he Hub", async ()=> {
      // Ensure final householder exists
      await expect(await $(await HubPage.summaryRowState("visitors-section-3")).isExisting()).to.be.true;

      await $(await HubPage.summaryRowLink("section")).click();

      // Remove final visitor
      await $(await SectionSummaryPage.visitorListRemoveLink(3)).click();

      await $(await VisitorsListCollectorRemovePage.yes()).click();
      await $(await VisitorsListCollectorPage.submit()).click();
      await $(await SectionSummaryPage.submit()).click();

      // Ensure final householder no longer exists
      await expect(await $(await HubPage.summaryRowState("visitors-section-3")).isExisting()).to.be.false;
    });

    it("When the user submits, it should show the thank you page", async ()=> {
      await $(await HubPage.submit()).click();
      await expect(browser.getUrl()).to.contain("thank-you");
    });
  });
});
