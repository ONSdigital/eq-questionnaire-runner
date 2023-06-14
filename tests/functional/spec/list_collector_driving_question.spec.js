import { checkItemsInList } from "../helpers";
import HubPage from "../base_pages/hub.page.js";
import AnyoneUsuallyLiveAtPage from "../generated_pages/list_collector_driving_question/anyone-usually-live-at.page.js";
import AnyoneElseLiveAtListCollectorPage from "../generated_pages/list_collector_driving_question/anyone-else-live-at.page.js";
import AnyoneElseLiveAtListCollectorAddPage from "../generated_pages/list_collector_driving_question/anyone-else-live-at-add.page.js";
import AnyoneElseLiveAtListCollectorRemovePage from "../generated_pages/list_collector_driving_question/anyone-else-live-at-remove.page.js";
import SectionSummaryPage from "../generated_pages/list_collector_driving_question/section-summary.page.js";

describe("List Collector Driving Question", () => {
  beforeEach("Load the survey", async () => {
    await browser.openQuestionnaire("test_list_collector_driving_question.json");
    await $(HubPage.submit()).click();
  });

  describe("Given a happy journey through the list collector", () => {
    it("The collector shows all of the household members in the summary", async () => {
      await $(AnyoneUsuallyLiveAtPage.yes()).click();
      await $(AnyoneUsuallyLiveAtPage.submit()).click();
      await $(AnyoneElseLiveAtListCollectorAddPage.firstName()).setValue("Marcus");
      await $(AnyoneElseLiveAtListCollectorAddPage.lastName()).setValue("Twin");
      await $(AnyoneElseLiveAtListCollectorAddPage.submit()).click();
      await $(AnyoneElseLiveAtListCollectorPage.yes()).click();
      await $(AnyoneElseLiveAtListCollectorPage.submit()).click();
      await $(AnyoneElseLiveAtListCollectorAddPage.firstName()).setValue("Suzy");
      await $(AnyoneElseLiveAtListCollectorAddPage.lastName()).setValue("Clemens");
      await $(AnyoneElseLiveAtListCollectorAddPage.submit()).click();
      await $(AnyoneElseLiveAtListCollectorPage.no()).click();
      await $(AnyoneElseLiveAtListCollectorPage.submit()).click();

      const peopleExpected = ["Marcus Twin", "Suzy Clemens"];

      await checkItemsInList(peopleExpected, SectionSummaryPage.peopleListLabel);
    });
  });

  describe("Given the user answers no to the driving question", () => {
    it("The summary add link returns to the driving question", async () => {
      await $(AnyoneUsuallyLiveAtPage.no()).click();
      await $(AnyoneUsuallyLiveAtPage.submit()).click();
      await $(SectionSummaryPage.peopleListAddLink()).click();
      await expect(await browser.getUrl()).to.contain(AnyoneUsuallyLiveAtPage.url());
    });
  });

  describe("Given the user answers yes to the driving question, adds someone and later removes them", () => {
    it("The summary add link should return to the original list collector", async () => {
      await $(AnyoneUsuallyLiveAtPage.yes()).click();
      await $(AnyoneUsuallyLiveAtPage.submit()).click();
      await $(AnyoneElseLiveAtListCollectorAddPage.firstName()).setValue("Marcus");
      await $(AnyoneElseLiveAtListCollectorAddPage.lastName()).setValue("Twin");
      await $(AnyoneElseLiveAtListCollectorAddPage.submit()).click();
      await $(AnyoneElseLiveAtListCollectorPage.no()).click();
      await $(AnyoneElseLiveAtListCollectorPage.submit()).click();
      await $(SectionSummaryPage.peopleListRemoveLink(1)).click();
      await $(AnyoneElseLiveAtListCollectorRemovePage.yes()).click();
      await $(AnyoneElseLiveAtListCollectorRemovePage.submit()).click();
      await $(SectionSummaryPage.peopleListAddLink()).click();
      await expect(await browser.getUrl()).to.contain(AnyoneElseLiveAtListCollectorAddPage.pageName);
    });
  });
});
