import CheckboxBlockPage from "../generated_pages/radio_checkbox_descriptions/checkbox-block.page";
import RadioBlockPage from "../generated_pages/radio_checkbox_descriptions/radio-block.page";
import { click } from "../helpers";

describe("Checkbox and Radio item descriptions", () => {
  describe("Given the user is presented with radio or checkbox options", () => {
    before("Launch survey", async () => {
      await browser.openQuestionnaire("test_radio_checkbox_descriptions.json");
    });

    it("When the schema defines a description for a checkbox option, then that description is displayed", async () => {
      await expect(
        await $(CheckboxBlockPage.newMethodsOfOrganisingExternalRelationshipsWithOtherFirmsOrPublicInstitutionsLabelDescription()).getText(),
      ).to.contain("For example first use of alliances, partnerships, outsourcing or sub-contracting");
    });

    it("When the schema defines a description for a radio option, then that description is displayed", async () => {
      await $(CheckboxBlockPage.newBusinessPracticesForOrganisingProcedures()).click();
      await click(CheckboxBlockPage.submit());
      await expect(
        await $(RadioBlockPage.newMethodsOfOrganisingExternalRelationshipsWithOtherFirmsOrPublicInstitutionsLabelDescription()).getText(),
      ).to.contain("For example first use of alliances, partnerships, outsourcing or sub-contracting");
    });
  });
});
