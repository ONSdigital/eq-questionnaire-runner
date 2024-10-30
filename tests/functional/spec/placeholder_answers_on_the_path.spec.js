import DateEntryBlockPage from "../generated_pages/placeholder_first_non_empty_item/date-entry-block.page";
import DateQuestionBlockPage from "../generated_pages/placeholder_first_non_empty_item/date-question-block.page";
import TotalTurnoverBlockPage from "../generated_pages/placeholder_first_non_empty_item/total-turnover-block.page";
import FoodQuestionBlockPage from "../generated_pages/placeholder_first_non_empty_item_cross_section_dependencies/food-question-block.page";

import AddPersonPage from "../generated_pages/placeholder_first_non_empty_item_repeating_sections/list-collector-add.page";
import ListCollectorPage from "../generated_pages/placeholder_first_non_empty_item_repeating_sections/list-collector.page";
import PersonalDetailsBlockPage from "../generated_pages/placeholder_first_non_empty_item_repeating_sections/personal-details-block.page";
import HubPage from "../base_pages/hub.page.js";
import {click, verifyUrlContains} from "../helpers";

describe("First Non Empty Item Transform", () => {
  before("Launch survey", async () => {
    await browser.openQuestionnaire("test_placeholder_first_non_empty_item.json");
  });

  it("When the custom date range is entered and the answer is changed back to metadata date range, Then metadata date should be displayed", async () => {
    // Set the date
    await $(DateQuestionBlockPage.noINeedToReportForADifferentPeriod()).click();
    await click(DateQuestionBlockPage.submit());
    await $(DateEntryBlockPage.dateEntryFromday()).setValue("5");
    await $(DateEntryBlockPage.dateEntryFrommonth()).setValue("01");
    await $(DateEntryBlockPage.dateEntryFromyear()).setValue("2017");
    await $(DateEntryBlockPage.dateEntryToday()).setValue("25");
    await $(DateEntryBlockPage.dateEntryTomonth()).setValue("01");
    await $(DateEntryBlockPage.dateEntryToyear()).setValue("2017");
    await click(DateEntryBlockPage.submit());
    // Change to original dates
    await $(TotalTurnoverBlockPage.previous()).click();
    await $(DateEntryBlockPage.previous()).click();
    await $(DateQuestionBlockPage.yesICanReportForThisPeriod()).click();
    await click(DateQuestionBlockPage.submit());
    await verifyUrlContains(TotalTurnoverBlockPage.pageName);
    expect(await $(TotalTurnoverBlockPage.questionTitle()).getText()).toContain("1 January 2017 to 1 February 2017");
  });
});

describe("First Non Empty Item Transform Cross Section", () => {
  before("Launch survey", async () => {
    await browser.openQuestionnaire("test_placeholder_first_non_empty_item_cross_section_dependencies.json");
    await click(HubPage.submit());
  });

  it("Given a custom date range is entered, When the answer is changed back to metadata range, Then the metadata date should be displayed for both sections", async () => {
    // Set the date
    await $(DateQuestionBlockPage.noINeedToReportForADifferentPeriod()).click();
    await click(DateQuestionBlockPage.submit());
    await $(DateEntryBlockPage.dateEntryFromday()).setValue("5");
    await $(DateEntryBlockPage.dateEntryFrommonth()).setValue("01");
    await $(DateEntryBlockPage.dateEntryFromyear()).setValue("2017");
    await $(DateEntryBlockPage.dateEntryToday()).setValue("25");
    await $(DateEntryBlockPage.dateEntryTomonth()).setValue("01");
    await $(DateEntryBlockPage.dateEntryToyear()).setValue("2017");
    await click(DateEntryBlockPage.submit());

    // Check date changed and then change to original dates
    await click(HubPage.submit());
    expect(await $(FoodQuestionBlockPage.questionTitle()).getText()).toContain("5 January 2017 to 25 January 2017");
    await $(FoodQuestionBlockPage.previous()).click();
    await $(HubPage.summaryRowLink("default-section")).click();
    await $(DateQuestionBlockPage.yesICanReportForThisPeriod()).click();
    await click(DateQuestionBlockPage.submit());
    // Check the next section if the metadata date is shown
    await click(HubPage.submit());
    await verifyUrlContains(FoodQuestionBlockPage.pageName);
    expect(await $(FoodQuestionBlockPage.questionTitle()).getText()).toContain("1 January 2017 to 1 February 2017");
  });
});

describe("First Non Empty Item Transform Repeating Sections", () => {
  before("Launch survey", async () => {
    await browser.openQuestionnaire("test_placeholder_first_non_empty_item_repeating_sections.json");
    await click(HubPage.submit());
  });
  it("Given a custom date range is entered, When the answer is changed back to metadata range, Then the metadata date should be displayed for the repeating section title", async () => {
    // Set the date
    await $(DateQuestionBlockPage.noINeedToReportForADifferentPeriod()).click();
    await click(DateQuestionBlockPage.submit());
    await $(DateEntryBlockPage.dateEntryFromday()).setValue("5");
    await $(DateEntryBlockPage.dateEntryFrommonth()).setValue("01");
    await $(DateEntryBlockPage.dateEntryFromyear()).setValue("2017");
    await $(DateEntryBlockPage.dateEntryToday()).setValue("25");
    await $(DateEntryBlockPage.dateEntryTomonth()).setValue("01");
    await $(DateEntryBlockPage.dateEntryToyear()).setValue("2017");
    await click(DateEntryBlockPage.submit());
    await click(HubPage.submit());

    // Add a person to the list collector
    await $(ListCollectorPage.yes()).click();
    await click(ListCollectorPage.submit());
    await $(AddPersonPage.firstName()).setValue("Paul");
    await $(AddPersonPage.lastName()).setValue("Pogba");
    await click(AddPersonPage.submit());
    await $(ListCollectorPage.no()).click();
    await click(ListCollectorPage.submit());
    await click(ListCollectorPage.submit());
    // Check Repeating Section has the set dates
    await click(HubPage.submit());
    await verifyUrlContains(PersonalDetailsBlockPage.pageName);
    expect(await $(PersonalDetailsBlockPage.questionTitle()).getText()).toContain("5 January 2017 to 25 January 2017");
    await $(PersonalDetailsBlockPage.previous()).click();
    // Change to original dates
    await $(HubPage.summaryRowLink("date-section")).click();
    await $(DateQuestionBlockPage.yesICanReportForThisPeriod()).click();
    await click(DateQuestionBlockPage.submit());
    await click(HubPage.submit());
    // Check the list collector has metadata dates in the title
    await verifyUrlContains(PersonalDetailsBlockPage.pageName);
    expect(await $(PersonalDetailsBlockPage.questionTitle()).getText()).toContain("1 January 2017 to 1 February 2017");
  });
});
