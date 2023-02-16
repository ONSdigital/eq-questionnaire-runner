import checkPeopleInList from "../helpers";
import HubPage from "../base_pages/hub.page.js";
import AnyoneUsuallyLiveAtPage from "../generated_pages/list_collector_driving_question/anyone-usually-live-at.page.js";
import AnyoneElseLiveAtListCollectorPage from "../generated_pages/list_collector_driving_question/anyone-else-live-at.page.js";
import AnyoneElseLiveAtListCollectorAddPage from "../generated_pages/list_collector_driving_question/anyone-else-live-at-add.page.js";
import AnyoneElseLiveAtListCollectorRemovePage from "../generated_pages/list_collector_driving_question/anyone-else-live-at-remove.page.js";
import SectionSummaryPage from "../generated_pages/list_collector_driving_question/section-summary.page.js";

describe("List Collector Driving Question", () => {
  beforeEach("Load the survey", async ()=> {
    await browser.openQuestionnaire("test_list_collector_driving_question.json");
    await $(await HubPage.submit()).click();
  });

  describe("Given a happy journey through the list collector", () => {
    it("The collector shows all of the household members in the summary", async ()=> {
      await $(await AnyoneUsuallyLiveAtPage.yes()).click();
      await $(await AnyoneUsuallyLiveAtPage.submit()).click();
      await $(await AnyoneElseLiveAtListCollectorAddPage.firstName()).setValue("Marcus");
      await $(await AnyoneElseLiveAtListCollectorAddPage.lastName()).setValue("Twin");
      await $(await AnyoneElseLiveAtListCollectorAddPage.submit()).click();
      await $(await AnyoneElseLiveAtListCollectorPage.yes()).click();
      await $(await AnyoneElseLiveAtListCollectorPage.submit()).click();
      await $(await AnyoneElseLiveAtListCollectorAddPage.firstName()).setValue("Suzy");
      await $(await AnyoneElseLiveAtListCollectorAddPage.lastName()).setValue("Clemens");
      await $(await AnyoneElseLiveAtListCollectorAddPage.submit()).click();
      await $(await AnyoneElseLiveAtListCollectorPage.no()).click();
      await $(await AnyoneElseLiveAtListCollectorPage.submit()).click();

      const peopleExpected = ["Marcus Twin", "Suzy Clemens"];

      checkPeopleInList(peopleExpected, SectionSummaryPage.peopleListLabel);
    });
  });

  describe("Given the user answers no to the driving question", () => {
    it("The summary add link returns to the driving question", async ()=> {
      await $(await AnyoneUsuallyLiveAtPage.no()).click();
      await $(await AnyoneUsuallyLiveAtPage.submit()).click();
      await $(await SectionSummaryPage.peopleListAddLink()).click();
      await expect(browser.getUrl()).to.contain(AnyoneUsuallyLiveAtPage.url());
    });
  });

  describe("Given the user answers yes to the driving question, adds someone and later removes them", () => {
    it("The summary add link should return to the original list collector", async ()=> {
      await $(await AnyoneUsuallyLiveAtPage.yes()).click();
      await $(await AnyoneUsuallyLiveAtPage.submit()).click();
      await $(await AnyoneElseLiveAtListCollectorAddPage.firstName()).setValue("Marcus");
      await $(await AnyoneElseLiveAtListCollectorAddPage.lastName()).setValue("Twin");
      await $(await AnyoneElseLiveAtListCollectorAddPage.submit()).click();
      await $(await AnyoneElseLiveAtListCollectorPage.no()).click();
      await $(await AnyoneElseLiveAtListCollectorPage.submit()).click();
      await $(await SectionSummaryPage.peopleListRemoveLink(1)).click();
      await $(await AnyoneElseLiveAtListCollectorRemovePage.yes()).click();
      await $(await AnyoneElseLiveAtListCollectorRemovePage.submit()).click();
      await $(await SectionSummaryPage.peopleListAddLink()).click();
      await expect(browser.getUrl()).to.contain(AnyoneElseLiveAtListCollectorAddPage.pageName);
    });
  });
});
