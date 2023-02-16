import RadioVoluntaryTruePage from "../../../generated_pages/radio_voluntary/radio-voluntary-true.page.js";
import RadioVoluntaryFalsePage from "../../../generated_pages/radio_voluntary/radio-voluntary-false.page.js";

describe("Component: Radio", () => {
  describe("Given I start a Voluntary Radio survey", () => {
    before(async ()=> {
      await browser.openQuestionnaire("test_radio_voluntary.json");
    });

    it("When I select a voluntary radio option, Then the clear button should be displayed", async ()=> {
      await $(await RadioVoluntaryTruePage.coffee()).click();
      await expect(await $(await RadioVoluntaryTruePage.clearSelectionButton()).isDisplayed()).to.equal(true);
    });

    it("When I select a voluntary radio option and click the clear button, Then the radio option should not be selected and the clear button should not be displayed", async ()=> {
      await $(await RadioVoluntaryTruePage.coffee()).click();
      await $(await RadioVoluntaryTruePage.clearSelectionButton()).click();
      await expect(await $(await RadioVoluntaryTruePage.coffee()).isSelected()).to.equal(false);
      await expect(await $(await RadioVoluntaryTruePage.clearSelectionButton()).isDisplayed()).to.equal(false);
    });

    it("When I clear a previously saved voluntary radio option and submit, Then when returning to the page the radio option is no longer selected", async ()=> {
      await $(await RadioVoluntaryTruePage.coffee()).click();
      await $(await RadioVoluntaryTruePage.submit()).click();
      await $(await RadioVoluntaryTruePage.previous()).click();
      await $(await RadioVoluntaryTruePage.clearSelectionButton()).click();
      await $(await RadioVoluntaryTruePage.submit()).click();
      await $(await RadioVoluntaryTruePage.previous()).click();
      await expect(await $(await RadioVoluntaryTruePage.coffee()).isSelected()).to.equal(false);
      await expect(await $(await RadioVoluntaryTruePage.clearSelectionButton()).isDisplayed()).to.equal(false);
    });

    it("When I select a non-voluntary radio option, Then the clear button should not be displayed on the page", async ()=> {
      await $(await RadioVoluntaryTruePage.submit()).click();
      await $(await RadioVoluntaryFalsePage.iceCream()).click();
      await expect(await $(await RadioVoluntaryFalsePage.clearSelectionButton()).isDisplayed()).to.equal(false);
    });
  });
});
