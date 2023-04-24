import DateEntryBlockPage from "../generated_pages/first_non_empty_item/date-entry-block.page";
import DateQuestionBlockPage from "../generated_pages/first_non_empty_item/date-question-block.page";
import TotalTurnoverBlockPage from "../generated_pages/first_non_empty_item/total-turnover-block.page";

describe("First Non Empty Item Transform", () => {
  before("Launch survey", async () => {
    await browser.openQuestionnaire("test_first_non_empty_item.json");
  });

  it("When the custom date range is entered and the answer is changed back to metadata date range, Then metadata date should be displayed", async () => {
    await $(DateQuestionBlockPage.noINeedToReportForADifferentPeriod()).click();
    await $(DateQuestionBlockPage.submit()).click();
    await $(DateEntryBlockPage.dateEntryFromday()).setValue("5");
    await $(DateEntryBlockPage.dateEntryFrommonth()).setValue("01");
    await $(DateEntryBlockPage.dateEntryFromyear()).setValue("2017");
    await $(DateEntryBlockPage.dateEntryToday()).setValue("25");
    await $(DateEntryBlockPage.dateEntryTomonth()).setValue("01");
    await $(DateEntryBlockPage.dateEntryToyear()).setValue("2017");
    await $(DateEntryBlockPage.submit()).click();
    await $(TotalTurnoverBlockPage.previous()).click();
    await $(DateEntryBlockPage.previous()).click();
    await $(DateQuestionBlockPage.yesICanReportForThisPeriod()).click();
    await $(DateQuestionBlockPage.submit()).click();
    await expect(await browser.getUrl()).to.contain(TotalTurnoverBlockPage.pageName);
    await expect(await $(TotalTurnoverBlockPage.questionTitle()).getText()).to.contain("5 January 2017 to 25 January 2017");
  });
});
