import checkPeopleInList from "../helpers";
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

describe("List Collector", () => {
  describe("Given a normal journey through the list collector without variants", () => {
    before("Load the survey", async ()=> {
      await browser.openQuestionnaire("test_list_collector.json");
    });

    it("The user is able to add members of the household", async ()=> {
      await $(await ListCollectorPage.yes()).click();
      await $(await ListCollectorPage.submit()).click();
      await $(await ListCollectorAddPage.firstName()).setValue("Marcus");
      await $(await ListCollectorAddPage.lastName()).setValue("Twin");
      await $(await ListCollectorAddPage.submit()).click();
      await $(await ListCollectorPage.yes()).click();
      await $(await ListCollectorPage.submit()).click();
      await $(await ListCollectorAddPage.firstName()).setValue("Samuel");
      await $(await ListCollectorAddPage.lastName()).setValue("Clemens");
      await $(await ListCollectorAddPage.submit()).click();
      await $(await ListCollectorPage.yes()).click();
      await $(await ListCollectorPage.submit()).click();
      await $(await ListCollectorAddPage.firstName()).setValue("Olivia");
      await $(await ListCollectorAddPage.lastName()).setValue("Clemens");
      await $(await ListCollectorAddPage.submit()).click();
      await $(await ListCollectorPage.yes()).click();
      await $(await ListCollectorPage.submit()).click();
      await $(await ListCollectorAddPage.firstName()).setValue("Suzy");
      await $(await ListCollectorAddPage.lastName()).setValue("Clemens");
      await $(await ListCollectorAddPage.submit()).click();
    });

    it("The collector shows all of the household members in the summary", async ()=> {
      const peopleExpected = ["Marcus Twin", "Samuel Clemens", "Olivia Clemens", "Suzy Clemens"];
      checkPeopleInList(peopleExpected, ListCollectorPage.listLabel);
    });

    it("The questionnaire allows the name of a person to be changed", async ()=> {
      await $(await ListCollectorPage.listEditLink(1)).click();
      await $(await ListCollectorEditPage.firstName()).setValue("Mark");
      await $(await ListCollectorEditPage.lastName()).setValue("Twain");
      await $(await ListCollectorEditPage.submit()).click();
      await expect(await $(await ListCollectorPage.listLabel(1)).getText()).to.equal("Mark Twain");
    });

    it("The questionnaire allows me to remove the first person (Mark Twain) from the summary", async ()=> {
      await $(await ListCollectorPage.listRemoveLink(1)).click();
      await $(await ListCollectorRemovePage.yes()).click();
      await $(await ListCollectorRemovePage.submit()).click();
    });

    it("The collector summary does not show Mark Twain anymore.", async ()=> {
      await expect(await $(await ListCollectorPage.listLabel(1)).getText()).to.not.have.string("Mark Twain");
      await expect(await $(await ListCollectorPage.listLabel(3)).getText()).to.equal("Suzy Clemens");
    });

    it("The questionnaire allows more people to be added", async ()=> {
      await $(await ListCollectorPage.yes()).click();
      await $(await ListCollectorPage.submit()).click();
      await expect(await $(await ListCollectorAddPage.questionText()).getText()).to.contain("What is the name of the person");
      await $(await ListCollectorAddPage.firstName()).setValue("Clara");
      await $(await ListCollectorAddPage.lastName()).setValue("Clemens");
      await $(await ListCollectorAddPage.submit()).click();
      await $(await ListCollectorPage.yes()).click();
      await $(await ListCollectorPage.submit()).click();
      await $(await ListCollectorAddPage.firstName()).setValue("Jean");
      await $(await ListCollectorAddPage.lastName()).setValue("Clemens");
      await $(await ListCollectorAddPage.submit()).click();
    });

    it("The user is returned to the list collector when the cancel link is clicked on the add page.", async ()=> {
      await $(await ListCollectorPage.yes()).click();
      await $(await ListCollectorPage.submit()).click();
      await $(await ListCollectorAddPage.firstName()).setValue("Someone");
      await $(await ListCollectorAddPage.lastName()).setValue("Else");
      await $(await ListCollectorAddPage.cancelAndReturn()).click();
      await expect(browser.getUrl()).to.contain(ListCollectorPage.pageName);
    });

    it("The user is returned to the list collector when the cancel link is clicked on the edit page.", async ()=> {
      await $(await ListCollectorPage.yes()).click();
      await $(await ListCollectorPage.submit()).click();
      await $(await ListCollectorAddPage.firstName()).setValue("Someone");
      await $(await ListCollectorAddPage.lastName()).setValue("Else");
      await $(await ListCollectorAddPage.submit()).click();
      await $(await ListCollectorPage.listEditLink(1)).click();
      await $(await ListCollectorEditPage.cancelAndReturn()).click();
      await expect(browser.getUrl()).to.contain(ListCollectorPage.pageName);
    });

    it("The collector shows everyone on the summary", async ()=> {
      const peopleExpected = ["Samuel Clemens", "Olivia Clemens", "Suzy Clemens", "Clara Clemens", "Jean Clemens"];
      checkPeopleInList(peopleExpected, ListCollectorPage.listLabel);
    });

    it("When No is answered on the list collector the user sees an interstitial", async ()=> {
      await $(await ListCollectorPage.no()).click();
      await $(await ListCollectorPage.submit()).click();
      await expect(browser.getUrl()).to.contain(NextInterstitialPage.pageName);
      await $(await NextInterstitialPage.submit()).click();
    });

    it("After the interstitial, the user should be on the second list collector page", async ()=> {
      await expect(browser.getUrl()).to.contain(AnotherListCollectorPage.pageName);
    });

    it("The collector still shows the same list of people on the summary", async ()=> {
      const peopleExpected = ["Samuel Clemens", "Olivia Clemens", "Suzy Clemens", "Clara Clemens", "Jean Clemens"];
      checkPeopleInList(peopleExpected, ListCollectorPage.listLabel);
    });

    it("The collector allows the user to add another person to the same list", async ()=> {
      await $(await AnotherListCollectorPage.yes()).click();
      await $(await AnotherListCollectorPage.submit()).click();
      await $(await AnotherListCollectorAddPage.firstName()).setValue("Someone");
      await $(await AnotherListCollectorAddPage.lastName()).setValue("Else");
      await $(await AnotherListCollectorAddPage.submit()).click();
      await expect(await $(await AnotherListCollectorPage.listLabel(6)).getText()).to.equal("Someone Else");
    });

    it("The collector allows the user to remove a person again", async ()=> {
      await $(await AnotherListCollectorPage.listRemoveLink(5)).click();
      await $(await AnotherListCollectorRemovePage.yes()).click();
      await $(await AnotherListCollectorRemovePage.submit()).click();
    });

    it("The user is returned to the list collector when the previous link is clicked.", async ()=> {
      await $(await AnotherListCollectorPage.listRemoveLink(1)).click();
      await $(await AnotherListCollectorRemovePage.previous()).click();
      await expect(browser.getUrl()).to.contain(AnotherListCollectorPage.pageName);
      await $(await AnotherListCollectorPage.listEditLink(1)).click();
      await $(await AnotherListCollectorEditPage.previous()).click();
      await expect(browser.getUrl()).to.contain(AnotherListCollectorPage.pageName);
      await $(await AnotherListCollectorPage.yes()).click();
      await $(await AnotherListCollectorPage.submit()).click();
      await $(await AnotherListCollectorEditPage.previous()).click();
      await expect(browser.getUrl()).to.contain(AnotherListCollectorPage.pageName);
    });

    it("The questionnaire shows the confirmation page when no more people to add", async ()=> {
      await $(await AnotherListCollectorPage.no()).click();
      await $(await AnotherListCollectorPage.submit()).click();
      await expect(browser.getUrl()).to.contain("/sections/section/");
    });

    it("The questionnaire allows submission", async ()=> {
      await $(await SummaryPage.submit()).click();
      await $(await SubmitPage.submit()).click();
      await expect(browser.getUrl()).to.contain("thank-you");
    });
  });

  describe("Given I start a list collector survey and complete to Section Summary", () => {
    beforeEach(async ()=> {
      await browser.openQuestionnaire("test_list_collector_list_summary.json");
      await $(await PrimaryPersonListCollectorPage.yes()).click();
      await $(await PrimaryPersonListCollectorPage.submit()).click();
      await $(await PrimaryPersonListCollectorAddPage.firstName()).setValue("Marcus");
      await $(await PrimaryPersonListCollectorAddPage.lastName()).setValue("Twin");
      await $(await PrimaryPersonListCollectorAddPage.submit()).click();
      await $(await SectionSummaryListCollectorPage.yes()).click();
      await $(await SectionSummaryListCollectorPage.submit()).click();
      await $(await SectionSummaryListCollectorAddPage.firstName()).setValue("Samuel");
      await $(await SectionSummaryListCollectorAddPage.lastName()).setValue("Clemens");
      await $(await SectionSummaryListCollectorAddPage.submit()).click();
      await $(await SectionSummaryListCollectorPage.no()).click();
      await $(await SectionSummaryListCollectorPage.submit()).click();
      await $(await VisitorListCollectorPage.yes()).click();
      await $(await VisitorListCollectorPage.submit()).click();
      await $(await VisitorListCollectorAddPage.firstNameVisitor()).setValue("Olivia");
      await $(await VisitorListCollectorAddPage.lastNameVisitor()).setValue("Clemens");
      await $(await VisitorListCollectorAddPage.submit()).click();
      await $(await VisitorListCollectorPage.no()).click();
      await $(await VisitorListCollectorPage.submit()).click();
    });

    it("The section summary should display contents of the list collector", async ()=> {
      await expect(await $(await PeopleListSectionSummaryPage.peopleListLabel(1)).getText()).to.contain("Marcus Twin (You)");
      await expect(await $(await PeopleListSectionSummaryPage.peopleListLabel(2)).getText()).to.contain("Samuel Clemens");
      await expect(await $(await PeopleListSectionSummaryPage.visitorsListLabel(1)).getText()).to.contain("Olivia Clemens");
    });

    it("When the user adds an item to the list, They should return to the section summary and it should display the updated list", async ()=> {
      await $(await PeopleListSectionSummaryPage.visitorsListAddLink(1)).click();
      await $(await VisitorListCollectorAddPage.firstNameVisitor()).setValue("Joe");
      await $(await VisitorListCollectorAddPage.lastNameVisitor()).setValue("Bloggs");
      await $(await VisitorListCollectorAddPage.submit()).click();
      await expect(await $(await PeopleListSectionSummaryPage.visitorsListLabel(2)).getText()).to.contain("Joe Bloggs");
    });

    it("When the user removes an item from the list, They should return to the section summary and it should display the updated list", async ()=> {
      await $(await PeopleListSectionSummaryPage.peopleListRemoveLink(2)).click();
      await $(await SectionSummaryListCollectorRemovePage.yes()).click();
      await $(await SectionSummaryListCollectorRemovePage.submit()).click();
      await expect(await $(await PeopleListSectionSummaryPage.visitorsListLabel(2)).isExisting()).to.equal(false);
    });

    it("When the user updates the list, They should return to the section summary and it should display the updated list", async ()=> {
      await $(await PeopleListSectionSummaryPage.peopleListEditLink(1)).click();
      await $(await SectionSummaryListCollectorEditPage.firstName()).setValue("Mark");
      await $(await SectionSummaryListCollectorEditPage.lastName()).setValue("Twain");
      await $(await SectionSummaryListCollectorEditPage.submit()).click();
      await expect(await $(await PeopleListSectionSummaryPage.peopleListLabel(1)).getText()).to.contain("Mark Twain (You)");
    });

    it("When the user removes an item from the list, They should see the individual response guidance", async ()=> {
      await $(await PeopleListSectionSummaryPage.peopleListRemoveLink(2)).click();
      await expect(await $(await SectionSummaryListCollectorRemovePage.individualResponseGuidance()).isExisting()).to.equal(true);
    });
  });
});
