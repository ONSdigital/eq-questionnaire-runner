import ListCollectorPage from "../generated_pages/list_collector_primary_person/list-collector.page.js";
import ListCollectorAddPage from "../generated_pages/list_collector_primary_person/list-collector-add.page.js";
import ListCollectorEditPage from "../generated_pages/list_collector_primary_person/list-collector-edit.page.js";
import PrimaryPersonListCollectorPage from "../generated_pages/list_collector_primary_person/primary-person-list-collector.page.js";
import PrimaryPersonListCollectorAddPage from "../generated_pages/list_collector_primary_person/primary-person-list-collector-add.page.js";
import SectionSummaryPage from "../generated_pages/list_collector/section-summary.page.js";
import { SubmitPage } from "../base_pages/submit.page.js";
import ThankYouPage from "../base_pages/thank-you.page.js";
import AnyoneUsuallyLiveAtPage from "../generated_pages/list_collector_primary_person/anyone-usually-live-at.page.js";

describe("Primary Person List Collector Survey", () => {
  describe("Given the user starts on the 'do you live here' question", () => {
    before("Load the survey", async ()=> {
      await browser.openQuestionnaire("test_list_collector_primary_person.json");
    });

    it.skip("When the user says they do not live there, and changes their answer to yes, then the user can't navigate to the list collector", async ()=> {
      await $(await PrimaryPersonListCollectorPage.noLabel()).click();
      await $(await PrimaryPersonListCollectorPage.submit()).click();
      await $(await PrimaryPersonListCollectorAddPage.previous()).click();
      await $(await PrimaryPersonListCollectorPage.yesLabel()).click();
      await $(await PrimaryPersonListCollectorPage.submit()).click();
      browser.url("questionnaire/list-collector");
      await expect(await $(await PrimaryPersonListCollectorPage.questionText()).getText()).to.contain("Do you live here");
    });
  });

  describe("Given the user starts on the 'do you live here' question", () => {
    before("Load the survey", async ()=> {
      await browser.openQuestionnaire("test_list_collector_primary_person.json");
    });

    it("When the user says that they do live there, then they are shown as the primary person", async ()=> {
      await $(await PrimaryPersonListCollectorPage.yesLabel()).click();
      await $(await PrimaryPersonListCollectorPage.submit()).click();
      await $(await PrimaryPersonListCollectorAddPage.firstName()).setValue("Mark");
      await $(await PrimaryPersonListCollectorAddPage.lastName()).setValue("Twin");
      await $(await PrimaryPersonListCollectorAddPage.submit()).click();
      await expect(await $(await ListCollectorPage.listLabel(1)).getText()).to.equal("Mark Twin (You)");
    });

    it("When the user adds another person, they are shown in the summary", async ()=> {
      await $(await ListCollectorPage.yesLabel()).click();
      await $(await ListCollectorPage.submit()).click();
      await $(await ListCollectorAddPage.firstName()).setValue("Samuel");
      await $(await ListCollectorAddPage.lastName()).setValue("Clemens");
      await $(await ListCollectorAddPage.submit()).click();
      await expect(await $(await ListCollectorPage.listLabel(2)).getText()).to.equal("Samuel Clemens");
    });

    it("When the user goes back and answers No, the primary person is not shown", async ()=> {
      await $(await ListCollectorPage.previous()).click();
      await $(await PrimaryPersonListCollectorPage.no()).click();
      await $(await PrimaryPersonListCollectorPage.submit()).click();
      await $(await AnyoneUsuallyLiveAtPage.no()).click();
      await $(await AnyoneUsuallyLiveAtPage.submit()).click();
      await expect(await $(await ListCollectorPage.listLabel(1)).getText()).to.equal("Samuel Clemens");
    });

    it("When the user adds the primary person again, then the primary person is first in the list", async ()=> {
      await $(await ListCollectorPage.previous()).click();
      await $(await AnyoneUsuallyLiveAtPage.previous()).click();
      await $(await PrimaryPersonListCollectorPage.yes()).click();
      await $(await PrimaryPersonListCollectorPage.submit()).click();
      await $(await PrimaryPersonListCollectorAddPage.firstName()).setValue("Mark");
      await $(await PrimaryPersonListCollectorAddPage.lastName()).setValue("Twin");
      await $(await PrimaryPersonListCollectorAddPage.submit()).click();
      await expect(await $(await ListCollectorPage.listLabel(1)).getText()).to.equal("Mark Twin (You)");
    });

    it("When the user views the summary, then it does not show the remove link for the primary person", async ()=> {
      await expect(await $(await ListCollectorPage.listRemoveLink(1)).isExisting()).to.be.false;
      await expect(await $(await ListCollectorPage.listRemoveLink(2)).isExisting()).to.be.true;
    });

    it("When the user changes the primary person's name on the summary, then the name should be updated", async ()=> {
      await $(await ListCollectorPage.listEditLink(1)).click();
      await $(await ListCollectorEditPage.firstName()).setValue("Mark");
      await $(await ListCollectorEditPage.lastName()).setValue("Twain");
      await $(await ListCollectorEditPage.submit()).click();
      await expect(await $(await ListCollectorPage.listLabel(1)).getText()).to.equal("Mark Twain (You)");
      await expect(await $(await ListCollectorPage.listLabel(2)).getText()).to.equal("Samuel Clemens");
    });

    it("When the user views the summary, then it does not show the does anyone usually live here question", async ()=> {
      await $(await ListCollectorPage.no()).click();
      await $(await ListCollectorPage.submit()).click();
      await expect($("body").getText()).to.not.equal("usually live here");
    });

    it("When the user attempts to submit, then they are shown the confirmation page", async ()=> {
      await $(await SectionSummaryPage.submit()).click();
      await expect(await $(await SubmitPage.guidance()).getText()).to.contain("Thank you for your answers, do you wish to submit");
    });

    it("When the user submits, then they are allowed to submit the survey", async ()=> {
      await $(await SubmitPage.submit()).click();
      await expect(browser.getUrl()).to.contain(ThankYouPage.pageName);
    });
  });

  describe("Given the user starts on the 'do you live here' question", () => {
    before("Load the survey", async ()=> {
      await browser.openQuestionnaire("test_list_collector_primary_person.json");
    });

    it("When the user says they do not live there, then an empty list is displayed", async ()=> {
      await $(await PrimaryPersonListCollectorPage.no()).click();
      await $(await PrimaryPersonListCollectorPage.submit()).click();
      await $(await AnyoneUsuallyLiveAtPage.no()).click();
      await expect(await $(await ListCollectorPage.listLabel(1)).isExisting()).to.be.false;
    });

    it("When the user clicks on the add person button multiple times, then only one person is added", async ()=> {
      await $(await ListCollectorPage.previous()).click();
      await $(await PrimaryPersonListCollectorPage.yes()).click();
      await $(await PrimaryPersonListCollectorPage.submit()).click();
      await $(await PrimaryPersonListCollectorAddPage.firstName()).setValue("Mark");
      await $(await PrimaryPersonListCollectorAddPage.lastName()).setValue("Twain");
      await $(await PrimaryPersonListCollectorPage.submit()).click();
      await $(await PrimaryPersonListCollectorPage.submit()).click();
      await expect(await $(await ListCollectorPage.listLabel(1)).getText()).to.equal("Mark Twain (You)");
      await expect(await $(await ListCollectorPage.listLabel(2)).isExisting()).to.be.false;
    });
  });
});
