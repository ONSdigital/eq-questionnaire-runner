import PercentagePage from "../generated_pages/percentage/block.page.js";
import PercentageDecimalPage from "../generated_pages/percentage/block-decimal.page.js";
import SubmitPage from "../generated_pages/percentage/submit.page.js";
import { click, verifyUrlContains } from "../helpers";

describe("Decimal places", () => {
  it("Given an answer allows 3 decimal places, When I enter a value to 3 decimal places and return to edit the value, Then the answer should be displayed with 3 decimal places", async () => {
    await browser.openQuestionnaire("test_percentage.json");
    await click(PercentagePage.submit());
    await $(PercentageDecimalPage.decimal()).setValue("3.333");
    await click(PercentageDecimalPage.submit());
    await $(SubmitPage.previous()).click();
    await verifyUrlContains(PercentageDecimalPage.pageName);
    await expect(await $(PercentageDecimalPage.decimal()).getValue()).toBe("3.333");
  });

  it("Given an answer allows 3 decimal places, When I enter a value to 1 decimal place and return to edit the value, Then the answer should be displayed with 3 decimal places", async () => {
    await browser.openQuestionnaire("test_percentage.json");
    await click(PercentagePage.submit());
    await $(PercentageDecimalPage.decimal()).setValue("3.3");
    await click(PercentageDecimalPage.submit());
    await $(SubmitPage.previous()).click();
    await verifyUrlContains(PercentageDecimalPage.pageName);
    await expect(await $(PercentageDecimalPage.decimal()).getValue()).toBe("3.300");
  });
});
