import { expect } from "@wdio/globals";
import { getRandomString } from "../../jwt_helper";
import { waitForPageToLoad } from "../../helpers";

async function assertLaunchedQuestionPageLooksReal() {
  await waitForPageToLoad(15000);

  const main = await $("#main-content");
  await expect(await main.isExisting()).toBe(true);

  const submits = await $$('[data-qa="btn-submit"]');
  await expect(submits.length).toBeGreaterThan(0);

  const h1 = await $("h1");
  await expect(await h1.isExisting()).toBe(true);
  const h1Text = await h1.getText();
  await expect(h1Text.trim().length).toBeGreaterThan(0);
}

const DATASETS = ["203b2f9d-c500-8175-98db-86ffcfdccfa3", "3bb41d29-4daa-9520-82f0-cae365f390c6"];

const SCHEMAS = [
  "test_supplementary_data_with_introduction_and_calculated_summary.json",
  "test_supplementary_data_repeating_block_and_calculated_summary.json",
  "test_hub_section_required_with_repeat_supplementary.json",
  "test_supplementary_data.json",
];

describe("SDS smoke: open every schema with every SDS dataset", () => {
  for (const schema of SCHEMAS) {
    for (const sdsDatasetId of DATASETS) {
      it(`opens "${schema}" with SDS ${sdsDatasetId}`, async () => {
        const responseId = getRandomString(16); // fresh each time
        await browser.openQuestionnaire(schema, {
          launchVersion: "v2",
          sdsDatasetId,
          responseId,
        });

        await assertLaunchedQuestionPageLooksReal();
      });
    }
  }
});
