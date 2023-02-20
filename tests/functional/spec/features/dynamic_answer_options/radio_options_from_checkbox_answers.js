import HealedTheQuickestPage from "../../../generated_pages/dynamic_radio_options_from_checkbox/healed-the-quickest.page";
import InjurySustainedPage from "../../../generated_pages/dynamic_radio_options_from_checkbox/injury-sustained.page";
import MostSeriousInjuryPage from "../../../generated_pages/dynamic_radio_options_from_checkbox/most-serious-injury.page";
import SubmitPage from "../../../generated_pages/dynamic_radio_options_from_checkbox/submit.page";

describe("Dynamic radio options from checkbox answers", () => {
  describe("Given the dynamic radio options from checkbox questionnaire and I am on the checkbox answer page", () => {
    it("When the respondent answers the checkbox question and submits, Then the radio question should show the answers from that checkbox as options, as well as a static option", async () => {
      await browser.openQuestionnaire("test_dynamic_radio_options_from_checkbox.json");
      await $(InjurySustainedPage.head()).click();
      await $(InjurySustainedPage.body()).click();
      await $(InjurySustainedPage.submit()).click();

      await expect(await browser.getUrl()).to.contain(MostSeriousInjuryPage.pageName);
      await expect(await $(MostSeriousInjuryPage.answerLabelByIndex(0)).getText()).to.contain("Head");
      await expect(await $(MostSeriousInjuryPage.answerLabelByIndex(1)).getText()).to.contain("Body");
      await expect(await $(MostSeriousInjuryPage.answerLabelByIndex(2)).getText()).to.contain("They were of equal severity (static option)");
      await expect(await $(MostSeriousInjuryPage.answerLabelByIndex(3)).isExisting()).to.be.false;
    });

    it("When the respondent answers the radio question and submits, Then the next radio question should show only the answers from the first checkbox as options", async () => {
      await $(MostSeriousInjuryPage.answerLabelByIndex(0)).click();
      await $(MostSeriousInjuryPage.submit()).click();

      await expect(await browser.getUrl()).to.contain(HealedTheQuickestPage.pageName);
      await expect(await $(HealedTheQuickestPage.answerLabelByIndex(0)).getText()).to.contain("Head");
      await expect(await $(HealedTheQuickestPage.answerLabelByIndex(1)).getText()).to.contain("Body");
      await expect(await $(HealedTheQuickestPage.answerLabelByIndex(2)).isExisting()).to.be.false;
    });

    it("When the respondent answers the radio question and submits, then the summary should display all the answers correctly", async () => {
      await $(HealedTheQuickestPage.answerLabelByIndex(1)).click();
      await $(HealedTheQuickestPage.submit()).click();

      await expect(await browser.getUrl()).to.contain(SubmitPage.pageName);
      await expect(await $(SubmitPage.injurySustainedAnswer()).getText()).to.contain("Head\nBody");
      await expect(await $(SubmitPage.mostSeriousInjuryAnswer()).getText()).to.contain("Head");
      await expect(await $(SubmitPage.healedTheQuickestAnswer()).getText()).to.contain("Body");
    });

    it("When I edit and change the answer which the dynamic options is dependent on, then my selected answers are removed", async () => {
      await $(SubmitPage.injurySustainedAnswerEdit()).click();
      await $(InjurySustainedPage.arms()).click();
      await $(InjurySustainedPage.submit()).click();

      await expect(await $(MostSeriousInjuryPage.answerByIndex(0)).isSelected()).to.be.false;
      await expect(await $(MostSeriousInjuryPage.answerByIndex(1)).isSelected()).to.be.false;
    });
  });
});
