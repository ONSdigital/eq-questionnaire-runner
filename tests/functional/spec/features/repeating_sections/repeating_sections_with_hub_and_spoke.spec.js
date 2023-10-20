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
import { click } from "../../../helpers";
describe("Feature: Repeating Sections with Hub and Spoke", () => {
  describe("Given the user has added some members to the household and is on the Hub", () => {
    before("Open survey and add household members", async () => {
      await browser.openQuestionnaire("test_repeating_sections_with_hub_and_spoke.json");
      // Accept cookies, this is done due to headless window size where cookie banner
      // is pushing the submit button outside window
      await $(HubPage.acceptCookies()).click();
      // Ensure we are on the Hub
      await expect(await browser.getUrl()).toContain(HubPage.url());
      // Ensure the first section is not started
      await expect(await $(HubPage.summaryRowState("section")).getText()).toBe("Not started");
      // Start first section to add household members
      await $(HubPage.summaryRowLink("section")).click();

      // Add a primary person
      await $(PrimaryPersonPage.yes()).click();
      await click(PrimaryPersonPage.submit());
      await $(PrimaryPersonAddPage.firstName()).setValue("Marcus");
      await $(PrimaryPersonAddPage.lastName()).setValue("Twin");
      await click(PrimaryPersonPage.submit());

      // Add other household members (First list collector)
      await $(FirstListCollectorPage.yes()).click();
      await click(FirstListCollectorPage.submit());
      await $(FirstListCollectorAddPage.firstName()).setValue("Jean");
      await $(FirstListCollectorAddPage.lastName()).setValue("Clemens");
      await click(FirstListCollectorAddPage.submit());

      await $(FirstListCollectorPage.yes()).click();
      await click(FirstListCollectorPage.submit());
      await $(FirstListCollectorAddPage.firstName()).setValue("Samuel");
      await $(FirstListCollectorAddPage.lastName()).setValue("Clemens");
      await click(FirstListCollectorAddPage.submit());

      // Go to second list collector
      await $(FirstListCollectorPage.no()).click();
      await click(FirstListCollectorPage.submit());
      await click(SecondListCollectorInterstitialPage.submit());

      // Add other household members (Second list collector)
      await $(SecondListCollectorPage.yes()).click();
      await click(SecondListCollectorPage.submit());
      await $(SecondListCollectorAddPage.firstName()).setValue("John");
      await $(SecondListCollectorAddPage.lastName()).setValue("Doe");
      await click(SecondListCollectorAddPage.submit());

      // Go back to the Hub
      await $(SecondListCollectorPage.no()).click();
      await click(SecondListCollectorPage.submit());
      await $(VisitorsListCollectorPage.no()).click();
      await click(VisitorsListCollectorPage.submit());
    });

    beforeEach("Navigate to the Hub", async () => await browser.url(HubPage.url()));

    it("Then a section for each household member should be displayed", async () => {
      await expect(await browser.getUrl()).toContain(HubPage.url());

      await expect(await $(HubPage.summaryRowState("section")).getText()).toBe("Completed");
      await expect(await $(HubPage.summaryRowTitle("personal-details-section-1")).getText()).toBe("Marcus Twin");
      await expect(await $(HubPage.summaryRowState("personal-details-section-1")).getText()).toBe("Not started");
      await expect(await $(HubPage.summaryRowState("personal-details-section-2")).getText()).toBe("Not started");
      await expect(await $(HubPage.summaryRowTitle("personal-details-section-2")).getText()).toBe("Jean Clemens");
      await expect(await $(HubPage.summaryRowState("personal-details-section-3")).getText()).toBe("Not started");
      await expect(await $(HubPage.summaryRowTitle("personal-details-section-3")).getText()).toBe("Samuel Clemens");
      await expect(await $(HubPage.summaryRowState("personal-details-section-4")).getText()).toBe("Not started");
      await expect(await $(HubPage.summaryRowTitle("personal-details-section-4")).getText()).toBe("John Doe");

      await expect(await $(HubPage.summaryRowState("section-5")).isExisting()).toBe(false);
    });

    it("When the user starts a repeating section and clicks the Previous link on the first question, Then they should be taken back to the Hub", async () => {
      await $(HubPage.summaryRowLink("personal-details-section-2")).click();
      await $(ProxyPage.previous()).click();

      await expect(await browser.getUrl()).toContain(HubPage.url());
    });

    it("When the user partially completes a repeating section, Then that section should be marked as 'Partially completed' on the Hub", async () => {
      await $(HubPage.summaryRowLink("personal-details-section-1")).click();
      await $(ProxyPage.yes()).click();
      await click(ProxyPage.submit());

      await $(DateOfBirthPage.day()).setValue("01");
      await $(DateOfBirthPage.month()).setValue("03");
      await $(DateOfBirthPage.year()).setValue("2000");
      await click(DateOfBirthPage.submit());

      await $(ConfirmDateOfBirthPage.confirmDateOfBirthYesPersonNameIsAgeOld()).click();
      await click(ConfirmDateOfBirthPage.submit());

      await browser.url(HubPage.url());

      await expect(await browser.getUrl()).toContain(HubPage.url());
      await expect(await $(HubPage.summaryRowState("personal-details-section-1")).getText()).toBe("Partially completed");
    });

    it("When the user continues with a partially completed repeating section, Then they are taken to the first incomplete block", async () => {
      await $(HubPage.summaryRowLink("personal-details-section-1")).click();

      await expect(await $(SexPage.questionText()).getText()).toBe("What is Marcus Twin’s sex?");
    });

    it("When the user completes a repeating section, Then that section should be marked as 'Completed' on the Hub", async () => {
      await $(HubPage.summaryRowLink("personal-details-section-2")).click();
      await $(ProxyPage.yes()).click();
      await click(ProxyPage.submit());

      await $(DateOfBirthPage.day()).setValue("09");
      await $(DateOfBirthPage.month()).setValue("09");
      await $(DateOfBirthPage.year()).setValue("1995");
      await click(DateOfBirthPage.submit());

      await $(ConfirmDateOfBirthPage.confirmDateOfBirthYesPersonNameIsAgeOld()).click();
      await click(ConfirmDateOfBirthPage.submit());

      await $(SexPage.female()).click();
      await click(SexPage.submit());

      await click(PersonalDetailsSummaryPage.submit());

      await expect(await browser.getUrl()).toContain(HubPage.url());
      await expect(await $(HubPage.summaryRowState("personal-details-section-2")).getText()).toBe("Completed");
    });

    it("When the user clicks 'View answers' for a completed repeating section, Then they are taken to the summary", async () => {
      await $(HubPage.summaryRowLink("personal-details-section-2")).click();
      await expect(await browser.getUrl()).toContain("/sections/personal-details-section");
    });

    it("When the user views the summary for a repeating section, Then the page title is shown", async () => {
      await $(HubPage.summaryRowLink("personal-details-section-2")).click();
      await expect(await browser.getTitle()).toBe("… - Hub & Spoke");
    });

    it("When the user adds 2 visitors to the household then a section for each visitor should be display on the hub", async () => {
      // Ensure no other sections exist
      await expect(await $(HubPage.summaryRowState("personal-details-section-5")).isExisting()).toBe(false);
      await expect(await $(HubPage.summaryRowState("visitors-section-1")).isExisting()).toBe(false);

      // Start section for first visitor
      await $(HubPage.summaryRowLink("section")).click();

      // Add first visitor
      await $(SectionSummaryPage.visitorListAddLink()).click();
      await $(VisitorsListCollectorAddPage.firstName()).setValue("Joe");
      await $(VisitorsListCollectorAddPage.lastName()).setValue("Public");
      await click(VisitorsListCollectorAddPage.submit());
      await expect(await browser.getUrl()).toContain("/questionnaire/visitors-block");

      // Add second visitor
      await $(VisitorsListCollectorPage.yes()).click();
      await click(VisitorsListCollectorPage.submit());
      await $(VisitorsListCollectorAddPage.firstName()).setValue("Yvonne");
      await $(VisitorsListCollectorAddPage.lastName()).setValue("Yoe");
      await click(VisitorsListCollectorAddPage.submit());

      // Exit the visitors list collector
      await $(VisitorsListCollectorPage.no()).click();
      await click(VisitorsListCollectorPage.submit());

      await click(SectionSummaryPage.submit());

      await expect(await $(HubPage.summaryRowState("visitors-section-1")).getText()).toBe("Not started");
      await expect(await $(HubPage.summaryRowTitle("visitors-section-1")).getText()).toBe("Joe Public");
      await expect(await $(HubPage.summaryRowState("visitors-section-2")).getText()).toBe("Not started");
      await expect(await $(HubPage.summaryRowTitle("visitors-section-2")).getText()).toBe("Yvonne Yoe");

      await expect(await $(HubPage.summaryRowState("visitors-section-3")).isExisting()).toBe(false);
    });

    it("When the user clicks 'Continue' from the Hub, Then they should progress to the first incomplete section", async () => {
      await click(HubPage.submit());
      await expect(await $(ConfirmDateOfBirthPage.questionText()).getText()).toBe("What is Marcus Twin’s sex?");
    });

    it("When the user answers on their behalf, Then they are shown the non proxy question variant", async () => {
      await $(HubPage.summaryRowLink("personal-details-section-4")).click();
      await $(ProxyPage.noIMAnsweringForMyself()).click();
      await click(ProxyPage.submit());

      await $(DateOfBirthPage.day()).setValue("07");
      await $(DateOfBirthPage.month()).setValue("07");
      await $(DateOfBirthPage.year()).setValue("1970");
      await click(DateOfBirthPage.submit());

      await $(ConfirmDateOfBirthPage.confirmDateOfBirthYesIAmAgeOld()).click();
      await click(ConfirmDateOfBirthPage.submit());

      await expect(await $(SexPage.questionText()).getText()).toBe("What is your sex?");
    });

    it("When the user answers on on behalf of someone else, Then they are shown the proxy question variant for the relevant repeating section", async () => {
      await $(HubPage.summaryRowLink("personal-details-section-3")).click();
      await $(ProxyPage.yes()).click();
      await click(ProxyPage.submit());

      await $(DateOfBirthPage.day()).setValue("11");
      await $(DateOfBirthPage.month()).setValue("11");
      await $(DateOfBirthPage.year()).setValue("1990");
      await click(DateOfBirthPage.submit());

      await $(ConfirmDateOfBirthPage.confirmDateOfBirthYesPersonNameIsAgeOld()).click();
      await click(ConfirmDateOfBirthPage.submit());
      await expect(await $(SexPage.questionText()).getText()).toBe("What is Samuel Clemens’ sex?");
    });

    it("When the user completes all sections, Then the Hub should be in the completed state", async () => {
      // Complete remaining sections
      await click(HubPage.submit());
      await $(SexPage.male()).click();
      await click(SexPage.submit());
      await click(PersonalDetailsSummaryPage.submit());

      await click(HubPage.submit());
      await click(SexPage.submit());
      await click(PersonalDetailsSummaryPage.submit());

      await click(HubPage.submit());
      await $(SexPage.female()).click();
      await click(SexPage.submit());
      await click(PersonalDetailsSummaryPage.submit());

      await click(HubPage.submit());
      await $(VisitorsDateOfBirthPage.day()).setValue("03");
      await $(VisitorsDateOfBirthPage.month()).setValue("09");
      await $(VisitorsDateOfBirthPage.year()).setValue("1975");
      await click(VisitorsDateOfBirthPage.submit());

      await click(HubPage.submit());
      await $(VisitorsDateOfBirthPage.day()).setValue("31");
      await $(VisitorsDateOfBirthPage.month()).setValue("07");
      await $(VisitorsDateOfBirthPage.year()).setValue("1999");
      await click(VisitorsDateOfBirthPage.submit());

      await expect(await $(HubPage.submit()).getText()).toBe("Submit survey");
      await expect(await $(HubPage.heading()).getText()).toBe("Submit survey");
    });

    it("When the user adds a new visitor, Then the Hub should not be in the completed state", async () => {
      await $(HubPage.summaryRowLink("section")).click();

      // Add another visitor
      await $(SectionSummaryPage.visitorListAddLink()).click();
      await $(VisitorsListCollectorAddPage.firstName()).setValue("Anna");
      await $(VisitorsListCollectorAddPage.lastName()).setValue("Doe");
      await click(VisitorsListCollectorAddPage.submit());

      await $(VisitorsListCollectorPage.no()).click();
      await click(VisitorsListCollectorPage.submit());

      await click(SectionSummaryPage.submit());

      // New visitor added to hub
      await expect(await $(HubPage.summaryRowState("visitors-section-3")).getText()).toBe("Not started");
      await expect(await $(HubPage.summaryRowState("visitors-section-3")).isExisting()).toBe(true);

      await expect(await $(HubPage.submit()).getText()).not.toBe("Submit survey");
      await expect(await $(HubPage.submit()).getText()).toBe("Continue");

      await expect(await $(HubPage.heading()).getText()).not.toBe("Submit survey");
      await expect(await $(HubPage.heading()).getText()).toBe("Choose another section to complete");
    });

    it("When the user removes a visitor, Then their section is not longer displayed on he Hub", async () => {
      // Ensure final householder exists
      await expect(await $(HubPage.summaryRowState("visitors-section-3")).isExisting()).toBe(true);

      await $(HubPage.summaryRowLink("section")).click();

      // Remove final visitor
      await $(SectionSummaryPage.visitorListRemoveLink(3)).click();

      await $(VisitorsListCollectorRemovePage.yes()).click();
      await click(VisitorsListCollectorPage.submit());
      await click(SectionSummaryPage.submit());

      // Ensure final householder no longer exists
      await expect(await $(HubPage.summaryRowState("visitors-section-3")).isExisting()).toBe(false);
    });

    it("When the user submits, it should show the thank you page", async () => {
      await click(HubPage.submit());
      await expect(await browser.getUrl()).toContain("thank-you");
    });
  });
});
