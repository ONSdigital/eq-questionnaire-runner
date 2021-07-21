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
import SexPage from "../../../generated_pages/repeating_sections_with_hub_and_spoke/sex.page";
import VisitorsDateOfBirthPage from "../../../generated_pages/repeating_sections_with_hub_and_spoke/visitors-date-of-birth.page";
import VisitorsListCollectorAddPage from "../../../generated_pages/repeating_sections_with_hub_and_spoke/visitors-block-add.page";
import VisitorsListCollectorPage from "../../../generated_pages/repeating_sections_with_hub_and_spoke/visitors-block.page";
import VisitorsListCollectorRemovePage from "../../../generated_pages/repeating_sections_with_hub_and_spoke/visitors-block-remove.page";

describe("Feature: Repeating Sections with Hub and Spoke", () => {
  describe("Given the user has added some members to the household and is on the Hub", () => {
    before("Open survey and add household members", () => {
      browser.openQuestionnaire("test_repeating_sections_with_hub_and_spoke.json");
      // Ensure we are on the Hub
      expect(browser.getUrl()).to.contain(HubPage.url());
      // Ensure the first section is not started
      expect($(HubPage.summaryRowState("section")).getText()).to.equal("Not started");
      // Start first section to add household members
      $(HubPage.summaryRowLink("section")).click();

      // Add a primary person
      $(PrimaryPersonPage.yes()).click();
      $(PrimaryPersonPage.submit()).click();
      $(PrimaryPersonAddPage.firstName()).setValue("Marcus");
      $(PrimaryPersonAddPage.lastName()).setValue("Twin");
      $(PrimaryPersonPage.submit()).click();

      // Add other household members (First list collector)
      $(FirstListCollectorPage.yes()).click();
      $(FirstListCollectorPage.submit()).click();
      $(FirstListCollectorAddPage.firstName()).setValue("Jean");
      $(FirstListCollectorAddPage.lastName()).setValue("Clemens");
      $(FirstListCollectorAddPage.submit()).click();

      $(FirstListCollectorPage.yes()).click();
      $(FirstListCollectorPage.submit()).click();
      $(FirstListCollectorAddPage.firstName()).setValue("Samuel");
      $(FirstListCollectorAddPage.lastName()).setValue("Clemens");
      $(FirstListCollectorAddPage.submit()).click();

      // Go to second list collector
      $(FirstListCollectorPage.no()).click();
      $(FirstListCollectorPage.submit()).click();
      $(SecondListCollectorInterstitialPage.submit()).click();

      // Add other household members (Second list collector)
      $(SecondListCollectorPage.yes()).click();
      $(SecondListCollectorPage.submit()).click();
      $(SecondListCollectorAddPage.firstName()).setValue("John");
      $(SecondListCollectorAddPage.lastName()).setValue("Doe");
      $(SecondListCollectorAddPage.submit()).click();

      // Go back to the Hub
      $(SecondListCollectorPage.no()).click();
      $(SecondListCollectorPage.submit()).click();
      $(VisitorsListCollectorPage.no()).click();
      $(VisitorsListCollectorPage.submit()).click();
    });

    beforeEach("Navigate to the Hub", () => browser.url(HubPage.url()));

    it("Then a section for each household member should be displayed", () => {
      expect(browser.getUrl()).to.contain(HubPage.url());

      expect($(HubPage.summaryRowState("section")).getText()).to.equal("Completed");
      expect($(HubPage.summaryRowTitle("personal-details-section-1")).getText()).to.equal("Marcus Twin");
      expect($(HubPage.summaryRowState("personal-details-section-1")).getText()).to.equal("Not started");
      expect($(HubPage.summaryRowState("personal-details-section-2")).getText()).to.equal("Not started");
      expect($(HubPage.summaryRowTitle("personal-details-section-2")).getText()).to.equal("Jean Clemens");
      expect($(HubPage.summaryRowState("personal-details-section-3")).getText()).to.equal("Not started");
      expect($(HubPage.summaryRowTitle("personal-details-section-3")).getText()).to.equal("Samuel Clemens");
      expect($(HubPage.summaryRowState("personal-details-section-4")).getText()).to.equal("Not started");
      expect($(HubPage.summaryRowTitle("personal-details-section-4")).getText()).to.equal("John Doe");

      expect($(HubPage.summaryRowState("section-5")).isExisting()).to.be.false;
    });

    it("When the user starts a repeating section and clicks the Previous link on the first question, Then they should be taken back to the Hub", () => {
      $(HubPage.summaryRowLink("personal-details-section-2")).click();
      $(ProxyPage.previous()).click();

      expect(browser.getUrl()).to.contain(HubPage.url());
    });

    it("When the user partially completes a repeating section, Then that section should be marked as 'Partially completed' on the Hub", () => {
      $(HubPage.summaryRowLink("personal-details-section-1")).click();
      $(ProxyPage.yes()).click();
      $(ProxyPage.submit()).click();

      $(DateOfBirthPage.day()).setValue("01");
      $(DateOfBirthPage.month()).setValue("03");
      $(DateOfBirthPage.year()).setValue("2000");
      $(DateOfBirthPage.submit()).click();

      $(ConfirmDateOfBirthPage.confirmDateOfBirthYesPersonNameIsAgeOld()).click();
      $(ConfirmDateOfBirthPage.submit()).click();

      browser.url(HubPage.url());

      expect(browser.getUrl()).to.contain(HubPage.url());
      expect($(HubPage.summaryRowState("personal-details-section-1")).getText()).to.equal("Partially completed");
    });

    it("When the user continues with a partially completed repeating section, Then they are taken to the first incomplete block", () => {
      $(HubPage.summaryRowLink("personal-details-section-1")).click();

      expect($(SexPage.questionText()).getText()).to.equal("What is Marcus Twin’s sex?");
    });

    it("When the user completes a repeating section, Then that section should be marked as 'Completed' on the Hub", () => {
      $(HubPage.summaryRowLink("personal-details-section-2")).click();
      $(ProxyPage.yes()).click();
      $(ProxyPage.submit()).click();

      $(DateOfBirthPage.day()).setValue("09");
      $(DateOfBirthPage.month()).setValue("09");
      $(DateOfBirthPage.year()).setValue("1995");
      $(DateOfBirthPage.submit()).click();

      $(ConfirmDateOfBirthPage.confirmDateOfBirthYesPersonNameIsAgeOld()).click();
      $(ConfirmDateOfBirthPage.submit()).click();

      $(SexPage.female()).click();
      $(SexPage.submit()).click();

      $(PersonalDetailsSummaryPage.submit()).click();

      expect(browser.getUrl()).to.contain(HubPage.url());
      expect($(HubPage.summaryRowState("personal-details-section-2")).getText()).to.equal("Completed");
    });

    it("When the user clicks 'View answers' for a completed repeating section, Then they are taken to the summary", () => {
      $(HubPage.summaryRowLink("personal-details-section-2")).click();
      expect(browser.getUrl()).to.contain("/sections/personal-details-section");
    });

    it("When the user views the summary for a repeating section, Then the page title is shown", () => {
      $(HubPage.summaryRowLink("personal-details-section-2")).click();
      expect(browser.getTitle()).to.equal("… - Hub & Spoke");
    });

    it("When the user adds 2 visitors to the household then a section for each visitor should be display on the hub", () => {
      // Ensure no other sections exist
      expect($(HubPage.summaryRowState("personal-details-section-5")).isExisting()).to.be.false;
      expect($(HubPage.summaryRowState("visitors-section-1")).isExisting()).to.be.false;

      // Start section for first visitor
      $(HubPage.summaryRowLink("section")).click();
      $(PrimaryPersonPage.submit()).click();
      $(PrimaryPersonAddPage.submit()).click();
      $(FirstListCollectorPage.submit()).click();
      $(SecondListCollectorInterstitialPage.submit()).click();
      $(SecondListCollectorPage.submit()).click();

      // Add first visitor
      $(VisitorsListCollectorPage.yes()).click();
      $(VisitorsListCollectorPage.submit()).click();
      $(VisitorsListCollectorAddPage.firstName()).setValue("Joe");
      $(VisitorsListCollectorAddPage.lastName()).setValue("Public");
      $(VisitorsListCollectorAddPage.submit()).click();

      // Add second visitor
      $(VisitorsListCollectorPage.yes()).click();
      $(VisitorsListCollectorPage.submit()).click();
      $(VisitorsListCollectorAddPage.firstName()).setValue("Yvonne");
      $(VisitorsListCollectorAddPage.lastName()).setValue("Yoe");
      $(VisitorsListCollectorAddPage.submit()).click();
      $(VisitorsListCollectorPage.no()).click();
      $(VisitorsListCollectorPage.submit()).click();

      expect($(HubPage.summaryRowState("visitors-section-1")).getText()).to.equal("Not started");
      expect($(HubPage.summaryRowTitle("visitors-section-1")).getText()).to.equal("Joe Public");
      expect($(HubPage.summaryRowState("visitors-section-2")).getText()).to.equal("Not started");
      expect($(HubPage.summaryRowTitle("visitors-section-2")).getText()).to.equal("Yvonne Yoe");

      expect($(HubPage.summaryRowState("visitors-section-3")).isExisting()).to.be.false;
    });

    it("When the user clicks 'Continue' from the Hub, Then they should progress to the first incomplete section", () => {
      $(HubPage.submit()).click();
      expect($(ConfirmDateOfBirthPage.questionText()).getText()).to.equal("What is Marcus Twin’s sex?");
    });

    it("When the user answers on their behalf, Then they are shown the non proxy question variant", () => {
      $(HubPage.summaryRowLink("personal-details-section-4")).click();
      $(ProxyPage.noIMAnsweringForMyself()).click();
      $(ProxyPage.submit()).click();

      $(DateOfBirthPage.day()).setValue("07");
      $(DateOfBirthPage.month()).setValue("07");
      $(DateOfBirthPage.year()).setValue("1970");
      $(DateOfBirthPage.submit()).click();

      $(ConfirmDateOfBirthPage.confirmDateOfBirthYesIAmAgeOld()).click();
      $(ConfirmDateOfBirthPage.submit()).click();

      expect($(SexPage.questionText()).getText()).to.equal("What is your sex?");
    });

    it("When the user answers on on behalf of someone else, Then they are shown the proxy question variant for the relevant repeating section", () => {
      $(HubPage.summaryRowLink("personal-details-section-3")).click();
      $(ProxyPage.yes()).click();
      $(ProxyPage.submit()).click();

      $(DateOfBirthPage.day()).setValue("11");
      $(DateOfBirthPage.month()).setValue("11");
      $(DateOfBirthPage.year()).setValue("1990");
      $(DateOfBirthPage.submit()).click();

      $(ConfirmDateOfBirthPage.confirmDateOfBirthYesPersonNameIsAgeOld()).click();
      $(ConfirmDateOfBirthPage.submit()).click();
      expect($(SexPage.questionText()).getText()).to.equal("What is Samuel Clemens’ sex?");
    });

    it("When the user completes all sections, Then the Hub should be in the completed state", () => {
      // Complete remaining sections
      $(HubPage.submit()).click();
      $(SexPage.male()).click();
      $(SexPage.submit()).click();
      $(PersonalDetailsSummaryPage.submit()).click();

      $(HubPage.submit()).click();
      $(SexPage.submit()).click();
      $(PersonalDetailsSummaryPage.submit()).click();

      $(HubPage.submit()).click();
      $(SexPage.female()).click();
      $(SexPage.submit()).click();
      $(PersonalDetailsSummaryPage.submit()).click();

      $(HubPage.submit()).click();
      $(VisitorsDateOfBirthPage.day()).setValue("03");
      $(VisitorsDateOfBirthPage.month()).setValue("09");
      $(VisitorsDateOfBirthPage.year()).setValue("1975");
      $(VisitorsDateOfBirthPage.submit()).click();

      $(HubPage.submit()).click();
      $(VisitorsDateOfBirthPage.day()).setValue("31");
      $(VisitorsDateOfBirthPage.month()).setValue("07");
      $(VisitorsDateOfBirthPage.year()).setValue("1999");
      $(VisitorsDateOfBirthPage.submit()).click();

      expect($(HubPage.submit()).getText()).to.equal("Submit survey");
      expect($(HubPage.heading()).getText()).to.equal("Submit survey");
    });

    it("When the user adds a new member to the household, Then the Hub should not be in the completed state", () => {
      $(HubPage.summaryRowLink("section")).click();
      $(PrimaryPersonPage.submit()).click();
      $(PrimaryPersonAddPage.submit()).click();
      $(FirstListCollectorPage.submit()).click();
      $(SecondListCollectorInterstitialPage.submit()).click();
      $(SecondListCollectorPage.submit()).click();

      // Add another householder
      $(VisitorsListCollectorPage.yes()).click();
      $(VisitorsListCollectorPage.submit()).click();

      $(VisitorsListCollectorAddPage.firstName()).setValue("Anna");
      $(VisitorsListCollectorAddPage.lastName()).setValue("Doe");

      $(SecondListCollectorAddPage.submit()).click();
      $(VisitorsListCollectorPage.no()).click();
      $(VisitorsListCollectorPage.submit()).click();

      // New householder added to hub
      expect($(HubPage.summaryRowState("visitors-section-3")).getText()).to.equal("Not started");
      expect($(HubPage.summaryRowState("visitors-section-3")).isExisting()).to.be.true;

      expect($(HubPage.submit()).getText()).to.not.equal("Submit survey");
      expect($(HubPage.submit()).getText()).to.equal("Continue");

      expect($(HubPage.heading()).getText()).to.not.equal("Submit survey");
      expect($(HubPage.heading()).getText()).to.equal("Choose another section to complete");
    });

    it("When the user removes a member from the household, Then their section is not longer displayed on he Hub", () => {
      // Ensure final householder exists
      expect($(HubPage.summaryRowState("visitors-section-3")).isExisting()).to.be.true;

      $(HubPage.summaryRowLink("section")).click();
      $(PrimaryPersonPage.submit()).click();
      $(PrimaryPersonAddPage.submit()).click();
      $(FirstListCollectorPage.submit()).click();
      $(SecondListCollectorInterstitialPage.submit()).click();
      $(SecondListCollectorPage.submit()).click();

      // Remove final householder
      $(VisitorsListCollectorPage.listRemoveLink(3)).click();
      $(VisitorsListCollectorRemovePage.yes()).click();
      $(VisitorsListCollectorPage.submit()).click();

      // Ensure final householder no longer exists
      expect($(HubPage.summaryRowState("visitors-section-3")).isExisting()).to.be.false;
    });

    it("When the user submits, it should show the thank you page", () => {
      $(HubPage.submit()).click();
      expect(browser.getUrl()).to.contain("thank-you");
    });
  });
});
