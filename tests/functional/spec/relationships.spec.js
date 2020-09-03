import ListCollectorPage from "../generated_pages/relationships/list-collector.page.js";
import ListCollectorAddPage from "../generated_pages/relationships/list-collector-add.page.js";
import ListCollectorRemovePage from "../generated_pages/relationships/list-collector-remove.page.js";
import RelationshipsPage from "../generated_pages/relationships/relationships.page.js";
import RelationshipsInterstitialPage from "../generated_pages/relationships/relationship-interstitial.page.js";
import SectionSummaryPage from "../generated_pages/relationships/section-summary.page.js";

describe("Relationships", () => {
  const schema = "test_relationships.json";

  describe("Given I am completing the test_relationships survey,", () => {
    beforeEach("load the survey", () => {
      browser.openQuestionnaire(schema);
    });

    it("When I have one household member, Then I will be not be asked about relationships", () => {
      $(ListCollectorPage.yes()).click();
      $(ListCollectorPage.submit()).click();
      $(ListCollectorAddPage.firstName()).setValue("Marcus");
      $(ListCollectorAddPage.lastName()).setValue("Twin");
      $(ListCollectorAddPage.submit()).click();
      $(ListCollectorPage.no()).click();
      $(ListCollectorPage.submit()).click();
      expect(browser.getUrl()).to.contain("/sections/section/");
    });

    it("When I add two household members, Then I will be asked about one relationship", () => {
      $(ListCollectorPage.yes()).click();
      $(ListCollectorPage.submit()).click();
      $(ListCollectorAddPage.firstName()).setValue("Marcus");
      $(ListCollectorAddPage.lastName()).setValue("Twin");
      $(ListCollectorAddPage.submit()).click();
      $(ListCollectorPage.yes()).click();
      $(ListCollectorPage.submit()).click();
      $(ListCollectorAddPage.firstName()).setValue("Samuel");
      $(ListCollectorAddPage.lastName()).setValue("Clemens");
      $(ListCollectorAddPage.submit()).click();
      $(ListCollectorPage.no()).click();
      $(ListCollectorPage.submit()).click();
      expect(browser.getUrl()).to.contain(RelationshipsPage.pageName);
      $(RelationshipsPage.husbandOrWife()).click();
      $(RelationshipsPage.submit()).click();
      $(RelationshipsInterstitialPage.submit()).click();
      expect(browser.getUrl()).to.contain("/sections/section/");
    });

    describe("When I add three household members,", () => {
      beforeEach("add three people", () => {
        addThreePeople();
      });

      it("Then I will be asked about all relationships", () => {
        $(ListCollectorPage.no()).click();
        $(ListCollectorPage.submit()).click();
        $(RelationshipsPage.husbandOrWife()).click();
        $(RelationshipsPage.submit()).click();
        $(RelationshipsPage.legallyRegisteredCivilPartner()).click();
        $(RelationshipsPage.submit()).click();
        $(RelationshipsPage.husbandOrWife()).click();
        $(RelationshipsPage.submit()).click();
        $(RelationshipsInterstitialPage.submit()).click();
        expect(browser.getUrl()).to.contain("/sections/section/");
      });

      it("And go to the first relationship, Then the previous link should return to the list collector", () => {
        $(ListCollectorPage.no()).click();
        $(ListCollectorPage.submit()).click();
        $(RelationshipsPage.previous()).click();
        expect(browser.getUrl()).to.contain("/questionnaire/list-collector/");
      });

      it("And go to the first relationship, Then the 'Brother or Sister' option should have the text 'Including half brother or half sister'", () => {
        $(ListCollectorPage.no()).click();
        $(ListCollectorPage.submit()).click();
        expect($(RelationshipsPage.brotherOrSisterLabelDescription()).getText()).to.contain("Including half brother or half sister");
      });

      it("And go to the second relationship, Then the previous link should return to the first relationship", () => {
        $(ListCollectorPage.no()).click();
        $(ListCollectorPage.submit()).click();
        $(RelationshipsPage.husbandOrWife()).click();
        $(RelationshipsPage.submit()).click();
        $(RelationshipsPage.previous()).click();
        $(RelationshipsInterstitialPage.submit()).click();
        expect(browser.getUrl()).to.contain(RelationshipsPage.pageName);
        expect($(RelationshipsPage.questionText()).getText()).to.contain("Marcus");
      });

      it("And go to the section summary, Then the previous link should return to the last relationship Interstitial", () => {
        $(ListCollectorPage.no()).click();
        $(ListCollectorPage.submit()).click();
        $(RelationshipsPage.husbandOrWife()).click();
        $(RelationshipsPage.submit()).click();
        $(RelationshipsPage.legallyRegisteredCivilPartner()).click();
        $(RelationshipsPage.submit()).click();
        $(RelationshipsPage.husbandOrWife()).click();
        $(RelationshipsPage.submit()).click();
        $(RelationshipsInterstitialPage.submit()).click();
        expect(browser.getUrl()).to.contain("/sections/section/");
        $(SectionSummaryPage.previous()).click();
        $(RelationshipsInterstitialPage.previous()).click();
        expect(browser.getUrl()).to.contain(RelationshipsPage.pageName);
        expect($(RelationshipsPage.questionText()).getText()).to.contain("Olivia");
      });

      it("When I add all relationships and return to the relationships, Then the relationships should be populated", () => {
        $(ListCollectorPage.no()).click();
        $(ListCollectorPage.submit()).click();
        $(RelationshipsPage.husbandOrWife()).click();
        $(RelationshipsPage.submit()).click();
        $(RelationshipsPage.legallyRegisteredCivilPartner()).click();
        $(RelationshipsPage.submit()).click();
        $(RelationshipsPage.husbandOrWife()).click();
        $(RelationshipsPage.submit()).click();
        $(RelationshipsInterstitialPage.submit()).click();
        expect(browser.getUrl()).to.contain("/sections/section/");
        $(SectionSummaryPage.previous()).click();
        $(RelationshipsInterstitialPage.previous()).click();
        expect($(RelationshipsPage.husbandOrWife()).isSelected()).to.be.true;
        $(RelationshipsPage.previous()).click();
        expect($(RelationshipsPage.legallyRegisteredCivilPartner()).isSelected()).to.be.true;
      });

      it("And go to the first relationship, Then the person's name should be in the question title and playback text", () => {
        $(ListCollectorPage.no()).click();
        $(ListCollectorPage.submit()).click();
        expect($(ListCollectorPage.questionText()).getText()).to.contain("Marcus Twin");
        expect($(RelationshipsPage.playback()).getText()).to.contain("Marcus Twin");
      });

      it("And go to the first relationship and submit without selecting an option, Then an error should be displayed", () => {
        $(ListCollectorPage.no()).click();
        $(ListCollectorPage.submit()).click();
        $(RelationshipsPage.submit()).click();
        expect($(RelationshipsPage.error()).isDisplayed()).to.be.true;
      });

      it("And go to the first relationship and click 'Save and sign out', Then I should be signed out", () => {
        $(ListCollectorPage.no()).click();
        $(ListCollectorPage.submit()).click();
        $(RelationshipsPage.husbandOrWife()).click();
        $(RelationshipsPage.saveSignOut()).click();
        expect(browser.getUrl()).to.not.contain("questionnaire");
      });

      it("And go to the first relationship, select a relationship and click 'Save and sign out', Then I should be signed out", () => {
        $(ListCollectorPage.no()).click();
        $(ListCollectorPage.submit()).click();
        $(RelationshipsPage.saveSignOut()).click();
        expect(browser.getUrl()).to.not.contain("questionnaire");
      });
    });

    describe("When I have added one or more household members after answering the relationships question,", () => {
      beforeEach("add three people and complete their relationships", () => {
        addThreePeopleAndCompleteRelationships();
      });

      it("Then I delete one of the original household members I will not be asked for the original members relationships again", () => {
        $(SectionSummaryPage.peopleListRemoveLink(1)).click();
        $(ListCollectorRemovePage.yes()).click();
        $(ListCollectorRemovePage.submit()).click();
        expect(browser.getUrl()).to.contain("/sections/section/");
      });

      it("Then I add another household member I will be redirected to parent list collector", () => {
        $(SectionSummaryPage.peopleListAddLink()).click();
        $(ListCollectorAddPage.firstName()).setValue("Tom");
        $(ListCollectorAddPage.lastName()).setValue("Bowden");
        $(ListCollectorAddPage.submit()).click();
        expect(browser.getUrl()).to.contain("/questionnaire/list-collector/");
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
      $(ListCollectorAddPage.firstName()).setValue("Marcus");
      $(ListCollectorAddPage.lastName()).setValue("Twin");
      $(ListCollectorAddPage.submit()).click();
      $(ListCollectorPage.yes()).click();
      $(ListCollectorPage.submit()).click();
      $(ListCollectorAddPage.firstName()).setValue("Samuel");
      $(ListCollectorAddPage.lastName()).setValue("Clemens");
      $(ListCollectorAddPage.submit()).click();
      $(ListCollectorPage.yes()).click();
      $(ListCollectorPage.submit()).click();
      $(ListCollectorAddPage.firstName()).setValue("Olivia");
      $(ListCollectorAddPage.lastName()).setValue("Clemens");
      $(ListCollectorAddPage.submit()).click();
    }
  });
});
