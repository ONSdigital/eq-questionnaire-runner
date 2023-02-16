import checkPeopleInList from "../helpers";
import YouLiveHerePage from "../generated_pages/list_collector_variants/you-live-here-block.page.js";
import ListCollectorPage from "../generated_pages/list_collector_variants/list-collector.page.js";
import ListCollectorAddPage from "../generated_pages/list_collector_variants/list-collector-add.page.js";
import ListCollectorEditPage from "../generated_pages/list_collector_variants/list-collector-edit.page.js";
import ListCollectorRemovePage from "../generated_pages/list_collector_variants/list-collector-remove.page.js";
import { SubmitPage } from "../base_pages/submit.page.js";
import ThankYouPage from "../base_pages/thank-you.page.js";

describe("List Collector With Variants", () => {
  describe("Given that a person lives in house", () => {
    before("Load the survey", async ()=> {
      await browser.openQuestionnaire("test_list_collector_variants.json");
    });

    it("The user is asked questions about whether they live there", async ()=> {
      await $(await YouLiveHerePage.yes()).click();
      await $(await YouLiveHerePage.submit()).click();
      await expect(await $(await ListCollectorPage.questionText()).getText()).to.equal("Does anyone else live at 1 Pleasant Lane?");
    });

    it("The user is able to add members of the household", async ()=> {
      await $(await ListCollectorPage.anyoneElseYes()).click();
      await $(await ListCollectorPage.submit()).click();
      await expect(await $(await ListCollectorAddPage.questionText()).getText()).to.equal("What is the name of the person?");
      await $(await ListCollectorAddPage.firstName()).setValue("Samuel");
      await $(await ListCollectorAddPage.lastName()).setValue("Clemens");
      await $(await ListCollectorAddPage.submit()).click();
    });

    it("The user can see all household members in the summary", async ()=> {
      const peopleExpected = ["Samuel Clemens"];
      checkPeopleInList(peopleExpected, ListCollectorPage.listLabel);
    });

    it("The questionnaire has the correct question text on the change and remove pages", async ()=> {
      await $(await ListCollectorPage.listEditLink(1)).click();
      await expect(await $(await ListCollectorEditPage.questionText()).getText()).to.equal("What is the name of the person?");
      await $(await ListCollectorEditPage.previous()).click();
      await $(await ListCollectorPage.listRemoveLink(1)).click();
      await expect(await $(await ListCollectorRemovePage.questionText()).getText()).to.equal("Are you sure you want to remove this person?");
      await $(await ListCollectorRemovePage.previous()).click();
    });

    it("The questionnaire shows the confirmation page when no more people to add", async ()=> {
      await $(await ListCollectorPage.anyoneElseNo()).click();
      await $(await ListCollectorPage.submit()).click();
      await expect(browser.getUrl()).to.contain(SubmitPage.url());
    });

    it("The questionnaire allows submission", async ()=> {
      await $(await SubmitPage.submit()).click();
      await expect(browser.getUrl()).to.contain("thank-you");
    });
  });

  describe("Given a person does not live in house", () => {
    before("Load the survey", async ()=> {
      await browser.openQuestionnaire("test_list_collector_variants.json");
    });

    it("The user is asked questions about whether they live there", async ()=> {
      await $(await YouLiveHerePage.no()).click();
      await $(await YouLiveHerePage.submit()).click();
      await expect(await $(await ListCollectorPage.questionText()).getText()).to.equal("Does anyone live at 1 Pleasant Lane?");
    });

    it("The user is able to add members of the household", async ()=> {
      await $(await ListCollectorPage.anyoneElseYes()).click();
      await $(await ListCollectorPage.submit()).click();
      await expect(await $(await ListCollectorAddPage.questionText()).getText()).to.equal("What is the name of the person who isn’t you?");
      await $(await ListCollectorAddPage.firstName()).setValue("Samuel");
      await $(await ListCollectorAddPage.lastName()).setValue("Clemens");
      await $(await ListCollectorAddPage.submit()).click();
    });

    it("The user can see all household members in the summary", async ()=> {
      const peopleExpected = ["Samuel Clemens"];
      checkPeopleInList(peopleExpected, ListCollectorPage.listLabel);
    });

    it("The questionnaire has the correct question text on the change and remove pages", async ()=> {
      await $(await ListCollectorPage.listEditLink(1)).click();
      await expect(await $(await ListCollectorEditPage.questionText()).getText()).to.equal("What is the name of the person who isn’t you?");
      await $(await ListCollectorEditPage.previous()).click();
      await $(await ListCollectorPage.listRemoveLink(1)).click();
      await expect(await $(await ListCollectorRemovePage.questionText()).getText()).to.equal("Are you sure you want to remove this person who isn’t you?");
      await $(await ListCollectorRemovePage.previous()).click();
    });

    it("The questionnaire shows the confirmation page when no more people to add", async ()=> {
      await $(await ListCollectorPage.anyoneElseNo()).click();
      await $(await ListCollectorPage.submit()).click();
      await expect(browser.getUrl()).to.contain(SubmitPage.url());
    });

    it("The questionnaire allows submission", async ()=> {
      await $(await SubmitPage.submit()).click();
      await expect(browser.getUrl()).to.contain(ThankYouPage.url());
    });
  });
});
