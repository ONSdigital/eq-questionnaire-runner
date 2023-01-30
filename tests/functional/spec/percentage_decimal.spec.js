import PercentagePage from "../generated_pages/percentage/block.page.js";
import SubmitPage from "../generated_pages/percentage/submit.page.js";

describe("Percentage", () => {
  it("Given a percentage decimal answer, when I return to edit the value it does not amend the decimal places", () => {
    browser.openQuestionnaire("test_percentage.json");
    $(PercentagePage.answer()).setValue("3.333");
    $(PercentagePage.submit()).click();
    $(SubmitPage.previous()).click();
    expect(browser.getUrl()).to.contain(PercentagePage.pageName);
    expect($(PercentagePage.answer()).getHTML()).to.contain("3.333");
  });
});
