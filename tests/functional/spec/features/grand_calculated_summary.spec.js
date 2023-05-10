import { GrandCalculatedSummaryTestCase } from "./grand_calculated_summary_test_case.js";

describe("Feature: Grand Calculated Summary", () => {
  describe("Given I have a Grand Calculated Summary", () => {
    GrandCalculatedSummaryTestCase.testCrossSectionDependencies("test_grand_calculated_summary_cross_section_dependencies.json");
  });
});
