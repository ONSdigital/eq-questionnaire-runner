import { CalculatedSummaryTestCase } from "./calculated_summary_test_case.js";

describe("Feature: Calculated Summary", () => {
  describe("Given I have a Calculated Summary", () => {
    CalculatedSummaryTestCase.testCase("test_calculated_summary.json");
  });
  describe("Given I have a Calculated Summary with the new format", () => {
    CalculatedSummaryTestCase.testCase("test_new_calculated_summary.json");
  });

  describe("Given I have a Calculated Summary", () => {
    CalculatedSummaryTestCase.testCrossSectionDependencies("test_calculated_summary_cross_section_dependencies.json");
  });
  describe("Given I have a Calculated Summary with the new format", () => {
    CalculatedSummaryTestCase.testCrossSectionDependencies("test_new_calculated_summary_cross_section_dependencies.json");
  });
});
