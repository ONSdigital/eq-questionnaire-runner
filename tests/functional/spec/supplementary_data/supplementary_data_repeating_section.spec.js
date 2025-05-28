import { click } from "../../helpers";
import { expect } from "@wdio/globals";
import { getRandomString } from "../../jwt_helper";
import AddAdditionalEmployeePage from "../../generated_pages/supplementary_data/list-collector-additional-add.page.js";
import AdditionalLengthOfEmploymentPage from "../../generated_pages/supplementary_data/additional-length-of-employment.page.js";
import AnyAdditionalEmployeesPage from "../../generated_pages/supplementary_data/any-additional-employees.page.js";

import HubPage from "../../base_pages/hub.page";

import LengthOfEmploymentPage from "../../generated_pages/supplementary_data/length-of-employment.page.js";
import ListCollectorAdditionalPage from "../../generated_pages/supplementary_data/list-collector-additional.page.js";
import ListCollectorEmployeesPage from "../../generated_pages/supplementary_data/list-collector-employees.page.js";

import Section3Page from "../../generated_pages/supplementary_data/section-3-summary.page.js";
import Section4Page from "../../generated_pages/supplementary_data/section-4-summary.page.js";
import Section5Page from "../../generated_pages/supplementary_data/section-5-summary.page.js";

