import { checkItemsInList, click, verifyUrlContains } from "../../helpers";
import HubPage from "../../base_pages/hub.page.js";
import AnyoneUsuallyLiveAtPage from "../../generated_pages/list_collector_driving_question/anyone-usually-live-at.page.js";
import AnyoneElseLiveAtListCollectorPage from "../../generated_pages/list_collector_driving_question/anyone-else-live-at.page.js";
import AnyoneElseLiveAtListCollectorAddPage from "../../generated_pages/list_collector_driving_question/anyone-else-live-at-add.page.js";
import AnyoneElseLiveAtListCollectorRemovePage from "../../generated_pages/list_collector_driving_question/anyone-else-live-at-remove.page.js";
import SectionSummaryPage from "../../generated_pages/list_collector_driving_question/section-summary.page.js";

describe("List Collector Driving Question", () => {
  beforeEach("Load the survey", async () => {
    await browser.openQuestionnaire("test_list_collector_driving_question.json");
    await click(HubPage.submit());
  });

  describe("Given a happy journey through the list collector", () => {
    it("The collector shows all of the household members in the summary", async () => {
      await $(AnyoneUsuallyLiveAtPage.yes()).click();
      await click(AnyoneUsuallyLiveAtPage.submit());
      await $(AnyoneElseLiveAtListCollectorAddPage.firstName()).setValue("Marcus");
      await $(AnyoneElseLiveAtListCollectorAddPage.lastName()).setValue("Twin");
      await click(AnyoneElseLiveAtListCollectorAddPage.submit());
      await $(AnyoneElseLiveAtListCollectorPage.yes()).click();
      await click(AnyoneElseLiveAtListCollectorPage.submit());
      await $(AnyoneElseLiveAtListCollectorAddPage.firstName()).setValue("Suzy");
      await $(AnyoneElseLiveAtListCollectorAddPage.lastName()).setValue("Clemens");
      await click(AnyoneElseLiveAtListCollectorAddPage.submit());
      await $(AnyoneElseLiveAtListCollectorPage.no()).click();
      await click(AnyoneElseLiveAtListCollectorPage.submit());

      const peopleExpected = ["Marcus Twin", "Suzy Clemens"];

      await checkItemsInList(peopleExpected, SectionSummaryPage.peopleListLabel);
    });
  });

  describe("Given the user answers no to the driving question", () => {
    it("The summary add link returns to the driving question", async () => {
      await $(AnyoneUsuallyLiveAtPage.no()).click();
      await click(AnyoneUsuallyLiveAtPage.submit());
      await $(SectionSummaryPage.peopleListAddLink()).click();
      await verifyUrlContains(AnyoneUsuallyLiveAtPage.url());
    });
  });

  describe("Given the user answers yes to the driving question, adds someone and later removes them", () => {
    it("The summary add link should return to the original list collector", async () => {
      await $(AnyoneUsuallyLiveAtPage.yes()).click();
      await click(AnyoneUsuallyLiveAtPage.submit());
      await $(AnyoneElseLiveAtListCollectorAddPage.firstName()).setValue("Marcus");
      await $(AnyoneElseLiveAtListCollectorAddPage.lastName()).setValue("Twin");
      await click(AnyoneElseLiveAtListCollectorAddPage.submit());
      await $(AnyoneElseLiveAtListCollectorPage.no()).click();
      await click(AnyoneElseLiveAtListCollectorPage.submit());
      await $(SectionSummaryPage.peopleListRemoveLink(1)).click();
      await $(AnyoneElseLiveAtListCollectorRemovePage.yes()).click();
      await click(AnyoneElseLiveAtListCollectorRemovePage.submit());
      await $(SectionSummaryPage.peopleListAddLink()).click();
      await verifyUrlContains(AnyoneElseLiveAtListCollectorAddPage.pageName);
    });
  });
});
