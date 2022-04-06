import HealedTheQuickestPage from "../../../generated_pages/dynamic_radio_options_from_checkbox/healed-the-quickest.page";
import InjurySustainedPage from "../../../generated_pages/dynamic_radio_options_from_checkbox/injury-sustained.page";
import MostSeriousInjuryPage from "../../../generated_pages/dynamic_radio_options_from_checkbox/most-serious-injury.page";
import SubmitPage from "../../../generated_pages/dynamic_radio_options_from_checkbox/submit.page";

describe("Dynamic radio options from checkbox answers", () => {
  describe("Given the dynamic radio options from checkbox questionnaire and I am on the checkbox answer page", () => {
    it("When the respondent answers the checkbox question and submits, Then the radio question should show the answers from that checkbox as options, as well as a static option", () => {
      browser.openQuestionnaire("test_dynamic_radio_options_from_checkbox.json");
      $(InjurySustainedPage.head()).click();
      $(InjurySustainedPage.body()).click();
      $(InjurySustainedPage.submit()).click();

      expect(browser.getUrl()).to.contain(MostSeriousInjuryPage.pageName);
      expect($(MostSeriousInjuryPage.answerLabelByIndex(0)).getText()).to.contain("Head");
      expect($(MostSeriousInjuryPage.answerLabelByIndex(1)).getText()).to.contain("Body");
      expect($(MostSeriousInjuryPage.answerLabelByIndex(2)).getText()).to.contain("They were of equal severity (static option)");
      expect($(MostSeriousInjuryPage.answerLabelByIndex(3)).isExisting()).to.be.false;
    });

    it("When the respondent answers the radio question and submits, Then the next radio question should show only the answers from the first checkbox as options", () => {
      $(MostSeriousInjuryPage.answerLabelByIndex(0)).click();
      $(MostSeriousInjuryPage.submit()).click();

      expect(browser.getUrl()).to.contain(HealedTheQuickestPage.pageName);
      expect($(HealedTheQuickestPage.answerLabelByIndex(0)).getText()).to.contain("Head");
      expect($(HealedTheQuickestPage.answerLabelByIndex(1)).getText()).to.contain("Body");
      expect($(HealedTheQuickestPage.answerLabelByIndex(2)).isExisting()).to.be.false;
    });

    it("When the respondent answers the radio question and submits, then the summary should display all the answers correctly", () => {
      $(HealedTheQuickestPage.answerLabelByIndex(1)).click();
      $(HealedTheQuickestPage.submit()).click();

      expect(browser.getUrl()).to.contain(SubmitPage.pageName);
      expect($(SubmitPage.injurySustainedAnswer()).getText()).to.contain("Head\nBody");
      expect($(SubmitPage.mostSeriousInjuryAnswer()).getText()).to.contain("Head");
      expect($(SubmitPage.healedTheQuickestAnswer()).getText()).to.contain("Body");
    });

    it("When I edit and change the answer which the dynamic options is dependent on, then my selected answers are removed", () => {
      $(SubmitPage.injurySustainedAnswerEdit()).click();
      $(InjurySustainedPage.arms()).click();
      $(InjurySustainedPage.submit()).click();

      expect($(MostSeriousInjuryPage.answerByIndex(0)).isSelected()).to.be.false;
      expect($(MostSeriousInjuryPage.answerByIndex(1)).isSelected()).to.be.false;
    });
  });
});
