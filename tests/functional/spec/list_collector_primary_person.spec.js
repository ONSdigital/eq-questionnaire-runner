import ListCollectorPage from "../generated_pages/list_collector_primary_person/list-collector.page.js";
import ListCollectorAddPage from "../generated_pages/list_collector_primary_person/list-collector-add.page.js";
import ListCollectorEditPage from "../generated_pages/list_collector_primary_person/list-collector-edit.page.js";
import PrimaryPersonListCollectorPage from "../generated_pages/list_collector_primary_person/primary-person-list-collector.page.js";
import PrimaryPersonListCollectorAddPage from "../generated_pages/list_collector_primary_person/primary-person-list-collector-add.page.js";
import SectionSummaryPage from "../generated_pages/list_collector/section-summary.page.js";
import { SubmitPage } from "../base_pages/submit.page.js";
import ThankYouPage from "../base_pages/thank-you.page.js";
import AnyoneUsuallyLiveAtPage from "../generated_pages/list_collector_primary_person/anyone-usually-live-at.page.js";
import { click } from "../helpers";

describe("Primary Person List Collector Survey", () => {
  describe("Given the user starts on the 'do you live here' question", () => {
    before("Load the survey", async () => {
      await browser.openQuestionnaire("test_list_collector_primary_person.json");
    });

    it.skip("When the user says they do not live there, and changes their answer to yes, then the user can't navigate to the list collector", async () => {
      await $(PrimaryPersonListCollectorPage.noLabel()).click();
      await click(PrimaryPersonListCollectorPage.submit());
      await $(PrimaryPersonListCollectorAddPage.previous()).click();
      await $(PrimaryPersonListCollectorPage.yesLabel()).click();
      await click(PrimaryPersonListCollectorPage.submit());
      await browser.url("questionnaire/list-collector");
      await expect(await $(PrimaryPersonListCollectorPage.questionText()).getText()).toContain("Do you live here");
    });
  });

  describe("Given the user starts on the 'do you live here' question", () => {
    before("Load the survey", async () => {
      await browser.openQuestionnaire("test_list_collector_primary_person.json");
    });

    it("When the user says that they do live there, then they are shown as the primary person", async () => {
      await $(PrimaryPersonListCollectorPage.yesLabel()).click();
      await click(PrimaryPersonListCollectorPage.submit());
      await $(PrimaryPersonListCollectorAddPage.firstName()).setValue("Mark");
      await $(PrimaryPersonListCollectorAddPage.lastName()).setValue("Twin");
      await click(PrimaryPersonListCollectorAddPage.submit());
      await expect(await $(ListCollectorPage.listLabel(1)).getText()).toBe("Mark Twin (You)");
    });

    it("When the user adds another person, they are shown in the summary", async () => {
      await $(ListCollectorPage.yesLabel()).click();
      await click(ListCollectorPage.submit());
      await $(ListCollectorAddPage.firstName()).setValue("Samuel");
      await $(ListCollectorAddPage.lastName()).setValue("Clemens");
      await click(ListCollectorAddPage.submit());
      await expect(await $(ListCollectorPage.listLabel(2)).getText()).toBe("Samuel Clemens");
    });

    it("When the user goes back and answers No, the primary person is not shown", async () => {
      await $(ListCollectorPage.previous()).click();
      await $(PrimaryPersonListCollectorPage.no()).click();
      await click(PrimaryPersonListCollectorPage.submit());
      await $(AnyoneUsuallyLiveAtPage.no()).click();
      await click(AnyoneUsuallyLiveAtPage.submit());
      await expect(await $(ListCollectorPage.listLabel(1)).getText()).toBe("Samuel Clemens");
    });

    it("When the user adds the primary person again, then the primary person is first in the list", async () => {
      await $(ListCollectorPage.previous()).click();
      await $(AnyoneUsuallyLiveAtPage.previous()).click();
      await $(PrimaryPersonListCollectorPage.yes()).click();
      await click(PrimaryPersonListCollectorPage.submit());
      await $(PrimaryPersonListCollectorAddPage.firstName()).setValue("Mark");
      await $(PrimaryPersonListCollectorAddPage.lastName()).setValue("Twin");
      await click(PrimaryPersonListCollectorAddPage.submit());
      await expect(await $(ListCollectorPage.listLabel(1)).getText()).toBe("Mark Twin (You)");
    });

    it("When the user views the summary, then it does not show the remove link for the primary person", async () => {
      await expect(await $(ListCollectorPage.listRemoveLink(1)).isExisting()).toBe(false);
      await expect(await $(ListCollectorPage.listRemoveLink(2)).isExisting()).toBe(true);
    });

    it("When the user changes the primary person's name on the summary, then the name should be updated", async () => {
      await $(ListCollectorPage.listEditLink(1)).click();
      await $(ListCollectorEditPage.firstName()).setValue("Mark");
      await $(ListCollectorEditPage.lastName()).setValue("Twain");
      await click(ListCollectorEditPage.submit());
      await expect(await $(ListCollectorPage.listLabel(1)).getText()).toBe("Mark Twain (You)");
      await expect(await $(ListCollectorPage.listLabel(2)).getText()).toBe("Samuel Clemens");
    });

    it("When the user views the summary, then it does not show the does anyone usually live here question", async () => {
      await $(ListCollectorPage.no()).click();
      await click(ListCollectorPage.submit());
      await expect($("body").getText()).not.toBe("usually live here");
    });

    it("When the user attempts to submit, then they are shown the confirmation page", async () => {
      await click(SectionSummaryPage.submit());
      await expect(await $(SubmitPage.guidance()).getText()).toContain("Thank you for your answers, do you wish to submit");
    });

    it("When the user submits, then they are allowed to submit the survey", async () => {
      await click(SubmitPage.submit());
      await expect(await browser.getUrl()).toContain(ThankYouPage.pageName);
    });
  });

  describe("Given the user starts on the 'do you live here' question", () => {
    before("Load the survey", async () => {
      await browser.openQuestionnaire("test_list_collector_primary_person.json");
    });

    it("When the user says they do not live there, then an empty list is displayed", async () => {
      await $(PrimaryPersonListCollectorPage.no()).click();
      await click(PrimaryPersonListCollectorPage.submit());
      await $(AnyoneUsuallyLiveAtPage.no()).click();
      await expect(await $(ListCollectorPage.listLabel(1)).isExisting()).toBe(false);
    });

    it("When the user clicks on the add person button multiple times, then only one person is added", async () => {
      await $(ListCollectorPage.previous()).click();
      await $(PrimaryPersonListCollectorPage.yes()).click();
      await click(PrimaryPersonListCollectorPage.submit());
      await $(PrimaryPersonListCollectorAddPage.firstName()).setValue("Mark");
      await $(PrimaryPersonListCollectorAddPage.lastName()).setValue("Twain");
      await click(PrimaryPersonListCollectorPage.submit());
      await click(PrimaryPersonListCollectorPage.submit());
      await expect(await $(ListCollectorPage.listLabel(1)).getText()).toBe("Mark Twain (You)");
      await expect(await $(ListCollectorPage.listLabel(2)).isExisting()).toBe(false);
    });
  });
});
