import ListCollectorPage from "../generated_pages/relationships/list-collector.page.js";
import ListCollectorAddPage from "../generated_pages/relationships/list-collector-add.page.js";
import ListCollectorRemovePage from "../generated_pages/relationships/list-collector-remove.page.js";
import RelationshipsPage from "../generated_pages/relationships/relationships.page.js";
import RelationshipsInterstitialPage from "../generated_pages/relationships/relationship-interstitial.page.js";
import SectionSummaryPage from "../generated_pages/relationships/section-summary.page.js";
import { click } from "../helpers";

describe("Relationships", () => {
  const schema = "test_relationships.json";

  describe("Given I am completing the test_relationships survey,", () => {
    beforeEach("load the survey", async () => {
      await browser.openQuestionnaire(schema);
    });

    it("When I have one household member, Then I will be not be asked about relationships", async () => {
      await $(ListCollectorPage.yes()).click();
      await click(ListCollectorPage.submit());
      await $(ListCollectorAddPage.firstName()).setValue("Marcus");
      await $(ListCollectorAddPage.lastName()).setValue("Twin");
      await click(ListCollectorAddPage.submit());
      await $(ListCollectorPage.no()).click();
      // eslint-disable-next-line no-undef
      await click(ListCollectorPage.submit());
      await expect(await browser.getUrl()).to.contain("/sections/section/");
    });

    it("When I add two household members, Then I will be asked about one relationship", async () => {
      await $(ListCollectorPage.yes()).click();
      await click(ListCollectorPage.submit());
      await $(ListCollectorAddPage.firstName()).setValue("Marcus");
      await $(ListCollectorAddPage.lastName()).setValue("Twin");
      await click(ListCollectorAddPage.submit());
      await $(ListCollectorPage.yes()).click();
      await click(ListCollectorPage.submit());
      await $(ListCollectorAddPage.firstName()).setValue("Samuel");
      await $(ListCollectorAddPage.lastName()).setValue("Clemens");
      await click(ListCollectorAddPage.submit());
      await $(ListCollectorPage.no()).click();
      await $(ListCollectorPage.submit()).scrollIntoView();
      await click(ListCollectorPage.submit());
      await expect(await browser.getUrl()).to.contain(RelationshipsPage.pageName);
      await $(RelationshipsPage.husbandOrWife()).click();
      await click(RelationshipsPage.submit());
      await click(RelationshipsInterstitialPage.submit());
      await expect(await browser.getUrl()).to.contain("/sections/section/");
    });

    describe("When I add three household members,", () => {
      beforeEach("add three people", async () => {
        await addThreePeople();
      });

      it("Then I will be asked about all relationships", async () => {
        await $(ListCollectorPage.no()).click();
        await click(ListCollectorPage.submit());
        await $(RelationshipsPage.husbandOrWife()).click();
        await click(RelationshipsPage.submit());
        await $(RelationshipsPage.legallyRegisteredCivilPartner()).click();
        await click(RelationshipsPage.submit());
        await $(RelationshipsPage.husbandOrWife()).click();
        await click(RelationshipsPage.submit());
        await click(RelationshipsInterstitialPage.submit());
        await expect(await browser.getUrl()).to.contain("/sections/section/");
      });

      it("And go to the first relationship, Then the previous link should return to the list collector", async () => {
        await $(ListCollectorPage.no()).click();
        await click(ListCollectorPage.submit());
        await $(RelationshipsPage.previous()).click();
        await expect(await browser.getUrl()).to.contain("/questionnaire/list-collector/");
      });

      it("And go to the first relationship, Then the 'Brother or Sister' option should have the text 'Including half brother or half sister'", async () => {
        await $(ListCollectorPage.no()).click();
        await click(ListCollectorPage.submit());
        await expect(await $(RelationshipsPage.brotherOrSisterLabelDescription()).getText()).to.contain("Including half brother or half sister");
      });

      it("And go to the second relationship, Then the previous link should return to the first relationship", async () => {
        await $(ListCollectorPage.no()).click();
        await click(ListCollectorPage.submit());
        await $(RelationshipsPage.husbandOrWife()).click();
        await click(RelationshipsPage.submit());
        await $(RelationshipsPage.previous()).click();
        await click(RelationshipsInterstitialPage.submit());
        await expect(await browser.getUrl()).to.contain(RelationshipsPage.pageName);
        await expect(await $(RelationshipsPage.questionText()).getText()).to.contain("Marcus");
      });

      it("And go to the section summary, Then the previous link should return to the last relationship Interstitial", async () => {
        await $(ListCollectorPage.no()).click();
        await click(ListCollectorPage.submit());
        await $(RelationshipsPage.husbandOrWife()).click();
        await click(RelationshipsPage.submit());
        await $(RelationshipsPage.legallyRegisteredCivilPartner()).click();
        await click(RelationshipsPage.submit());
        await $(RelationshipsPage.husbandOrWife()).click();
        await click(RelationshipsPage.submit());
        await click(RelationshipsInterstitialPage.submit());
        await expect(await browser.getUrl()).to.contain("/sections/section/");
        await $(SectionSummaryPage.previous()).click();
        await $(RelationshipsInterstitialPage.previous()).click();
        await expect(await browser.getUrl()).to.contain(RelationshipsPage.pageName);
        await expect(await $(RelationshipsPage.questionText()).getText()).to.contain("Olivia");
      });

      it("When I add all relationships and return to the relationships, Then the relationships should be populated", async () => {
        await $(ListCollectorPage.no()).click();
        await click(ListCollectorPage.submit());
        await $(RelationshipsPage.husbandOrWife()).click();
        await click(RelationshipsPage.submit());
        await $(RelationshipsPage.legallyRegisteredCivilPartner()).click();
        await click(RelationshipsPage.submit());
        await $(RelationshipsPage.husbandOrWife()).click();
        await click(RelationshipsPage.submit());
        await click(RelationshipsInterstitialPage.submit());
        await expect(await browser.getUrl()).to.contain("/sections/section/");
        await $(SectionSummaryPage.previous()).click();
        await $(RelationshipsInterstitialPage.previous()).click();
        await expect(await $(RelationshipsPage.husbandOrWife()).isSelected()).to.be.true;
        await $(RelationshipsPage.previous()).click();
        await expect(await $(RelationshipsPage.legallyRegisteredCivilPartner()).isSelected()).to.be.true;
      });

      it("And go to the first relationship, Then the person's name should be in the question title and playback text", async () => {
        await $(ListCollectorPage.no()).click();
        await click(ListCollectorPage.submit());
        await expect(await $(ListCollectorPage.questionText()).getText()).to.contain("Marcus Twin");
        await expect(await $(RelationshipsPage.playback()).getText()).to.contain("Marcus Twin");
      });

      it("And go to the first relationship and submit without selecting an option, Then an error should be displayed", async () => {
        await $(ListCollectorPage.no()).click();
        await click(ListCollectorPage.submit());
        await click(RelationshipsPage.submit());
        await expect(await $(RelationshipsPage.error()).isDisplayed()).to.be.true;
      });

      it("And go to the first relationship and click 'Save and sign out', Then I should be signed out", async () => {
        await $(ListCollectorPage.no()).click();
        await click(ListCollectorPage.submit());
        await $(RelationshipsPage.husbandOrWife()).click();
        await $(RelationshipsPage.saveSignOut()).click();
        await expect(await browser.getUrl()).to.not.contain("questionnaire");
      });

      it("And go to the first relationship, select a relationship and click 'Save and sign out', Then I should be signed out", async () => {
        await $(ListCollectorPage.no()).click();
        await click(ListCollectorPage.submit());
        await $(RelationshipsPage.saveSignOut()).click();
        await expect(await browser.getUrl()).to.not.contain("questionnaire");
      });
    });

    describe("When I have added one or more household members after answering the relationships question,", () => {
      beforeEach("add three people and complete their relationships", async () => {
        await addThreePeopleAndCompleteRelationships();
      });

      it("Then I delete one of the original household members I will not be asked for the original members relationships again", async () => {
        await $(SectionSummaryPage.peopleListRemoveLink(1)).click();
        await $(ListCollectorRemovePage.yes()).click();
        await click(ListCollectorRemovePage.submit());
        await expect(await browser.getUrl()).to.contain("/sections/section/");
      });

      it("Then I add another household member I will be redirected to parent list collector", async () => {
        await $(SectionSummaryPage.peopleListAddLink()).click();
        await $(ListCollectorAddPage.firstName()).setValue("Tom");
        await $(ListCollectorAddPage.lastName()).setValue("Bowden");
        await click(ListCollectorAddPage.submit());
        await expect(await browser.getUrl()).to.contain("/questionnaire/list-collector/");
      });
    });

    async function addThreePeopleAndCompleteRelationships() {
      await addThreePeople();

      await $(ListCollectorPage.no()).click();
      await $(ListCollectorPage.submit()).scrollIntoView();
      await click(ListCollectorPage.submit());
      await $(RelationshipsPage.husbandOrWife()).click();
      await click(RelationshipsPage.submit());
      await $(RelationshipsPage.legallyRegisteredCivilPartner()).click();
      await click(RelationshipsPage.submit());
      await $(RelationshipsPage.husbandOrWife()).click();
      await click(RelationshipsPage.submit());
      await click(RelationshipsInterstitialPage.submit());
    }

    async function addThreePeople() {
      await $(ListCollectorPage.yes()).click();
      await click(ListCollectorPage.submit());
      await $(ListCollectorAddPage.firstName()).setValue("Marcus");
      await $(ListCollectorAddPage.lastName()).setValue("Twin");
      await click(ListCollectorAddPage.submit());
      await $(ListCollectorPage.yes()).click();
      await click(ListCollectorPage.submit());
      await $(ListCollectorAddPage.firstName()).setValue("Samuel");
      await $(ListCollectorAddPage.lastName()).setValue("Clemens");
      await $(ListCollectorAddPage.submit()).scrollIntoView();
      await click(ListCollectorAddPage.submit());
      await $(ListCollectorPage.yes()).click();
      await click(ListCollectorPage.submit());
      await $(ListCollectorAddPage.firstName()).setValue("Olivia");
      await $(ListCollectorAddPage.lastName()).setValue("Clemens");
      await click(ListCollectorAddPage.submit());
    }
  });
});
