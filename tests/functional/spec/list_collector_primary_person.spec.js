import ListCollectorPage from "../generated_pages/list_collector_primary_person/list-collector.page.js";
import ListCollectorAddPage from "../generated_pages/list_collector_primary_person/list-collector-add.page.js";
import ListCollectorEditPage from "../generated_pages/list_collector_primary_person/list-collector-edit.page.js";
import PrimaryPersonListCollectorPage from "../generated_pages/list_collector_primary_person/primary-person-list-collector.page.js";
import PrimaryPersonListCollectorAddPage from "../generated_pages/list_collector_primary_person/primary-person-list-collector-add.page.js";
import SectionSummaryPage from "../generated_pages/list_collector/section-summary.page.js";
import ConfirmationPage from "../base_pages/confirmation.page.js";
import ThankYouPage from "../base_pages/thank-you.page.js";
import AnyoneUsuallyLiveAtPage from "../generated_pages/list_collector_primary_person/anyone-usually-live-at.page.js";

describe("Primary Person List Collector Survey", () => {
  describe("Given the user starts on the 'do you live here' question", () => {
    before("Load the survey", () => {
      browser.openQuestionnaire("test_list_collector_primary_person.json");
    });

    it.skip("When the user says they do not live there, and changes their answer to yes, then the user can't navigate to the list collector", () => {
      $(PrimaryPersonListCollectorPage.noLabel()).click();
      $(PrimaryPersonListCollectorPage.submit()).click();
      $(PrimaryPersonListCollectorAddPage.previous()).click();
      $(PrimaryPersonListCollectorPage.yesLabel()).click();
      $(PrimaryPersonListCollectorPage.submit()).click();
      browser.url("questionnaire/list-collector");
      expect($(PrimaryPersonListCollectorPage.questionText()).getText()).to.contain("Do you live here");
    });
  });

  describe("Given the user starts on the 'do you live here' question", () => {
    before("Load the survey", () => {
      browser.openQuestionnaire("test_list_collector_primary_person.json");
    });

    it("When the user says that they do live there, then they are shown as the primary person", () => {
      $(PrimaryPersonListCollectorPage.yesLabel()).click();
      $(PrimaryPersonListCollectorPage.submit()).click();
      $(PrimaryPersonListCollectorAddPage.firstName()).setValue("Mark");
      $(PrimaryPersonListCollectorAddPage.lastName()).setValue("Twin");
      $(PrimaryPersonListCollectorAddPage.submit()).click();
      expect($(ListCollectorPage.listLabel(1)).getText()).to.equal("Mark Twin (You)");
    });

    it("When the user adds another person, they are shown in the summary", () => {
      $(ListCollectorPage.yesLabel()).click();
      $(ListCollectorPage.submit()).click();
      $(ListCollectorAddPage.firstName()).setValue("Samuel");
      $(ListCollectorAddPage.lastName()).setValue("Clemens");
      $(ListCollectorAddPage.submit()).click();
      expect($(ListCollectorPage.listLabel(2)).getText()).to.equal("Samuel Clemens");
    });

    it("When the user goes back and answers No, the primary person is not shown", () => {
      $(ListCollectorPage.previous()).click();
      $(PrimaryPersonListCollectorPage.no()).click();
      $(PrimaryPersonListCollectorPage.submit()).click();
      $(AnyoneUsuallyLiveAtPage.no()).click();
      $(AnyoneUsuallyLiveAtPage.submit()).click();
      expect($(ListCollectorPage.listLabel(1)).getText()).to.equal("Samuel Clemens");
    });

    it("When the user adds the primary person again, then the primary person is first in the list", () => {
      $(ListCollectorPage.previous()).click();
      $(AnyoneUsuallyLiveAtPage.previous()).click();
      $(PrimaryPersonListCollectorPage.yes()).click();
      $(PrimaryPersonListCollectorPage.submit()).click();
      $(PrimaryPersonListCollectorAddPage.firstName()).setValue("Mark");
      $(PrimaryPersonListCollectorAddPage.lastName()).setValue("Twin");
      $(PrimaryPersonListCollectorAddPage.submit()).click();
      expect($(ListCollectorPage.listLabel(1)).getText()).to.equal("Mark Twin (You)");
    });

    it("When the user views the summary, then it does not show the remove link for the primary person", () => {
      expect($(ListCollectorPage.listRemoveLink(1)).isExisting()).to.be.false;
      expect($(ListCollectorPage.listRemoveLink(2)).isExisting()).to.be.true;
    });

    it("When the user changes the primary person's name on the summary, then the name should be updated", () => {
      $(ListCollectorPage.listEditLink(1)).click();
      $(ListCollectorEditPage.firstName()).setValue("Mark");
      $(ListCollectorEditPage.lastName()).setValue("Twain");
      $(ListCollectorEditPage.submit()).click();
      expect($(ListCollectorPage.listLabel(1)).getText()).to.equal("Mark Twain (You)");
      expect($(ListCollectorPage.listLabel(2)).getText()).to.equal("Samuel Clemens");
    });

    it("When the user views the summary, then it does not show the does anyone usually live here question", () => {
      $(ListCollectorPage.no()).click();
      $(ListCollectorPage.submit()).click();
      expect($("body").getText()).to.not.equal("usually live here");
    });

    it("When the user attempts to submit, then they are shown the confirmation page", () => {
      $(SectionSummaryPage.submit()).click();
      expect($(ConfirmationPage.guidance()).getText()).to.contain("Thank you for your answers, do you wish to submit");
    });

    it("When the user submits, then they are allowed to submit the survey", () => {
      $(ConfirmationPage.submit()).click();
      expect($(ThankYouPage.questionText()).getText()).to.contain("Submission successful");
    });
  });

  describe("Given the user starts on the 'do you live here' question", () => {
    before("Load the survey", () => {
      browser.openQuestionnaire("test_list_collector_primary_person.json");
    });

    it("When the user says they do not live there, then an empty list is displayed", () => {
      $(PrimaryPersonListCollectorPage.no()).click();
      $(PrimaryPersonListCollectorPage.submit()).click();
      $(AnyoneUsuallyLiveAtPage.no()).click();
      expect($(ListCollectorPage.listLabel(1)).isExisting()).to.be.false;
    });

    it("When the user clicks on the add person button multiple times, then only one person is added", () => {
      $(ListCollectorPage.previous()).click();
      $(PrimaryPersonListCollectorPage.yes()).click();
      $(PrimaryPersonListCollectorPage.submit()).click();
      $(PrimaryPersonListCollectorAddPage.firstName()).setValue("Mark");
      $(PrimaryPersonListCollectorAddPage.lastName()).setValue("Twain");
      $(PrimaryPersonListCollectorPage.submit()).click();
      $(PrimaryPersonListCollectorPage.submit()).click();
      expect($(ListCollectorPage.listLabel(1)).getText()).to.equal("Mark Twain (You)");
      expect($(ListCollectorPage.listLabel(2)).isExisting()).to.be.false;
    });
  });
});
