import { checkItemsInList, click } from "../helpers";
import AnotherListCollectorPage from "../generated_pages/list_collector/another-list-collector-block.page.js";
import AnotherListCollectorAddPage from "../generated_pages/list_collector/another-list-collector-block-add.page.js";
import AnotherListCollectorEditPage from "../generated_pages/list_collector/another-list-collector-block-edit.page.js";
import AnotherListCollectorRemovePage from "../generated_pages/list_collector/another-list-collector-block-remove.page.js";
import ListCollectorPage from "../generated_pages/list_collector/list-collector.page.js";
import ListCollectorAddPage from "../generated_pages/list_collector/list-collector-add.page.js";
import ListCollectorEditPage from "../generated_pages/list_collector/list-collector-edit.page.js";
import ListCollectorRemovePage from "../generated_pages/list_collector/list-collector-remove.page.js";
import NextInterstitialPage from "../generated_pages/list_collector/next-interstitial.page.js";
import SummaryPage from "../generated_pages/list_collector/section-summary.page.js";
import PrimaryPersonListCollectorPage from "../generated_pages/list_collector_list_summary/primary-person-list-collector.page.js";
import PrimaryPersonListCollectorAddPage from "../generated_pages/list_collector_list_summary/primary-person-list-collector-add.page.js";
import SectionSummaryListCollectorPage from "../generated_pages/list_collector_list_summary/list-collector.page.js";
import SectionSummaryListCollectorAddPage from "../generated_pages/list_collector_list_summary/list-collector-add.page.js";
import SectionSummaryListCollectorEditPage from "../generated_pages/list_collector_list_summary/list-collector-edit.page.js";
import SectionSummaryListCollectorRemovePage from "../generated_pages/list_collector_list_summary/list-collector-remove.page.js";
import VisitorListCollectorPage from "../generated_pages/list_collector_list_summary/visitor-list-collector.page.js";
import VisitorListCollectorAddPage from "../generated_pages/list_collector_list_summary/visitor-list-collector-add.page.js";
import PeopleListSectionSummaryPage from "../generated_pages/list_collector_list_summary/section-summary.page.js";
import { SubmitPage } from "../base_pages/submit.page.js";
import IntroductionPage from "../generated_pages/list_collector_list_summary/introduction.page.js";

