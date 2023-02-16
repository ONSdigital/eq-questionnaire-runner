import ListCollectorPage from "../generated_pages/relationships/list-collector.page.js";
import ListCollectorAddPage from "../generated_pages/relationships/list-collector-add.page.js";
import ListCollectorRemovePage from "../generated_pages/relationships/list-collector-remove.page.js";
import RelationshipsPage from "../generated_pages/relationships/relationships.page.js";
import RelationshipsInterstitialPage from "../generated_pages/relationships/relationship-interstitial.page.js";
import SectionSummaryPage from "../generated_pages/relationships/section-summary.page.js";

describe("Relationships", () => {
  const schema = "test_relationships.json";

  describe("Given I am completing the test_relationships survey,", () => {
    beforeEach("load the survey", async ()=> {
      await browser.openQuestionnaire(schema);
    });

    it("When I have one household member, Then I will be not be asked about relationships", async ()=> {
      await $(await ListCollectorPage.yes()).click();
      await $(await ListCollectorPage.submit()).click();
      await $(await ListCollectorAddPage.firstName()).setValue("Marcus");
      await $(await ListCollectorAddPage.lastName()).setValue("Twin");
      await $(await ListCollectorAddPage.submit()).click();
      await $(await ListCollectorPage.no()).click();
      await $(await ListCollectorPage.submit()).click();
      await expect(browser.getUrl()).to.contain("/sections/section/");
    });

    it("When I add two household members, Then I will be asked about one relationship", async ()=> {
      await $(await ListCollectorPage.yes()).click();
      await $(await ListCollectorPage.submit()).click();
      await $(await ListCollectorAddPage.firstName()).setValue("Marcus");
      await $(await ListCollectorAddPage.lastName()).setValue("Twin");
      await $(await ListCollectorAddPage.submit()).click();
      await $(await ListCollectorPage.yes()).click();
      await $(await ListCollectorPage.submit()).click();
      await $(await ListCollectorAddPage.firstName()).setValue("Samuel");
      await $(await ListCollectorAddPage.lastName()).setValue("Clemens");
      await $(await ListCollectorAddPage.submit()).click();
      await $(await ListCollectorPage.no()).click();
      await $(await ListCollectorPage.submit()).click();
      await expect(browser.getUrl()).to.contain(RelationshipsPage.pageName);
      await $(await RelationshipsPage.husbandOrWife()).click();
      await $(await RelationshipsPage.submit()).click();
      await $(await RelationshipsInterstitialPage.submit()).click();
      await expect(browser.getUrl()).to.contain("/sections/section/");
    });

    describe("When I add three household members,", () => {
      beforeEach("add three people", async ()=> {
        addThreePeople();
      });

      it("Then I will be asked about all relationships", async ()=> {
        await $(await ListCollectorPage.no()).click();
        await $(await ListCollectorPage.submit()).click();
        await $(await RelationshipsPage.husbandOrWife()).click();
        await $(await RelationshipsPage.submit()).click();
        await $(await RelationshipsPage.legallyRegisteredCivilPartner()).click();
        await $(await RelationshipsPage.submit()).click();
        await $(await RelationshipsPage.husbandOrWife()).click();
        await $(await RelationshipsPage.submit()).click();
        await $(await RelationshipsInterstitialPage.submit()).click();
        await expect(browser.getUrl()).to.contain("/sections/section/");
      });

      it("And go to the first relationship, Then the previous link should return to the list collector", async ()=> {
        await $(await ListCollectorPage.no()).click();
        await $(await ListCollectorPage.submit()).click();
        await $(await RelationshipsPage.previous()).click();
        await expect(browser.getUrl()).to.contain("/questionnaire/list-collector/");
      });

      it("And go to the first relationship, Then the 'Brother or Sister' option should have the text 'Including half brother or half sister'", async ()=> {
        await $(await ListCollectorPage.no()).click();
        await $(await ListCollectorPage.submit()).click();
        await expect(await $(await RelationshipsPage.brotherOrSisterLabelDescription()).getText()).to.contain("Including half brother or half sister");
      });

      it("And go to the second relationship, Then the previous link should return to the first relationship", async ()=> {
        await $(await ListCollectorPage.no()).click();
        await $(await ListCollectorPage.submit()).click();
        await $(await RelationshipsPage.husbandOrWife()).click();
        await $(await RelationshipsPage.submit()).click();
        await $(await RelationshipsPage.previous()).click();
        await $(await RelationshipsInterstitialPage.submit()).click();
        await expect(browser.getUrl()).to.contain(RelationshipsPage.pageName);
        await expect(await $(await RelationshipsPage.questionText()).getText()).to.contain("Marcus");
      });

      it("And go to the section summary, Then the previous link should return to the last relationship Interstitial", async ()=> {
        await $(await ListCollectorPage.no()).click();
        await $(await ListCollectorPage.submit()).click();
        await $(await RelationshipsPage.husbandOrWife()).click();
        await $(await RelationshipsPage.submit()).click();
        await $(await RelationshipsPage.legallyRegisteredCivilPartner()).click();
        await $(await RelationshipsPage.submit()).click();
        await $(await RelationshipsPage.husbandOrWife()).click();
        await $(await RelationshipsPage.submit()).click();
        await $(await RelationshipsInterstitialPage.submit()).click();
        await expect(browser.getUrl()).to.contain("/sections/section/");
        await $(await SectionSummaryPage.previous()).click();
        await $(await RelationshipsInterstitialPage.previous()).click();
        await expect(browser.getUrl()).to.contain(RelationshipsPage.pageName);
        await expect(await $(await RelationshipsPage.questionText()).getText()).to.contain("Olivia");
      });

      it("When I add all relationships and return to the relationships, Then the relationships should be populated", async ()=> {
        await $(await ListCollectorPage.no()).click();
        await $(await ListCollectorPage.submit()).click();
        await $(await RelationshipsPage.husbandOrWife()).click();
        await $(await RelationshipsPage.submit()).click();
        await $(await RelationshipsPage.legallyRegisteredCivilPartner()).click();
        await $(await RelationshipsPage.submit()).click();
        await $(await RelationshipsPage.husbandOrWife()).click();
        await $(await RelationshipsPage.submit()).click();
        await $(await RelationshipsInterstitialPage.submit()).click();
        await expect(browser.getUrl()).to.contain("/sections/section/");
        await $(await SectionSummaryPage.previous()).click();
        await $(await RelationshipsInterstitialPage.previous()).click();
        await expect(await $(await RelationshipsPage.husbandOrWife()).isSelected()).to.be.true;
        await $(await RelationshipsPage.previous()).click();
        await expect(await $(await RelationshipsPage.legallyRegisteredCivilPartner()).isSelected()).to.be.true;
      });

      it("And go to the first relationship, Then the person's name should be in the question title and playback text", async ()=> {
        await $(await ListCollectorPage.no()).click();
        await $(await ListCollectorPage.submit()).click();
        await expect(await $(await ListCollectorPage.questionText()).getText()).to.contain("Marcus Twin");
        await expect(await $(await RelationshipsPage.playback()).getText()).to.contain("Marcus Twin");
      });

      it("And go to the first relationship and submit without selecting an option, Then an error should be displayed", async ()=> {
        await $(await ListCollectorPage.no()).click();
        await $(await ListCollectorPage.submit()).click();
        await $(await RelationshipsPage.submit()).click();
        await expect(await $(await RelationshipsPage.error()).isDisplayed()).to.be.true;
      });

      it("And go to the first relationship and click 'Save and sign out', Then I should be signed out", async ()=> {
        await $(await ListCollectorPage.no()).click();
        await $(await ListCollectorPage.submit()).click();
        await $(await RelationshipsPage.husbandOrWife()).click();
        await $(await RelationshipsPage.saveSignOut()).click();
        await expect(browser.getUrl()).to.not.contain("questionnaire");
      });

      it("And go to the first relationship, select a relationship and click 'Save and sign out', Then I should be signed out", async ()=> {
        await $(await ListCollectorPage.no()).click();
        await $(await ListCollectorPage.submit()).click();
        await $(await RelationshipsPage.saveSignOut()).click();
        await expect(browser.getUrl()).to.not.contain("questionnaire");
      });
    });

    describe("When I have added one or more household members after answering the relationships question,", () => {
      beforeEach("add three people and complete their relationships", async ()=> {
        addThreePeopleAndCompleteRelationships();
      });

      it("Then I delete one of the original household members I will not be asked for the original members relationships again", async ()=> {
        await $(await SectionSummaryPage.peopleListRemoveLink(1)).click();
        await $(await ListCollectorRemovePage.yes()).click();
        await $(await ListCollectorRemovePage.submit()).click();
        await expect(browser.getUrl()).to.contain("/sections/section/");
      });

      it("Then I add another household member I will be redirected to parent list collector", async ()=> {
        await $(await SectionSummaryPage.peopleListAddLink()).click();
        await $(await ListCollectorAddPage.firstName()).setValue("Tom");
        await $(await ListCollectorAddPage.lastName()).setValue("Bowden");
        await $(await ListCollectorAddPage.submit()).click();
        await expect(browser.getUrl()).to.contain("/questionnaire/list-collector/");
      });
    });

    function addThreePeopleAndCompleteRelationships() {
      addThreePeople();

      await $(await ListCollectorPage.no()).click();
      await $(await ListCollectorPage.submit()).click();
      await $(await RelationshipsPage.husbandOrWife()).click();
      await $(await RelationshipsPage.submit()).click();
      await $(await RelationshipsPage.legallyRegisteredCivilPartner()).click();
      await $(await RelationshipsPage.submit()).click();
      await $(await RelationshipsPage.husbandOrWife()).click();
      await $(await RelationshipsPage.submit()).click();
      await $(await RelationshipsInterstitialPage.submit()).click();
    }

    function addThreePeople() {
      await $(await ListCollectorPage.yes()).click();
      await $(await ListCollectorPage.submit()).click();
      await $(await ListCollectorAddPage.firstName()).setValue("Marcus");
      await $(await ListCollectorAddPage.lastName()).setValue("Twin");
      await $(await ListCollectorAddPage.submit()).click();
      await $(await ListCollectorPage.yes()).click();
      await $(await ListCollectorPage.submit()).click();
      await $(await ListCollectorAddPage.firstName()).setValue("Samuel");
      await $(await ListCollectorAddPage.lastName()).setValue("Clemens");
      await $(await ListCollectorAddPage.submit()).click();
      await $(await ListCollectorPage.yes()).click();
      await $(await ListCollectorPage.submit()).click();
      await $(await ListCollectorAddPage.firstName()).setValue("Olivia");
      await $(await ListCollectorAddPage.lastName()).setValue("Clemens");
      await $(await ListCollectorAddPage.submit()).click();
    }
  });
});
