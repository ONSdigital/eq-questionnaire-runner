import checkPeopleInList from "../helpers";
import YouLiveHerePage from "../generated_pages/list_collector_variants/you-live-here-block.page.js";
import ListCollectorPage from "../generated_pages/list_collector_variants/list-collector.page.js";
import ListCollectorAddPage from "../generated_pages/list_collector_variants/list-collector-add.page.js";
import ListCollectorEditPage from "../generated_pages/list_collector_variants/list-collector-edit.page.js";
import ListCollectorRemovePage from "../generated_pages/list_collector_variants/list-collector-remove.page.js";
import ConfirmationPage from "../base_pages/confirmation.page.js";
import ThankYouPage from "../base_pages/thank-you.page.js";

describe("List Collector With Variants", () => {
  describe("Given that a person lives in house", () => {
    before("Load the survey", () => {
      browser.openQuestionnaire("test_list_collector_variants.json");
    });

    it("The user is asked questions about whether they live there", () => {
      $(YouLiveHerePage.yes()).click();
      $(YouLiveHerePage.submit()).click();
      expect($(ListCollectorPage.questionText()).getText()).to.equal("Does anyone else live at 1 Pleasant Lane?");
    });

    it("The user is able to add members of the household", () => {
      $(ListCollectorPage.anyoneElseYes()).click();
      $(ListCollectorPage.submit()).click();
      expect($(ListCollectorAddPage.questionText()).getText()).to.equal("What is the name of the person?");
      $(ListCollectorAddPage.firstName()).setValue("Samuel");
      $(ListCollectorAddPage.lastName()).setValue("Clemens");
      $(ListCollectorAddPage.submit()).click();
    });

    it("The user can see all household members in the summary", () => {
      const peopleExpected = ["Samuel Clemens"];
      checkPeopleInList(peopleExpected, ListCollectorPage.listLabel);
    });

    it("The questionnaire has the correct question text on the change and remove pages", () => {
      $(ListCollectorPage.listEditLink(1)).click();
      expect($(ListCollectorEditPage.questionText()).getText()).to.equal("What is the name of the person?");
      $(ListCollectorEditPage.previous()).click();
      $(ListCollectorPage.listRemoveLink(1)).click();
      expect($(ListCollectorRemovePage.questionText()).getText()).to.equal("Are you sure you want to remove this person?");
      $(ListCollectorRemovePage.previous()).click();
    });

    it("The questionnaire shows the confirmation page when no more people to add", () => {
      $(ListCollectorPage.anyoneElseNo()).click();
      $(ListCollectorPage.submit()).click();
      expect(browser.getUrl()).to.contain(ConfirmationPage.url());
    });

    it("The questionnaire allows submission", () => {
      $(ConfirmationPage.submit()).click();
      expect(browser.getUrl()).to.contain("thank-you");
    });
  });

  describe("Given a person does not live in house", () => {
    before("Load the survey", () => {
      browser.openQuestionnaire("test_list_collector_variants.json");
    });

    it("The user is asked questions about whether they live there", () => {
      $(YouLiveHerePage.no()).click();
      $(YouLiveHerePage.submit()).click();
      expect($(ListCollectorPage.questionText()).getText()).to.equal("Does anyone live at 1 Pleasant Lane?");
    });

    it("The user is able to add members of the household", () => {
      $(ListCollectorPage.anyoneElseYes()).click();
      $(ListCollectorPage.submit()).click();
      expect($(ListCollectorAddPage.questionText()).getText()).to.equal("What is the name of the person who isn’t you?");
      $(ListCollectorAddPage.firstName()).setValue("Samuel");
      $(ListCollectorAddPage.lastName()).setValue("Clemens");
      $(ListCollectorAddPage.submit()).click();
    });

    it("The user can see all household members in the summary", () => {
      const peopleExpected = ["Samuel Clemens"];
      checkPeopleInList(peopleExpected, ListCollectorPage.listLabel);
    });

    it("The questionnaire has the correct question text on the change and remove pages", () => {
      $(ListCollectorPage.listEditLink(1)).click();
      expect($(ListCollectorEditPage.questionText()).getText()).to.equal("What is the name of the person who isn’t you?");
      $(ListCollectorEditPage.previous()).click();
      $(ListCollectorPage.listRemoveLink(1)).click();
      expect($(ListCollectorRemovePage.questionText()).getText()).to.equal("Are you sure you want to remove this person who isn’t you?");
      $(ListCollectorRemovePage.previous()).click();
    });

    it("The questionnaire shows the confirmation page when no more people to add", () => {
      $(ListCollectorPage.anyoneElseNo()).click();
      $(ListCollectorPage.submit()).click();
      expect(browser.getUrl()).to.contain(ConfirmationPage.url());
    });

    it("The questionnaire allows submission", () => {
      $(ConfirmationPage.submit()).click();
      expect(browser.getUrl()).to.contain(ThankYouPage.url());
    });
  });
});
