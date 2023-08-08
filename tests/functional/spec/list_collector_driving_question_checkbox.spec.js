import { checkItemsInList } from "../helpers";
import HubPage from "../base_pages/hub.page.js";
import PrimaryPersonListCollectorPage from "../generated_pages/list_collector_driving_checkbox/primary-person-list-collector.page.js";
import PrimaryPersonListCollectorAddPage from "../generated_pages/list_collector_driving_checkbox/primary-person-list-collector-add.page.js";
import AnyoneUsuallyLiveAtPage from "../generated_pages/list_collector_driving_checkbox/anyone-usually-live-at.page.js";
import ListCollectorAddPage from "../generated_pages/list_collector_driving_checkbox/list-collector-add.page.js";
import ListCollectorPage from "../generated_pages/list_collector_driving_checkbox/list-collector.page.js";
import ListCollectorTemporaryAwayPage from "../generated_pages/list_collector_driving_checkbox/list-collector-temporary-away-stay.page";
import ListCollectorTemporaryAwayAddPage from "../generated_pages/list_collector_driving_checkbox/list-collector-temporary-away-stay-add.page";
import SummaryPage from "../generated_pages/list_collector_driving_checkbox/section-summary.page";

const beforeSetup = async () => {
  await browser.openQuestionnaire("test_list_collector_driving_checkbox.json");
  await $(HubPage.submit()).click();
};

describe("List Collector Driving Checkbox Question", () => {
  before("Load the survey", beforeSetup);

  describe("Given a happy journey through the list collectors", () => {
    it("All of the household members and visitors are shown in the summary", async () => {
      await $(PrimaryPersonListCollectorPage.yesIUsuallyLiveHere()).click();
      await $(PrimaryPersonListCollectorPage.submit()).click();
      await $(PrimaryPersonListCollectorAddPage.firstName()).setValue("Marcus");
      await $(PrimaryPersonListCollectorAddPage.lastName()).setValue("Twin");
      await $(PrimaryPersonListCollectorAddPage.submit()).click();
      await $(AnyoneUsuallyLiveAtPage.familyMembersAndPartners()).click();
      await $(AnyoneUsuallyLiveAtPage.submit()).click();
      await $(ListCollectorAddPage.firstName()).setValue("Suzy");
      await $(ListCollectorAddPage.lastName()).setValue("Clemens");
      await $(ListCollectorAddPage.submit()).click();
      await $(ListCollectorPage.noIDoNotNeedToAddAPerson()).click();
      await $(ListCollectorPage.submit()).click();
      await $(ListCollectorTemporaryAwayPage.noThereAreNumberOfPeoplePeopleLivingHere()).click();
      await $(ListCollectorTemporaryAwayPage.submit()).click();

      const householdMembersExpected = ["Marcus Twin (You)", "Suzy Clemens"];
      await checkItemsInList(householdMembersExpected, SummaryPage.peopleListLabel);
    });
  });

  describe("Given the primary person is removed", () => {
    it("Then they aren't shown on the summary screen", async () => {
      await $(SummaryPage.previous()).click();
      await $(ListCollectorTemporaryAwayPage.previous()).click();
      await $(ListCollectorPage.previous()).click();
      await $(AnyoneUsuallyLiveAtPage.previous()).click();
      await $(PrimaryPersonListCollectorPage.noIDonTUsuallyLiveHere()).click();
      await $(PrimaryPersonListCollectorPage.submit()).click();

      const householdMembersExpected = ["Suzy Clemens"];
      await checkItemsInList(householdMembersExpected, SummaryPage.peopleListLabel);
    });
  });

  describe("Given the user chooses yes from the second list collector", () => {
    it("Then they are taken to the correct list add screen", async () => {
      await $(SummaryPage.previous()).click();
      await $(ListCollectorTemporaryAwayPage.yesINeedToAddSomeone()).click();
      await $(ListCollectorTemporaryAwayPage.submit()).click();
      await $(ListCollectorTemporaryAwayAddPage.firstName()).setValue("Christopher");
      await $(ListCollectorTemporaryAwayAddPage.lastName()).setValue("Pike");
      await $(ListCollectorTemporaryAwayAddPage.submit()).click();
      await $(ListCollectorTemporaryAwayPage.noThereAreNumberOfPeoplePeopleLivingHere()).click();
      await $(ListCollectorTemporaryAwayPage.submit()).click();

      const householdMembersExpected = ["Suzy Clemens", "Christopher Pike"];
      await checkItemsInList(householdMembersExpected, SummaryPage.peopleListLabel);
    });
  });
});

describe("Given the user says no one else lives in the house", () => {
  before("Load the survey", beforeSetup);

  it("The user is asked if they need to add anyone that is temporarily away", async () => {
    await $(PrimaryPersonListCollectorPage.yesIUsuallyLiveHere()).click();
    await $(PrimaryPersonListCollectorPage.submit()).click();
    await $(PrimaryPersonListCollectorAddPage.firstName()).setValue("Marcus");
    await $(PrimaryPersonListCollectorAddPage.lastName()).setValue("Twin");
    await $(PrimaryPersonListCollectorAddPage.submit()).click();
    await $(AnyoneUsuallyLiveAtPage.exclusiveNoneOfTheseApplyNoOneUsuallyLivesHere()).click();
    await $(AnyoneUsuallyLiveAtPage.submit()).click();

    await expect(await $(ListCollectorTemporaryAwayPage.questionText()).getText()).to.equal(
      "You said 1 person lives at 12 Lovely Villas. Do you need to add anyone?",
    );
  });
});

describe("Given a person does not live in the house", () => {
  before("Load the survey", beforeSetup);
  it("The user is asked whether they live there", async () => {
    await $(PrimaryPersonListCollectorPage.noIDonTUsuallyLiveHere()).click();
    await $(PrimaryPersonListCollectorPage.submit()).click();
    await expect(await $(AnyoneUsuallyLiveAtPage.questionText()).getText()).to.equal("Do any of the following usually live at 12 Lovely Villas on 21 March?");

    await $(AnyoneUsuallyLiveAtPage.exclusiveNoneOfTheseApplyNoOneUsuallyLivesHere()).click();
    await $(AnyoneUsuallyLiveAtPage.submit()).click();
    await expect(await $(ListCollectorTemporaryAwayPage.questionText()).getText()).to.equal(
      "You said 0 people lives at 12 Lovely Villas. Do you need to add anyone?",
    );

    await $(ListCollectorTemporaryAwayPage.noThereAreNumberOfPeoplePeopleLivingHere()).click();
    await $(AnyoneUsuallyLiveAtPage.submit()).click();
  });
});
