import checkPeopleInList from "../helpers";
import HubPage from "../base_pages/hub.page.js";
import PrimaryPersonListCollectorPage from "../generated_pages/list_collector_driving_checkbox/primary-person-list-collector.page.js";
import PrimaryPersonListCollectorAddPage from "../generated_pages/list_collector_driving_checkbox/primary-person-list-collector-add.page.js";
import AnyoneUsuallyLiveAtPage from "../generated_pages/list_collector_driving_checkbox/anyone-usually-live-at.page.js";
import ListCollectorAddPage from "../generated_pages/list_collector_driving_checkbox/list-collector-add.page.js";
import ListCollectorPage from "../generated_pages/list_collector_driving_checkbox/list-collector.page.js";
import ListCollectorTemporaryAwayPage from "../generated_pages/list_collector_driving_checkbox/list-collector-temporary-away-stay.page";
import ListCollectorTemporaryAwayAddPage from "../generated_pages/list_collector_driving_checkbox/list-collector-temporary-away-stay-add.page";
import SummaryPage from "../generated_pages/list_collector_driving_checkbox/section-summary.page";

const beforeSetup = () => {
  browser.openQuestionnaire("test_list_collector_driving_checkbox.json");
  $(HubPage.submit()).click();
};

describe("List Collector Driving Checkbox Question", () => {
  before("Load the survey", beforeSetup);

  describe("Given a happy journey through the list collectors", () => {
    it("All of the household members and visitors are shown in the summary", () => {
      $(PrimaryPersonListCollectorPage.yesIUsuallyLiveHere()).click();
      $(PrimaryPersonListCollectorPage.submit()).click();
      $(PrimaryPersonListCollectorAddPage.firstName()).setValue("Marcus");
      $(PrimaryPersonListCollectorAddPage.lastName()).setValue("Twin");
      $(PrimaryPersonListCollectorAddPage.submit()).click();
      $(AnyoneUsuallyLiveAtPage.familyMembersAndPartners()).click();
      $(AnyoneUsuallyLiveAtPage.submit()).click();
      $(ListCollectorAddPage.firstName()).setValue("Suzy");
      $(ListCollectorAddPage.lastName()).setValue("Clemens");
      $(ListCollectorAddPage.submit()).click();
      $(ListCollectorPage.noIDoNotNeedToAddAPerson()).click();
      $(ListCollectorPage.submit()).click();
      $(ListCollectorTemporaryAwayPage.noThereAreNumberOfPeoplePeopleLivingHere()).click();
      $(ListCollectorTemporaryAwayPage.submit()).click();

      const householdMembersExpected = ["Marcus Twin (You)", "Suzy Clemens"];
      checkPeopleInList(householdMembersExpected, SummaryPage.peopleListLabel);
    });
  });

  describe("Given the primary person is removed", () => {
    it("Then they aren't shown on the summary screen", () => {
      $(SummaryPage.previous()).click();
      $(ListCollectorTemporaryAwayPage.previous()).click();
      $(ListCollectorPage.previous()).click();
      $(AnyoneUsuallyLiveAtPage.previous()).click();
      $(PrimaryPersonListCollectorPage.noIDonTUsuallyLiveHere()).click();
      $(PrimaryPersonListCollectorPage.submit()).click();
      $(AnyoneUsuallyLiveAtPage.submit()).click();
      $(ListCollectorPage.submit()).click();
      $(ListCollectorTemporaryAwayPage.submit()).click();

      const householdMembersExpected = ["Suzy Clemens"];
      checkPeopleInList(householdMembersExpected, SummaryPage.peopleListLabel);
    });
  });

  describe("Given the user chooses yes from the second list collector", () => {
    it("Then they are taken to the correct list add screen", () => {
      $(SummaryPage.previous()).click();
      $(ListCollectorTemporaryAwayPage.yesINeedToAddSomeone()).click();
      $(ListCollectorTemporaryAwayPage.submit()).click();
      $(ListCollectorTemporaryAwayAddPage.firstName()).setValue("Christopher");
      $(ListCollectorTemporaryAwayAddPage.lastName()).setValue("Pike");
      $(ListCollectorTemporaryAwayAddPage.submit()).click();
      $(ListCollectorTemporaryAwayPage.noThereAreNumberOfPeoplePeopleLivingHere()).click();
      $(ListCollectorTemporaryAwayPage.submit()).click();

      const householdMembersExpected = ["Suzy Clemens", "Christopher Pike"];
      checkPeopleInList(householdMembersExpected, SummaryPage.peopleListLabel);
    });
  });
});

describe("Given the user says no one else lives in the house", () => {
  before("Load the survey", beforeSetup);

  it("The user is asked if they need to add anyone that is temporarily away", () => {
    $(PrimaryPersonListCollectorPage.yesIUsuallyLiveHere()).click();
    $(PrimaryPersonListCollectorPage.submit()).click();
    $(PrimaryPersonListCollectorAddPage.firstName()).setValue("Marcus");
    $(PrimaryPersonListCollectorAddPage.lastName()).setValue("Twin");
    $(PrimaryPersonListCollectorAddPage.submit()).click();
    $(AnyoneUsuallyLiveAtPage.exclusiveNoneOfTheseApplyNoOneUsuallyLivesHere()).click();
    $(AnyoneUsuallyLiveAtPage.submit()).click();

    expect($(ListCollectorTemporaryAwayPage.questionText()).getText()).to.equal("You said 1 person lives at 12 Lovely Villas. Do you need to add anyone?");
  });
});

describe("Given a person does not live in the house", () => {
  before("Load the survey", beforeSetup);
  it("The user is asked whether they live there", () => {
    $(PrimaryPersonListCollectorPage.noIDonTUsuallyLiveHere()).click();
    $(PrimaryPersonListCollectorPage.submit()).click();
    expect($(AnyoneUsuallyLiveAtPage.questionText()).getText()).to.equal("Do any of the following usually live at 12 Lovely Villas on 21 March?");

    $(AnyoneUsuallyLiveAtPage.exclusiveNoneOfTheseApplyNoOneUsuallyLivesHere()).click();
    $(AnyoneUsuallyLiveAtPage.submit()).click();
    expect($(ListCollectorTemporaryAwayPage.questionText()).getText()).to.equal("You said 0 people lives at 12 Lovely Villas. Do you need to add anyone?");

    $(ListCollectorTemporaryAwayPage.noThereAreNumberOfPeoplePeopleLivingHere()).click();
    $(AnyoneUsuallyLiveAtPage.submit()).click();
  });
});