describe("List Collector", () => {
  describe("Given a normal journey through the list collector without variants", () => {
    before("Load the survey", async () => {
      await browser.openQuestionnaire("test_list_collector.json");
    });

    it("The user is able to add members of the household", async () => {
      await $(ListCollectorPage.yes()).click();
      await click(ListCollectorPage.submit());
      await $(ListCollectorAddPage.firstName()).setValue("Marcus");
      await $(ListCollectorAddPage.lastName()).setValue("Twin");
      await click(ListCollectorAddPage.submit());
      await $(ListCollectorPage.yes()).click();
      // eslint-disable-next-line no-undef
      await click(ListCollectorPage.submit());
      await $(ListCollectorAddPage.firstName()).setValue("Samuel");
      await $(ListCollectorAddPage.lastName()).setValue("Clemens");
      await click(ListCollectorAddPage.submit());
      await $(ListCollectorPage.yes()).click();
      await click(ListCollectorPage.submit());
      await $(ListCollectorAddPage.firstName()).setValue("Olivia");
      await $(ListCollectorAddPage.lastName()).setValue("Clemens");
      await click(ListCollectorAddPage.submit());
      await $(ListCollectorPage.yes()).click();
      await click(ListCollectorPage.submit());
      await $(ListCollectorAddPage.firstName()).setValue("Suzy");
      await $(ListCollectorAddPage.lastName()).setValue("Clemens");
      await click(ListCollectorAddPage.submit());
    });

    it("The collector shows all of the household members in the summary", async () => {
      const peopleExpected = ["Marcus Twin", "Samuel Clemens", "Olivia Clemens", "Suzy Clemens"];
      checkItemsInList(peopleExpected, ListCollectorPage.listLabel);
    });

    it("The questionnaire allows the name of a person to be changed", async () => {
      await $(ListCollectorPage.listEditLink(1)).click();
      await $(ListCollectorEditPage.firstName()).setValue("Mark");
      await $(ListCollectorEditPage.lastName()).setValue("Twain");
      await click(ListCollectorEditPage.submit());
      await expect(await $(ListCollectorPage.listLabel(1)).getText()).to.equal("Mark Twain");
    });

    it("The questionnaire allows me to remove the first person (Mark Twain) from the summary", async () => {
      await $(ListCollectorPage.listRemoveLink(1)).click();
      await $(ListCollectorRemovePage.yes()).click();
      await click(ListCollectorRemovePage.submit());
    });

    it("The collector summary does not show Mark Twain anymore.", async () => {
      await expect(await $(ListCollectorPage.listLabel(1)).getText()).to.not.have.string("Mark Twain");
      await expect(await $(ListCollectorPage.listLabel(3)).getText()).to.equal("Suzy Clemens");
    });

    it("The questionnaire allows more people to be added", async () => {
      await $(ListCollectorPage.yes()).click();
      await click(ListCollectorPage.submit());
      await expect(await $(ListCollectorAddPage.questionText()).getText()).to.contain("What is the name of the person");
      await $(ListCollectorAddPage.firstName()).setValue("Clara");
      await $(ListCollectorAddPage.lastName()).setValue("Clemens");
      await click(ListCollectorAddPage.submit());
      await $(ListCollectorPage.yes()).click();
      await click(ListCollectorPage.submit());
      await $(ListCollectorAddPage.firstName()).setValue("Jean");
      await $(ListCollectorAddPage.lastName()).setValue("Clemens");
      await click(ListCollectorAddPage.submit());
    });

    it("The user is returned to the list collector when the cancel link is clicked on the add page.", async () => {
      await $(ListCollectorPage.yes()).click();
      await click(ListCollectorPage.submit());
      await $(ListCollectorAddPage.firstName()).setValue("Someone");
      await $(ListCollectorAddPage.lastName()).setValue("Else");
      await $(ListCollectorAddPage.cancelAndReturn()).click();
      await expect(await browser.getUrl()).to.contain(ListCollectorPage.pageName);
    });

    it("The user is returned to the list collector when the cancel link is clicked on the edit page.", async () => {
      await $(ListCollectorPage.yes()).click();
      await click(ListCollectorPage.submit());
      await $(ListCollectorAddPage.firstName()).setValue("Someone");
      await $(ListCollectorAddPage.lastName()).setValue("Else");
      await click(ListCollectorAddPage.submit());
      await $(ListCollectorPage.listEditLink(1)).click();
      await $(ListCollectorEditPage.cancelAndReturn()).click();
      await expect(await browser.getUrl()).to.contain(ListCollectorPage.pageName);
    });

    it("The collector shows everyone on the summary", async () => {
      const peopleExpected = ["Samuel Clemens", "Olivia Clemens", "Suzy Clemens", "Clara Clemens", "Jean Clemens"];
      checkItemsInList(peopleExpected, ListCollectorPage.listLabel);
    });

    it("When No is answered on the list collector the user sees an interstitial", async () => {
      await $(ListCollectorPage.no()).click();
      await click(ListCollectorPage.submit());
      await expect(await browser.getUrl()).to.contain(NextInterstitialPage.pageName);
      await click(NextInterstitialPage.submit());
    });

    it("After the interstitial, the user should be on the second list collector page", async () => {
      await expect(await browser.getUrl()).to.contain(AnotherListCollectorPage.pageName);
    });

    it("The collector still shows the same list of people on the summary", async () => {
      const peopleExpected = ["Samuel Clemens", "Olivia Clemens", "Suzy Clemens", "Clara Clemens", "Jean Clemens"];
      checkItemsInList(peopleExpected, ListCollectorPage.listLabel);
    });

    it("The collector allows the user to add another person to the same list", async () => {
      await $(AnotherListCollectorPage.yes()).click();
      await click(AnotherListCollectorPage.submit());
      await $(AnotherListCollectorAddPage.firstName()).setValue("Someone");
      await $(AnotherListCollectorAddPage.lastName()).setValue("Else");
      await click(AnotherListCollectorAddPage.submit());
      await expect(await $(AnotherListCollectorPage.listLabel(6)).getText()).to.equal("Someone Else");
    });

    it("The collector allows the user to remove a person again", async () => {
      await $(AnotherListCollectorPage.listRemoveLink(5)).click();
      await $(AnotherListCollectorRemovePage.yes()).click();
      await click(AnotherListCollectorRemovePage.submit());
    });

    it("The user is returned to the list collector when the previous link is clicked.", async () => {
      await $(AnotherListCollectorPage.listRemoveLink(1)).click();
      await $(AnotherListCollectorRemovePage.previous()).click();
      await expect(await browser.getUrl()).to.contain(AnotherListCollectorPage.pageName);
      await $(AnotherListCollectorPage.listEditLink(1)).click();
      await $(AnotherListCollectorEditPage.previous()).click();
      await expect(await browser.getUrl()).to.contain(AnotherListCollectorPage.pageName);
      await $(AnotherListCollectorPage.yes()).click();
      await click(AnotherListCollectorPage.submit());
      await $(AnotherListCollectorEditPage.previous()).click();
      await expect(await browser.getUrl()).to.contain(AnotherListCollectorPage.pageName);
    });

    it("The questionnaire shows the confirmation page when no more people to add", async () => {
      await $(AnotherListCollectorPage.no()).click();
      await click(AnotherListCollectorPage.submit());
      await expect(await browser.getUrl()).to.contain("/sections/section/");
    });

    it("The questionnaire allows submission", async () => {
      await click(SummaryPage.submit());
      await click(SubmitPage.submit());
      await expect(await browser.getUrl()).to.contain("thank-you");
    });
  });

  describe("Given I start a list collector survey and complete to Section Summary", () => {
    beforeEach(async () => {
      await browser.openQuestionnaire("test_list_collector_list_summary.json");
      await click(IntroductionPage.submit());
      await $(PrimaryPersonListCollectorPage.yes()).click();
      await click(PrimaryPersonListCollectorPage.submit());
      await $(PrimaryPersonListCollectorAddPage.firstName()).setValue("Marcus");
      await $(PrimaryPersonListCollectorAddPage.lastName()).setValue("Twin");
      await click(PrimaryPersonListCollectorAddPage.submit());
      await $(SectionSummaryListCollectorPage.yes()).click();
      await click(SectionSummaryListCollectorPage.submit());
      await $(SectionSummaryListCollectorAddPage.firstName()).setValue("Samuel");
      await $(SectionSummaryListCollectorAddPage.lastName()).setValue("Clemens");
      await click(SectionSummaryListCollectorAddPage.submit());
      await $(SectionSummaryListCollectorPage.no()).click();
      await click(SectionSummaryListCollectorPage.submit());
      await $(VisitorListCollectorPage.yes()).click();
      await click(VisitorListCollectorPage.submit());
      await $(VisitorListCollectorAddPage.firstNameVisitor()).setValue("Olivia");
      await $(VisitorListCollectorAddPage.lastNameVisitor()).setValue("Clemens");
      await click(VisitorListCollectorAddPage.submit());
      await $(VisitorListCollectorPage.no()).click();
      await click(VisitorListCollectorPage.submit());
    });

    it("The section summary should display contents of the list collector", async () => {
      await expect(await $(PeopleListSectionSummaryPage.peopleListLabel(1)).getText()).to.contain("Marcus Twin (You)");
      await expect(await $(PeopleListSectionSummaryPage.peopleListLabel(2)).getText()).to.contain("Samuel Clemens");
      await expect(await $(PeopleListSectionSummaryPage.visitorsListLabel(1)).getText()).to.contain("Olivia Clemens");
    });

    it("When the user adds an item to the list, They should return to the section summary and it should display the updated list", async () => {
      await $(PeopleListSectionSummaryPage.visitorsListAddLink(1)).click();
      await $(VisitorListCollectorAddPage.firstNameVisitor()).setValue("Joe");
      await $(VisitorListCollectorAddPage.lastNameVisitor()).setValue("Bloggs");
      await click(VisitorListCollectorAddPage.submit());
      await $(VisitorListCollectorPage.no()).click();
      await click(VisitorListCollectorPage.submit());
      await expect(await $(PeopleListSectionSummaryPage.visitorsListLabel(2)).getText()).to.contain("Joe Bloggs");
    });

    it("When the user removes an item from the list, They should return to the section summary and it should display the updated list", async () => {
      await $(PeopleListSectionSummaryPage.peopleListRemoveLink(2)).click();
      await $(SectionSummaryListCollectorRemovePage.yes()).click();
      await click(SectionSummaryListCollectorRemovePage.submit());
      await expect(await $(PeopleListSectionSummaryPage.visitorsListLabel(2)).isExisting()).to.equal(false);
    });

    it("When the user updates the list, They should return to the section summary and it should display the updated list", async () => {
      await $(PeopleListSectionSummaryPage.peopleListEditLink(1)).click();
      await $(SectionSummaryListCollectorEditPage.firstName()).setValue("Mark");
      await $(SectionSummaryListCollectorEditPage.lastName()).setValue("Twain");
      await click(SectionSummaryListCollectorEditPage.submit());
      await expect(await $(PeopleListSectionSummaryPage.peopleListLabel(1)).getText()).to.contain("Mark Twain (You)");
    });

    it("When the user removes an item from the list, They should see the individual response guidance", async () => {
      await $(PeopleListSectionSummaryPage.peopleListRemoveLink(2)).click();
      await expect(await $(SectionSummaryListCollectorRemovePage.individualResponseGuidance()).isExisting()).to.equal(true);
    });

    it("When the user submits and navigates back, They should see the Section Summary", async () => {
      await click(PeopleListSectionSummaryPage.submit());
      await click(SubmitPage.previous());
      await expect(await browser.getUrl()).to.contain(PeopleListSectionSummaryPage.pageName);
    });
  });
});
