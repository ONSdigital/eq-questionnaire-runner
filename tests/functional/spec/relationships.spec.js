const ListCollectorPage = require('../generated_pages/relationships/list-collector.page.js');
const ListCollectorAddPage = require('../generated_pages/relationships/list-collector-add.page.js');
const ListCollectorRemovePage = require('../generated_pages/relationships/list-collector-remove.page.js');
const RelationshipsPage = require('../generated_pages/relationships/relationships.page.js');
const RelationshipsInterstitialPage = require('../generated_pages/relationships/relationship-interstitial.page');

const ListCollectorSummary = require('../base_pages/list-collector-summary.page.js');
const SectionSummaryPage = require('../base_pages/section-summary.page.js');

describe('Relationships', function() {
  const schema = 'test_relationships.json';

  describe('Given I am completing the test_relationships survey,', function() {
    beforeEach('load the survey', function() {
      browser.openQuestionnaire(schema);
    });


    it('When I have one household member, Then I will be not be asked about relationships', function() {
      $(ListCollectorPage.yes()).click();
      $(ListCollectorPage.submit()).click();
      $(ListCollectorAddPage.firstName()).setValue('Marcus');
      $(ListCollectorAddPage.lastName()).setValue('Twin');
      $(ListCollectorAddPage.submit()).click();
      $(ListCollectorPage.no()).click();
      $(ListCollectorPage.submit()).click();
      expect(browser.getUrl()).to.contain('/sections/section/');
    });

    it('When I add two household members, Then I will be asked about one relationship', function() {
      $(ListCollectorPage.yes()).click();
      $(ListCollectorPage.submit()).click();
      $(ListCollectorAddPage.firstName()).setValue('Marcus');
      $(ListCollectorAddPage.lastName()).setValue('Twin');
      $(ListCollectorAddPage.submit()).click();
      $(ListCollectorPage.yes()).click();
      $(ListCollectorPage.submit()).click();
      $(ListCollectorAddPage.firstName()).setValue('Samuel');
      $(ListCollectorAddPage.lastName()).setValue('Clemens');
      $(ListCollectorAddPage.submit()).click();
      $(ListCollectorPage.no()).click();
      $(ListCollectorPage.submit()).click();
      expect(browser.getUrl()).to.contain(RelationshipsPage.pageName);
      $(RelationshipsPage.husbandOrWife()).click();
      $(RelationshipsPage.submit()).click();
      $(RelationshipsInterstitialPage.submit()).click();
      expect(browser.getUrl()).to.contain('/sections/section/');
    });

    describe('When I add three household members,', function() {
      beforeEach('add three people', function() {
        addThreePeople();
      });

      it('Then I will be asked about all relationships', function() {
        $(ListCollectorPage.no()).click();
        $(ListCollectorPage.submit()).click();
        $(RelationshipsPage.husbandOrWife()).click();
        $(RelationshipsPage.submit()).click();
        $(RelationshipsPage.legallyRegisteredCivilPartner()).click();
        $(RelationshipsPage.submit()).click();
        $(RelationshipsPage.husbandOrWife()).click();
        $(RelationshipsPage.submit()).click();
        $(RelationshipsInterstitialPage.submit()).click();
        expect(browser.getUrl()).to.contain('/sections/section/');
      });

      it('And go to the first relationship, Then the previous link should return to the list collector', function() {
        $(ListCollectorPage.no()).click();
        $(ListCollectorPage.submit()).click();
        $(RelationshipsPage.previous()).click();
        expect(browser.getUrl()).to.contain('/questionnaire/list-collector/');
      });

      it('And go to the first relationship, Then the \'Brother or Sister\' option should have the text \'Including half brother or half sister\'', function() {
        $(ListCollectorPage.no()).click();
        $(ListCollectorPage.submit()).click();
        expect($(RelationshipsPage.brotherOrSisterLabel()).getText()).to.contain('Including half brother or half sister');
      });

      it('And go to the second relationship, Then the previous link should return to the first relationship', function() {
        $(ListCollectorPage.no()).click();
        $(ListCollectorPage.submit()).click();
        $(RelationshipsPage.husbandOrWife()).click();
        $(RelationshipsPage.submit()).click();
        $(RelationshipsPage.previous()).click();
        $(RelationshipsInterstitialPage.submit()).click();
        expect(browser.getUrl()).to.contain(RelationshipsPage.pageName);
        expect($(RelationshipsPage.questionText()).getText()).to.contain('Marcus');
      });

      it('And go to the section summary, Then the previous link should return to the last relationship Interstitial', function() {
        $(ListCollectorPage.no()).click();
        $(ListCollectorPage.submit()).click();
        $(RelationshipsPage.husbandOrWife()).click();
        $(RelationshipsPage.submit()).click();
        $(RelationshipsPage.legallyRegisteredCivilPartner()).click();
        $(RelationshipsPage.submit()).click();
        $(RelationshipsPage.husbandOrWife()).click();
        $(RelationshipsPage.submit()).click();
        $(RelationshipsInterstitialPage.submit()).click();
        expect(browser.getUrl()).to.contain('/sections/section/');
        $(SectionSummaryPage.previous()).click();
        $(RelationshipsInterstitialPage.previous()).click();
        expect(browser.getUrl()).to.contain(RelationshipsPage.pageName);
        expect($(RelationshipsPage.questionText()).getText()).to.contain('Olivia');
      });

      it('When I add all relationships and return to the relationships, Then the relationships should be populated', function() {
        $(ListCollectorPage.no()).click();
        $(ListCollectorPage.submit()).click();
        $(RelationshipsPage.husbandOrWife()).click();
        $(RelationshipsPage.submit()).click();
        $(RelationshipsPage.legallyRegisteredCivilPartner()).click();
        $(RelationshipsPage.submit()).click();
        $(RelationshipsPage.husbandOrWife()).click();
        $(RelationshipsPage.submit()).click();
        $(RelationshipsInterstitialPage.submit()).click();
        expect(browser.getUrl()).to.contain('/sections/section/');
        $(SectionSummaryPage.previous()).click();
        $(RelationshipsInterstitialPage.previous()).click();
        expect($(RelationshipsPage.husbandOrWife()).isSelected()).to.be.true;
        $(RelationshipsPage.previous()).click();
        expect($(RelationshipsPage.legallyRegisteredCivilPartner()).isSelected()).to.be.true;
      });

      it('And go to the first relationship, Then the person\'s name should be in the question title and playback text', function() {
        $(ListCollectorPage.no()).click();
        $(ListCollectorPage.submit()).click();
        expect($(ListCollectorPage.questionText()).getText()).to.contain('Marcus Twin');
        expect($(RelationshipsPage.playback()).getText()).to.contain('Marcus Twin');
      });

      it('And go to the first relationship and submit without selecting an option, Then an error should be displayed', function() {
        $(ListCollectorPage.no()).click();
        $(ListCollectorPage.submit()).click();
        $(RelationshipsPage.submit()).click();
        expect($(RelationshipsPage.error()).isDisplayed()).to.be.true;
      });

      it('And go to a non existent relationship, Then I should be redirected to the first relationship', function() {
        $(ListCollectorPage.no()).click();
        $(ListCollectorPage.submit()).click();
        browser.url('/questionnaire/relationships/fake-id/to/another-fake-id');
        expect(browser.getUrl()).to.contain(RelationshipsPage.pageName);
        expect($(RelationshipsPage.playback()).getText()).to.contain('Marcus Twin');
      });

      it('And go to the first relationship and click \'Save and sign out\', Then I should be signed out', function() {
        $(ListCollectorPage.no()).click();
        $(ListCollectorPage.submit()).click();
        $(RelationshipsPage.husbandOrWife()).click();
        $(RelationshipsPage.saveSignOut()).click();
        expect(browser.getUrl()).to.not.contain('questionnaire');
      });

      it('And go to the first relationship, select a relationship and click \'Save and sign out\', Then I should be signed out', function() {
        $(ListCollectorPage.no()).click();
        $(ListCollectorPage.submit()).click();
        $(RelationshipsPage.saveSignOut()).click();
        expect(browser.getUrl()).to.not.contain('questionnaire');
      });
    });

    describe('When I have added one or more household members after answering the relationships question,', function() {
      beforeEach('add three people and complete their relationships', function() {
        addThreePeopleAndCompleteRelationships();
      });

      it('Then I delete one of the original household members I will not be asked for the original members relationships again', function() {
        $(ListCollectorSummary.listCollectorPeopleRowRemove(1)).click();
        $(ListCollectorRemovePage.yes()).click();
        $(ListCollectorRemovePage.submit()).click();
        expect(browser.getUrl()).to.contain('/sections/section/');
      });

      it('Then I add another household member I will be asked for about all relationships', function() {
        $(ListCollectorSummary.listCollectorPeopleRowAdd()).click();
        $(ListCollectorAddPage.firstName()).setValue('Tom');
        $(ListCollectorAddPage.lastName()).setValue('Bowden');
        $(ListCollectorAddPage.submit()).click();
        expect($(RelationshipsPage.husbandOrWife()).isSelected()).to.be.true;
        $(RelationshipsPage.submit()).click();
        expect($(RelationshipsPage.legallyRegisteredCivilPartner()).isSelected()).to.be.true;
        $(RelationshipsPage.submit()).click();
        expect($(RelationshipsPage.playback()).getText()).to.contain('Tom Bowden is Marcus Twin’s …');
        $(RelationshipsPage.sonOrDaughter()).click();
        $(RelationshipsPage.submit()).click();
        expect($(RelationshipsPage.husbandOrWife()).isSelected()).to.be.true;
        $(RelationshipsPage.submit()).click();
        expect($(RelationshipsPage.playback()).getText()).to.contain('Tom Bowden is Samuel Clemens’ …');
        $(RelationshipsPage.sonOrDaughter()).click();
        $(RelationshipsPage.submit()).click();
        browser.pause(20000);
        expect($(RelationshipsPage.playback()).getText()).to.contain('Tom Bowden is Olivia Clemens’ …');
      });
    });

    function addThreePeopleAndCompleteRelationships() {
      addThreePeople();

      $(ListCollectorPage.no()).click();
      $(ListCollectorPage.submit()).click();
      $(RelationshipsPage.husbandOrWife()).click();
      $(RelationshipsPage.submit()).click();
      $(RelationshipsPage.legallyRegisteredCivilPartner()).click();
      $(RelationshipsPage.submit()).click();
      $(RelationshipsPage.husbandOrWife()).click();
      $(RelationshipsPage.submit()).click();
      $(RelationshipsInterstitialPage.submit()).click();
    }

    function addThreePeople() {
      $(ListCollectorPage.yes()).click();
      $(ListCollectorPage.submit()).click();
      $(ListCollectorAddPage.firstName()).setValue('Marcus');
      $(ListCollectorAddPage.lastName()).setValue('Twin');
      $(ListCollectorAddPage.submit()).click();
      $(ListCollectorPage.yes()).click();
      $(ListCollectorPage.submit()).click();
      $(ListCollectorAddPage.firstName()).setValue('Samuel');
      $(ListCollectorAddPage.lastName()).setValue('Clemens');
      $(ListCollectorAddPage.submit()).click();
      $(ListCollectorPage.yes()).click();
      $(ListCollectorPage.submit()).click();
      $(ListCollectorAddPage.firstName()).setValue('Olivia');
      $(ListCollectorAddPage.lastName()).setValue('Clemens');
      $(ListCollectorAddPage.submit()).click();
    }

  });
});