describe("Using supplementary data", () => {
  const responseId = getRandomString(16);

  before("Starting the survey", async () => {
    await browser.openQuestionnaire("test_supplementary_data_with_repeating_section.json", {
      version: "v2",
      sdsDatasetId: "203b2f9d-c500-8175-98db-86ffcfdccfa3",
      responseId,
    });
  });
  it("Given I have a list collector content block using a supplementary list, When I start the section, I see the supplementary list items in the list", async () => {
    await click(HubPage.submit());
    await expect(await $(ListCollectorEmployeesPage.listLabel(1)).getText()).toBe("Harry Potter");
    await expect(await $(ListCollectorEmployeesPage.listLabel(2)).getText()).toBe("Clark Kent");
    await click(ListCollectorEmployeesPage.submit());
  });

  it("Given I add some additional employees via another list collector, When I return to the Hub, Then I see new enabled sections for the supplementary list items and my added ones", async () => {
    await click(HubPage.submit());
    await $(AnyAdditionalEmployeesPage.yes()).click();
    await click(AnyAdditionalEmployeesPage.submit());
    await $(AddAdditionalEmployeePage.employeeFirstName()).setValue("Jane");
    await $(AddAdditionalEmployeePage.employeeLastName()).setValue("Doe");
    await click(AddAdditionalEmployeePage.submit());
    await $(ListCollectorAdditionalPage.yes()).click();
    await click(ListCollectorAdditionalPage.submit());
    await $(AddAdditionalEmployeePage.employeeFirstName()).setValue("John");
    await $(AddAdditionalEmployeePage.employeeLastName()).setValue("Smith");
    await click(AddAdditionalEmployeePage.submit());
    await $(ListCollectorAdditionalPage.no()).click();
    await click(ListCollectorAdditionalPage.submit());
    await click(Section3Page.submit());
    await expect(await $(HubPage.summaryItems("section-4-1")).getText()).toContain("Harry Potter");
    await expect(await $(HubPage.summaryItems("section-4-2")).getText()).toContain("Clark Kent");
    await expect(await $(HubPage.summaryItems("section-5-1")).getText()).toContain("Jane Doe");
    await expect(await $(HubPage.summaryItems("section-5-2")).getText()).toContain("John Smith");
    await click(HubPage.submit());
  });

  it("Given I have repeating sections for both supplementary and dynamic list items, When I start a repeating section for a supplementary list item, Then I see static supplementary data correctly piped in", async () => {
    await expect(await $(LengthOfEmploymentPage.questionTitle()).getText()).toContain("When did Harry Potter start working for Tesco?");
    await expect(await $(LengthOfEmploymentPage.employmentStartLegend()).getText()).toContain("Start date at Tesco");
  });

  it("Given I have validation on the start date in the repeating section, When I enter a date before the incorporation date, Then I see an error message", async () => {
    await $(LengthOfEmploymentPage.day()).setValue(1);
    await $(LengthOfEmploymentPage.month()).setValue(1);
    await $(LengthOfEmploymentPage.year()).setValue(1930);
    await click(LengthOfEmploymentPage.submit());
    await expect(await $(LengthOfEmploymentPage.singleErrorLink()).getText()).toBe("Enter a date after 26 November 1947");
  });

  it("Given I have validation on the start date in the repeating section, When I enter a date after the incorporation date, Then I see that date on the summary page for the section", async () => {
    await $(LengthOfEmploymentPage.year()).setValue(1990);
    await click(LengthOfEmploymentPage.submit());
    await expect(await $(Section4Page.lengthEmploymentQuestion()).getText()).toBe("When did Harry Potter start working for Tesco?");
    await expect(await $(Section4Page.employmentStart()).getText()).toBe("1 January 1990");
  });

  it("Given I complete the repeating section for another supplementary item, When I reach the summary page, Then I see the correct supplementary data with my answers", async () => {
    await click(Section4Page.submit());
    await click(HubPage.submit());
    await expect(await $(LengthOfEmploymentPage.questionTitle()).getText()).toContain("When did Clark Kent start working for Tesco?");
    await $(LengthOfEmploymentPage.day()).setValue(5);
    await $(LengthOfEmploymentPage.month()).setValue(6);
    await $(LengthOfEmploymentPage.year()).setValue(2011);
    await click(LengthOfEmploymentPage.submit());
    await expect(await $(Section4Page.lengthEmploymentQuestion()).getText()).toBe("When did Clark Kent start working for Tesco?");
    await expect(await $(Section4Page.employmentStart()).getText()).toBe("5 June 2011");
  });

  it("Given I move onto the dynamic list items, When I start a repeating section for a dynamic list item, Then I see static supplementary data correctly piped in and the same validation and summary", async () => {
    await click(Section4Page.submit());
    await click(HubPage.submit());
    await expect(await $(AdditionalLengthOfEmploymentPage.questionTitle()).getText()).toContain("When did Jane Doe start working for Tesco?");
    await expect(await $(AdditionalLengthOfEmploymentPage.additionalEmploymentStartLegend()).getText()).toBe("Start date at Tesco");
    await $(AdditionalLengthOfEmploymentPage.day()).setValue(1);
    await $(AdditionalLengthOfEmploymentPage.month()).setValue(1);
    await $(AdditionalLengthOfEmploymentPage.year()).setValue(1930);
    await click(AdditionalLengthOfEmploymentPage.submit());
    await expect(await $(AdditionalLengthOfEmploymentPage.singleErrorLink()).getText()).toBe("Enter a date after 26 November 1947");
    await $(AdditionalLengthOfEmploymentPage.year()).setValue(2000);
    await click(AdditionalLengthOfEmploymentPage.submit());
    await expect(await $(Section5Page.additionalLengthEmploymentQuestion()).getText()).toBe("When did Jane Doe start working for Tesco?");
    await expect(await $(Section5Page.additionalEmploymentStart()).getText()).toBe("1 January 2000");
    await click(Section5Page.submit());
    await click(HubPage.submit());
    await $(AdditionalLengthOfEmploymentPage.day()).setValue(3);
    await $(AdditionalLengthOfEmploymentPage.month()).setValue(3);
    await $(AdditionalLengthOfEmploymentPage.year()).setValue(2010);
    await click(AdditionalLengthOfEmploymentPage.submit());
    await expect(await $(Section5Page.additionalLengthEmploymentQuestion()).getText()).toBe("When did John Smith start working for Tesco?");
    await expect(await $(Section5Page.additionalEmploymentStart()).getText()).toBe("3 March 2010");
    await click(Section5Page.submit());
  });
});
