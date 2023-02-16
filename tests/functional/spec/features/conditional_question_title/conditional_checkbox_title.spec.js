import CheckBoxPage from "../../../generated_pages/titles_radio_and_checkbox/checkbox-block.page";
import NameEntryPage from "../../../generated_pages/titles_radio_and_checkbox/preamble-block.page";
import RadioButtonsPage from "../../../generated_pages/titles_radio_and_checkbox/radio-block.page";
import SubmitPage from "../../../generated_pages/titles_radio_and_checkbox/submit.page";

describe("Feature: Conditional checkbox and radio question titles", () => {
  beforeEach(async ()=> {
    await browser.openQuestionnaire("test_titles_radio_and_checkbox.json");
  });

  describe("Given I start the test_titles_radio_and_checkbox survey", () => {
    it("When I enter an expected name and submit", async ()=> {
      await $(await NameEntryPage.name()).setValue("Peter");
      await $(await NameEntryPage.submit()).click();
      await expect(await $(await CheckBoxPage.questionText()).getText()).to.contain("Did Peter make changes to this business?");
    });

    it("When I enter an unknown name and go to the checkbox page", async ()=> {
      await $(await NameEntryPage.name()).setValue("Fred");
      await $(await NameEntryPage.submit()).click();
      await expect(await $(await CheckBoxPage.questionText()).getText()).to.contain("Did this business make major changes in the following areas");
      await $(await CheckBoxPage.checkboxImplementationOfChangesToMarketingConceptsOrStrategies()).click();
      await expect(await $(await RadioButtonsPage.questionText()).getText()).to.contain("Did this business make major changes in the following areas");
    });

    it("When I enter another known name page title should include selected title", async ()=> {
      await $(await NameEntryPage.name()).setValue("Mary");
      await $(await NameEntryPage.submit()).click();

      await expect(browser.getTitle()).to.contain("Did Mary make changes to this business? - Test Survey - Checkbox and Radio titles");
    });

    it("When I enter another known name and go to the summary", async ()=> {
      await $(await NameEntryPage.name()).setValue("Mary");
      await $(await NameEntryPage.submit()).click();
      await expect(await $(await CheckBoxPage.questionText()).getText()).to.contain("Did Mary make changes to this business");
      await $(await CheckBoxPage.checkboxImplementationOfChangesToMarketingConceptsOrStrategiesLabel()).click();
      await $(await CheckBoxPage.submit()).click();
      await expect(await $(await RadioButtonsPage.questionText()).getText()).to.contain("Is Mary the boss?");
      await $(await RadioButtonsPage.radioMaybe()).click();
      await $(await RadioButtonsPage.submit()).click();
      await expect(await $(await SubmitPage.nameAnswer()).getText()).to.contain("Mary");
      await expect(await $(await SubmitPage.checkboxQuestion()).getText()).to.contain("Did Mary make changes to this business?");
    });
  });
});
