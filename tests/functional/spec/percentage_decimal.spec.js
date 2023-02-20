import PercentagePage from "../generated_pages/percentage/block.page.js";
import PercentageDecimalPage from "../generated_pages/percentage/block-decimal.page.js";
import SubmitPage from "../generated_pages/percentage/submit.page.js";

describe("Decimal places", () => {
  it("Given an answer allows 3 decimal places, When I enter a value to 3 decimal places and return to edit the value, Then the answer should be displayed with 3 decimal places", async () => {
    await browser.openQuestionnaire("test_percentage.json");
    await $(PercentagePage.submit()).click();
    await $(PercentageDecimalPage.decimal()).setValue("3.333");
    await $(PercentageDecimalPage.submit()).click();
    await $(SubmitPage.previous()).click();
    await expect(await browser.getUrl()).to.contain(PercentageDecimalPage.pageName);
    await expect(await $(PercentageDecimalPage.decimal()).getValue()).to.equal("3.333");
  });

  it("Given an answer allows 3 decimal places, When I enter a value to 1 decimal place and return to edit the value, Then the answer should be displayed with 3 decimal places", async () => {
    await browser.openQuestionnaire("test_percentage.json");
    await $(PercentagePage.submit()).click();
    await $(PercentageDecimalPage.decimal()).setValue("3.3");
    await $(PercentageDecimalPage.submit()).click();
    await $(SubmitPage.previous()).click();
    await expect(await browser.getUrl()).to.contain(PercentageDecimalPage.pageName);
    await expect(await $(PercentageDecimalPage.decimal()).getValue()).to.equal("3.300");
  });
});
