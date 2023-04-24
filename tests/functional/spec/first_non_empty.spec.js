import DateEntryBlockPage from "../generated_pages/first_non_empy_item/date-entry-block.page";
import DateQuestionBlockPage from "../generated_pages/first_non_empy_item/date-question-block.page";
import TotalTurnoverBlockPage from "../generated_pages/first_non_empy_item/total-turnover-block.page";

describe("First Non Empty Item Transform", () => {
  describe('', () => {
    before("Launch survey", async () => {
      await browser.openQuestionnaire("test_first_non_empty_item.json");
    });

    it('When the custom date range is entered and the answer is changed back to metadata date range, Then metadata date should be displayed', async () => {
        await $(DateQuestionBlockPage.noINeedToReportForADifferentPeriod()).click();
        await $(DateEntryBlockPage.dateEntryFromday()).setValue("1");
        await $(DateEntryBlockPage.dateEntryFrommonth()).setValue("06");
        await $(DateEntryBlockPage.dateEntryFromyear()).setValue("2016");
        await $(DateEntryBlockPage.dateEntryToday()).setValue("11");
        await $(DateEntryBlockPage.dateEntryTomonth()).setValue("06");
        await $(DateEntryBlockPage.dateEntryToyear()).setValue("2016");
        await $(DateEntryBlockPage.submit());
        await $(TotalTurnoverBlockPage.previous());
        await $(DateEntryBlockPage.previous());
        await $(DateQuestionBlockPage.yesICanReportForThisPeriod()).click();
        await expect(await browser.getUrl()).to.contain(TotalTurnoverBlockPage.pageName);
        await expect(await $(TotalTurnoverBlockPage.questionTitle()).getText()).to.contain("1 June 2016 to 11 June 2016");
    });
  });
});
