import checkPeopleInList from "../helpers";
import HubPage from "../base_pages/hub.page.js";
import AnyoneUsuallyLiveAtPage from "../generated_pages/list_collector_driving_question/anyone-usually-live-at.page.js";
import AnyoneElseLiveAtListCollectorPage from "../generated_pages/list_collector_driving_question/anyone-else-live-at.page.js";
import AnyoneElseLiveAtListCollectorAddPage from "../generated_pages/list_collector_driving_question/anyone-else-live-at-add.page.js";
import AnyoneElseLiveAtListCollectorRemovePage from "../generated_pages/list_collector_driving_question/anyone-else-live-at-remove.page.js";
import SectionSummaryPage from "../generated_pages/list_collector_driving_question/section-summary.page.js";

describe("List Collector Driving Question", () => {
  beforeEach("Load the survey", () => {
    browser.openQuestionnaire("test_list_collector_driving_question.json");
    $(HubPage.submit()).click();
  });

  describe("Given a happy journey through the list collector", () => {
    it("The collector shows all of the household members in the summary", () => {
      $(AnyoneUsuallyLiveAtPage.yes()).click();
      $(AnyoneUsuallyLiveAtPage.submit()).click();
      $(AnyoneElseLiveAtListCollectorAddPage.firstName()).setValue("Marcus");
      $(AnyoneElseLiveAtListCollectorAddPage.lastName()).setValue("Twin");
      $(AnyoneElseLiveAtListCollectorAddPage.submit()).click();
      $(AnyoneElseLiveAtListCollectorPage.yes()).click();
      $(AnyoneElseLiveAtListCollectorPage.submit()).click();
      $(AnyoneElseLiveAtListCollectorAddPage.firstName()).setValue("Suzy");
      $(AnyoneElseLiveAtListCollectorAddPage.lastName()).setValue("Clemens");
      $(AnyoneElseLiveAtListCollectorAddPage.submit()).click();
      $(AnyoneElseLiveAtListCollectorPage.no()).click();
      $(AnyoneElseLiveAtListCollectorPage.submit()).click();

      const peopleExpected = ["Marcus Twin", "Suzy Clemens"];

      checkPeopleInList(peopleExpected, SectionSummaryPage.peopleListLabel);
    });
  });

  describe("Given the user answers no to the driving question", () => {
    it("The summary add link returns to the driving question", () => {
      $(AnyoneUsuallyLiveAtPage.no()).click();
      $(AnyoneUsuallyLiveAtPage.submit()).click();
      $(SectionSummaryPage.peopleListAddLink()).click();
      expect(browser.getUrl()).to.contain(AnyoneUsuallyLiveAtPage.url());
    });
  });

  describe("Given the user answers yes to the driving question, adds someone and later removes them", () => {
    it("The summary add link should return to the original list collector", () => {
      $(AnyoneUsuallyLiveAtPage.yes()).click();
      $(AnyoneUsuallyLiveAtPage.submit()).click();
      $(AnyoneElseLiveAtListCollectorAddPage.firstName()).setValue("Marcus");
      $(AnyoneElseLiveAtListCollectorAddPage.lastName()).setValue("Twin");
      $(AnyoneElseLiveAtListCollectorAddPage.submit()).click();
      $(AnyoneElseLiveAtListCollectorPage.no()).click();
      $(AnyoneElseLiveAtListCollectorPage.submit()).click();
      $(SectionSummaryPage.peopleListRemoveLink(1)).click();
      $(AnyoneElseLiveAtListCollectorRemovePage.yes()).click();
      $(AnyoneElseLiveAtListCollectorRemovePage.submit()).click();
      $(SectionSummaryPage.peopleListAddLink()).click();
      expect(browser.getUrl()).to.contain(AnyoneElseLiveAtListCollectorAddPage.pageName);
    });
  });
});
