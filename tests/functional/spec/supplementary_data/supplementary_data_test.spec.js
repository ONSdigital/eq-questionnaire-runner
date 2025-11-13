import { expect } from "@wdio/globals";
import { getRandomString } from "../../jwt_helper";
import { waitForPageToLoad } from "../../helpers";

const DATASETS = ["203b2f9d-c500-8175-98db-86ffcfdccfa3", "3bb41d29-4daa-9520-82f0-cae365f390c6"];

const SCHEMAS = [
  "test_supplementary_data_with_introduction_and_calculated_summary.json",
  "test_supplementary_data_repeating_block_and_calculated_summary.json",
  "test_hub_section_required_with_repeat_supplementary.json",
  "test_supplementary_data.json",
];

async function assertIntroAndCalcSummaryInterstitial() {
  await waitForPageToLoad(15000);
  const bodyText = await $("body").getText();
  await expect(bodyText).toContain("You have successfully loaded Supplementary data");
  await expect(await $$('[data-qa="btn-submit"]').length).toBeGreaterThan(0);
}

async function assertRepeatingBlockHubLanding() {
  await waitForPageToLoad(15000);
  const bodyText = await $("body").getText();
  await expect(bodyText).toContain("Product details");
}

async function assertGenericTestSupplementaryDataTitle() {
  await waitForPageToLoad(15000);
  const bodyText = await $("body").getText();
  await expect(bodyText).toContain("Test Supplementary Data");
}

function getValidatorForSchema(schema) {
  switch (schema) {
    case "test_supplementary_data_with_introduction_and_calculated_summary.json":
      return assertIntroAndCalcSummaryInterstitial;

    case "test_hub_section_required_with_repeat_supplementary.json":
      return assertIntroAndCalcSummaryInterstitial;

    case "test_supplementary_data_repeating_block_and_calculated_summary.json":
      return assertRepeatingBlockHubLanding;

    // If you later add a specific check for test_supplementary_data.json, swap it here
    case "test_supplementary_data.json":
      return assertGenericTestSupplementaryDataTitle;

    default:
      return assertGenericTestSupplementaryDataTitle;
  }
}

describe("Each schema validates its expected first page with each SDS dataset", () => {
  for (const schema of SCHEMAS) {
    for (const sdsDatasetId of DATASETS) {
      it(`opens "${schema}" with SDS ${sdsDatasetId} and passes its schema-specific check`, async () => {
        const responseId = getRandomString(16);
        await browser.openQuestionnaire(schema, {
          launchVersion: "v2",
          sdsDatasetId,
          responseId,
        });

        const validate = getValidatorForSchema(schema);
        await validate();
      });
    }
  }
});
