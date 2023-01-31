import PercentagePage from "../generated_pages/percentage/block.page.js";
import PercentageDecimalPage from "../generated_pages/percentage/block-decimal.page.js";
import SubmitPage from "../generated_pages/percentage/submit.page.js";

describe("Percentage", () => {
  it("Given a percentage decimal answer, when I return to edit the value it does not amend the decimal places", () => {
    browser.openQuestionnaire("test_percentage.json");
    $(PercentagePage.submit()).click();
    $(PercentageDecimalPage.decimal()).setValue("3.333");
    $(PercentageDecimalPage.submit()).click();
    $(SubmitPage.previous()).click();
    expect(browser.getUrl()).to.contain(PercentageDecimalPage.pageName);
    expect($(PercentageDecimalPage.decimal()).getValue()).to.equal("3.333");
    });
});
