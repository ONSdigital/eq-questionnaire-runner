import { expect } from "@wdio/globals";
import { getRandomString } from "../../jwt_helper";
import { clickSyncMode, click, waitForPageToLoad } from "../../helpers";
import LoadedSuccessfullyBlockPage from "../../generated_pages/hub_section_required_with_repeat_supplementary/loaded-successfully-block.page";
import IntroductionBlockPage from "../../generated_pages/hub_section_required_with_repeat_supplementary/introduction-block.page";
import HubPage from "../../base_pages/hub.page";
import ListCollectorProductsPage from "../../generated_pages/supplementary_data_repeating_block_and_calculated_summary/list-collector-products.page.js";

const DATASETS = ["203b2f9d-c500-8175-98db-86ffcfdccfa3", "3bb41d29-4daa-9520-82f0-cae365f390c6"];

const SCHEMAS = [
  "test_supplementary_data_with_introduction_and_calculated_summary.json",
  "test_supplementary_data_repeating_block_and_calculated_summary.json",
  "test_hub_section_required_with_repeat_supplementary.json",
  "test_supplementary_data.json",
];
const EXPECTED_SURNAMES_BY_DATASET = {
  "203b2f9d-c500-8175-98db-86ffcfdccfa3": "Potter, Kent",
  "3bb41d29-4daa-9520-82f0-cae365f390c6": "Potter, Wayne",
};

async function assertIntroAndCalcSummaryInterstitial(_schema, sdsDatasetId) {
  await waitForPageToLoad(15000);

  const bodyText = await $("body").getText();
  await expect(bodyText).toContain("You have successfully loaded Supplementary data");
  await expect((await $$('[data-qa="btn-submit"]')).length).toBeGreaterThan(0);

  const expectedSurnames = EXPECTED_SURNAMES_BY_DATASET[sdsDatasetId];
  const guidance = await $("#main-content #guidance-1").getText();
  await expect(guidance).toContain(`The surnames of the employees are: ${expectedSurnames}.`);

  const items = await $$("#main-content li");
  await expect(await items[0].getText()).toBe("Articles and equipment for sports or outdoor games");
  await expect(await items[1].getText()).toBe("Kitchen Equipment");
}

async function assertHubAndSpoke() {
  await waitForPageToLoad(15000);
  clickSyncMode(LoadedSuccessfullyBlockPage.submit());
  clickSyncMode(IntroductionBlockPage.submit());
}

async function assertRepeatingBlockHubLanding() {
  await waitForPageToLoad(15000);
  const bodyText = await $("body").getText();
  await expect(bodyText).toContain("Product details");
  await click(HubPage.submit());
  await expect(await $(ListCollectorProductsPage.listLabel(1)).getText()).toBe("Articles and equipment for sports or outdoor games");
  await expect(await $(ListCollectorProductsPage.listLabel(2)).getText()).toBe("Kitchen Equipment");
}

async function assertGenericTestSupplementaryDataTitle() {
  await waitForPageToLoad(15000);
  const bodyText = await $("body").getText();
  await expect(bodyText).toContain("Test Supplementary Data");
}

function getValidatorForSchema(schema, sdsDatasetId) {
  switch (schema) {
    case "test_supplementary_data_with_introduction_and_calculated_summary.json":
      return assertIntroAndCalcSummaryInterstitial;

    case "test_hub_section_required_with_repeat_supplementary.json":
      return assertHubAndSpoke;

    case "test_supplementary_data_repeating_block_and_calculated_summary.json":
      return assertRepeatingBlockHubLanding;

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
        await validate(schema, sdsDatasetId);
      });
    }
  }
});
