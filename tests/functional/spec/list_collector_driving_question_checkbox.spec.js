const checkPeopleInList = require('../helpers');
const HubPage = require('../base_pages/hub.page.js');

const PrimaryPersonListCollectorPage = require('../generated_pages/list_collector_driving_checkbox/primary-person-list-collector.page.js');
const PrimaryPersonListCollectorAddPage = require('../generated_pages/list_collector_driving_checkbox/primary-person-list-collector-add.page.js');
const AnyoneUsuallyLiveAtPage = require('../generated_pages/list_collector_driving_checkbox/anyone-usually-live-at.page.js');
const ListCollectorAddPage = require('../generated_pages/list_collector_driving_checkbox/list-collector-add.page.js');
const ListCollectorPage = require('../generated_pages/list_collector_driving_checkbox/list-collector.page.js');
const ListCollectorTemporaryAwayPage = require('../generated_pages/list_collector_driving_checkbox/list-collector-temporary-away-stay.page');
const ListCollectorTemporaryAwayAddPage = require('../generated_pages/list_collector_driving_checkbox/list-collector-temporary-away-stay-add.page');

const ListCollectorSummary = require('../base_pages/list-collector-summary.page.js');
const SectionSummaryPage = require('../base_pages/section-summary.page.js');

const beforeSetup = () => {
  browser.openQuestionnaire('test_list_collector_driving_checkbox.json');
  $(HubPage.submit()).click();
};

describe('List Collector Driving Checkbox Question', function() {
  before('Load the survey', beforeSetup);

  describe('Given a happy journey through the list collectors', function() {
    it('All of the household members and visitors are shown in the summary', function() {
      $(PrimaryPersonListCollectorPage.yesIUsuallyLiveHere()).click();
      $(PrimaryPersonListCollectorPage.submit()).click();
      $(PrimaryPersonListCollectorAddPage.firstName()).setValue('Marcus');
      $(PrimaryPersonListCollectorAddPage.lastName()).setValue('Twin');
      $(PrimaryPersonListCollectorAddPage.submit()).click();
      $(AnyoneUsuallyLiveAtPage.familyMembersAndPartners()).click();
      $(AnyoneUsuallyLiveAtPage.submit()).click();
      $(ListCollectorAddPage.firstName()).setValue('Suzy');
      $(ListCollectorAddPage.lastName()).setValue('Clemens');
      $(ListCollectorAddPage.submit()).click();
      $(ListCollectorPage.noIDoNotNeedToAddAPerson()).click();
      $(ListCollectorPage.submit()).click();
      $(ListCollectorTemporaryAwayPage.noThereAreNumberOfPeoplePeopleLivingHere()).click();
      $(ListCollectorTemporaryAwayPage.submit()).click();

      const householdMembersExpected = ['Marcus Twin (You)', 'Suzy Clemens'];
      checkPeopleInList(householdMembersExpected, ListCollectorSummary.peopleListLabel);
    });
  });

  describe('Given the primary person is removed', function() {
    it('Then they aren\'t shown on the summary screen', function() {
      $(SectionSummaryPage.previous()).click();
      $(ListCollectorTemporaryAwayPage.previous()).click();
      $(ListCollectorPage.previous()).click();
      $(AnyoneUsuallyLiveAtPage.previous()).click();
      $(PrimaryPersonListCollectorPage.noIDonTUsuallyLiveHere()).click();
      $(PrimaryPersonListCollectorPage.submit()).click();
      $(AnyoneUsuallyLiveAtPage.submit()).click();
      $(ListCollectorPage.submit()).click();
      $(ListCollectorTemporaryAwayPage.submit()).click();

      const householdMembersExpected = ['Suzy Clemens'];
      checkPeopleInList(householdMembersExpected, ListCollectorSummary.peopleListLabel);
    });
  });

  describe('Given the user chooses yes from the second list collector', function() {
    it('Then they are taken to the correct list add screen', function() {
      $(SectionSummaryPage.previous()).click();
      $(ListCollectorTemporaryAwayPage.yesINeedToAddSomeone()).click();
      $(ListCollectorTemporaryAwayPage.submit()).click();
      $(ListCollectorTemporaryAwayAddPage.firstName()).setValue('Christopher');
      $(ListCollectorTemporaryAwayAddPage.lastName()).setValue('Pike');
      $(ListCollectorTemporaryAwayAddPage.submit()).click();
      $(ListCollectorTemporaryAwayPage.noThereAreNumberOfPeoplePeopleLivingHere()).click();
      $(ListCollectorTemporaryAwayPage.submit()).click();

      const householdMembersExpected = ['Suzy Clemens', 'Christopher Pike'];
      checkPeopleInList(householdMembersExpected, ListCollectorSummary.peopleListLabel);
    });
  });
});

describe('Given the user says no one else lives in the house', function() {
  before('Load the survey', beforeSetup);

  it('The user is asked if they need to add anyone that is temporarily away', function() {
    $(PrimaryPersonListCollectorPage.yesIUsuallyLiveHere()).click();
    $(PrimaryPersonListCollectorPage.submit()).click();
    $(PrimaryPersonListCollectorAddPage.firstName()).setValue('Marcus');
    $(PrimaryPersonListCollectorAddPage.lastName()).setValue('Twin');
    $(PrimaryPersonListCollectorAddPage.submit()).click();
    $(AnyoneUsuallyLiveAtPage.exclusiveNoneOfTheseApplyNoOneUsuallyLivesHere()).click();
    $(AnyoneUsuallyLiveAtPage.submit()).click();

    expect($(ListCollectorTemporaryAwayPage.questionText()).getText()).to.equal('You said 1 person lives at 12 Lovely Villas. Do you need to add anyone?');
  });
});

describe('Given a person does not live in the house', function() {
  before('Load the survey', beforeSetup);
  it('The user is asked whether they live there', function() {
    $(PrimaryPersonListCollectorPage.noIDonTUsuallyLiveHere()).click();
    $(PrimaryPersonListCollectorPage.submit()).click();
    expect($(AnyoneUsuallyLiveAtPage.questionText()).getText()).to.equal('Do any of the following usually live at 12 Lovely Villas on 21 March?');

    $(AnyoneUsuallyLiveAtPage.exclusiveNoneOfTheseApplyNoOneUsuallyLivesHere()).click();
    $(AnyoneUsuallyLiveAtPage.submit()).click();
    expect($(ListCollectorTemporaryAwayPage.questionText()).getText()).to.equal('You said 0 people lives at 12 Lovely Villas. Do you need to add anyone?');

    $(ListCollectorTemporaryAwayPage.noThereAreNumberOfPeoplePeopleLivingHere()).click();
    $(AnyoneUsuallyLiveAtPage.submit()).click();
  });
});
