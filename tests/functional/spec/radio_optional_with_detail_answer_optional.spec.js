import RadioNonMandatoryPage from "../generated_pages/radio_optional_with_detail_answer_optional/radio-non-mandatory.page";
import SubmitPage from "../generated_pages/radio_optional_with_detail_answer_optional/submit.page";
import { click } from "../helpers";

describe("Checkbox and Radio item descriptions", () => {
  beforeEach("load the survey", async () => {
    await browser.openQuestionnaire("test_radio_optional_with_detail_answer_optional.json");
  });

  describe("Given the user is presented with an optional radio answer with optional detail answer", () => {
    it("When no answer is provided, Then the expected answer is displayed", async () => {
      await click(RadioNonMandatoryPage.submit());
      await expect(await $(SubmitPage.radioNonMandatoryAnswer()).getText()).toContain("No answer provided");
    });

    it("When Toast is selected and no detail answer is provided, Then the expected answer is displayed", async () => {
      await $(RadioNonMandatoryPage.toast()).click();
      await click(RadioNonMandatoryPage.submit());
      await expect(await $(SubmitPage.radioNonMandatoryAnswer()).getText()).toContain("Toast");
    });

    it("When Other is selected and no detail answer is provided, Then the expected answer is displayed", async () => {
      await $(RadioNonMandatoryPage.other()).click();
      await click(RadioNonMandatoryPage.submit());
      await expect(await $(SubmitPage.radioNonMandatoryAnswer()).getText()).toContain("Other");
    });

    it("When Other is selected and detail answer is provided, Then the expected answer is displayed", async () => {
      await $(RadioNonMandatoryPage.other()).click();
      await $(RadioNonMandatoryPage.otherDetail()).setValue("Eggs");
      await click(RadioNonMandatoryPage.submit());
      await expect(await $(SubmitPage.radioNonMandatoryAnswer()).getText()).toContain("Eggs");
    });

    it("When Other is selected and detail answer is provided and the answer is changed, Then the expected answer is displayed", async () => {
      await $(RadioNonMandatoryPage.other()).click();
      await $(RadioNonMandatoryPage.otherDetail()).setValue("Eggs");
      await $(RadioNonMandatoryPage.toast()).click();
      await click(RadioNonMandatoryPage.submit());
      await expect(await $(SubmitPage.radioNonMandatoryAnswer()).getText()).toContain("Toast");
    });
  });
});
