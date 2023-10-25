import InsuranceAddressPage from "../../generated_pages/submit_with_summary_return_to_answer/insurance-address.page.js";
import InsuranceTypePage from "../../generated_pages/submit_with_summary_return_to_answer/insurance-type.page.js";
import PropertyDetailsSummaryPage from "../../generated_pages/submit_with_summary_return_to_answer/property-details-section-summary.page.js";
import HouseType from "../../generated_pages/submit_with_summary_return_to_answer/house-type.page.js";
import HouseholdDetailsSummaryPage from "../../generated_pages/submit_with_summary_return_to_answer/house-details-section-summary.page.js";
import SubmitPage from "../../generated_pages/submit_with_summary_return_to_answer/submit.page.js";
import AddressDurationPage from "../../generated_pages/submit_with_summary_return_to_answer/address-duration.page.js";
import NamePage from "../../generated_pages/submit_with_summary_return_to_answer/name.page.js";
import { click } from "../../helpers";
describe("Summary Anchor Scrolling", () => {
  describe("Given I start a Test Section Summary survey", () => {
    beforeEach(async () => {
      await browser.openQuestionnaire("test_submit_with_summary_return_to_answer.json");
      await click(NamePage.submit());
      await $(InsuranceTypePage.both()).click();
      await click(InsuranceTypePage.submit());
    });

    it("When I have provided an answer and click through to the next question, Then the Previous link url shouldn't contain any anchors or reference to return_to or return_to_answer_id", async () => {
      await expect(await $(InsuranceAddressPage.previous()).getAttribute("href")).not.toContain("#");
      await expect(await $(InsuranceAddressPage.previous()).getAttribute("href")).not.toContain("return_to");
      await expect(await $(InsuranceAddressPage.previous()).getAttribute("href")).not.toContain("return_to_answer_id");
    });

    it("When I reach the section summary page, Then the Change link url should contain return_to, return_to_answer_id query params", async () => {
      await click(InsuranceAddressPage.submit());
      await click(AddressDurationPage.submit());
      await expect(
        await $(PropertyDetailsSummaryPage.insuranceAddressAnswer2Edit()).getAttribute("href")
      ).toContain(
        "insurance-address/?return_to=section-summary&return_to_answer_id=insurance-address-answer2#insurance-address-answer2"
      );
    });

    it("When I reach the section summary page, Then the Change link url for a concatenated answer should contain return_to, return_to_answer_id query params", async () => {
      await click(InsuranceAddressPage.submit());
      await click(AddressDurationPage.submit());
      await expect(
        await $(PropertyDetailsSummaryPage.summaryRowState("name-question-concatenated-answer-edit")).getAttribute("href")
      ).toContain(
        "name/?return_to=section-summary&return_to_answer_id=name-question-concatenated-answer#first-name"
      );
    });

    it("When I edit an answer from the section summary page, Then the Previous link url should contain an anchor referencing the answer id of the answer I am changing", async () => {
      await click(InsuranceAddressPage.submit());
      await click(AddressDurationPage.submit());
      await $(PropertyDetailsSummaryPage.insuranceAddressAnswer2Edit()).click();
      await expect(await $(InsuranceAddressPage.previous()).getAttribute("href")).toContain("property-details-section/#insurance-address-answer2");
    });

    it("When I edit an answer from the section summary page and click the Previous link, Then the browser url should contain an anchor referencing the answer id of the answer I am changing", async () => {
      await click(InsuranceAddressPage.submit());
      await click(AddressDurationPage.submit());
      await $(PropertyDetailsSummaryPage.insuranceAddressAnswer2Edit()).click();
      await $(InsuranceAddressPage.previous()).click();
      await expect(browser).toHaveUrlContaining("property-details-section/#insurance-address-answer2");
    });

    it("When I edit an answer from the section summary page and click the Submit button, Then I am taken to the summary page and the browser url should contain an anchor referencing the answer id of the answer I am changing", async () => {
      await click(InsuranceAddressPage.submit());
      await click(AddressDurationPage.submit());
      await $(PropertyDetailsSummaryPage.insuranceAddressAnswer2Edit()).click();
      await click(InsuranceAddressPage.submit());
      await expect(browser).toHaveUrlContaining("property-details-section/#insurance-address-answer2");
    });

    it("When I am on the final summary page, Then the Change link url should contain return_to, return_to_answer_id query params", async () => {
      await click(InsuranceAddressPage.submit());
      await click(AddressDurationPage.submit());
      await click(PropertyDetailsSummaryPage.submit());
      await click(HouseType.submit());
      await click(HouseholdDetailsSummaryPage.submit());
      await $(SubmitPage.summaryShowAllButton()).click();
      await expect(await $(SubmitPage.insuranceAddressAnswer2Edit()).getAttribute("href")).toContain(
        "?return_to=final-summary&return_to_answer_id=insurance-address-answer2#insurance-address-answer2"
      );
    });

    it("When I edit an answer from the final summary page, Then the browser url contains return_to, return_to_answer_id query params", async () => {
      await click(InsuranceAddressPage.submit());
      await click(AddressDurationPage.submit());
      await click(PropertyDetailsSummaryPage.submit());
      await click(HouseType.submit());
      await click(HouseholdDetailsSummaryPage.submit());
      await $(SubmitPage.summaryShowAllButton()).click();
      await $(SubmitPage.insuranceAddressAnswer2Edit()).click();
      await expect(browser).toHaveUrlContaining(
        "?return_to=final-summary&return_to_answer_id=insurance-address-answer2#insurance-address-answer2"
      );
    });
  });
});
