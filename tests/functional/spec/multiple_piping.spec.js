import AddressPage from "../generated_pages/multiple_piping/what-is-your-address.page";
import TextfieldPage from "../generated_pages/multiple_piping/textfield.page";
import MultiplePipingPage from "../generated_pages/multiple_piping/piping-question.page";
import { click } from "../helpers";

describe("Piping", () => {
  const pipingSchema = "test_multiple_piping.json";

  describe("Multiple piping into question and answer", () => {
    beforeEach("load the survey", async () => {
      await browser.openQuestionnaire(pipingSchema);
    });

    it("Given I enter multiple fields in one question, When I navigate to the multiple piping answer, Then I should see all values piped into an answer", async () => {
      await $(AddressPage.addressLine1()).setValue("1 The ONS");
      await $(AddressPage.townCity()).setValue("Newport");
      await $(AddressPage.postcode()).setValue("NP10 8XG");
      await $(AddressPage.country()).setValue("Wales");
      await click(AddressPage.submit());
      await $(TextfieldPage.firstText()).setValue("Fireman");
      await $(TextfieldPage.secondText()).setValue("Sam");
      await click(TextfieldPage.submit());
      await expect(await $(MultiplePipingPage.answerAddressLabel()).getText()).toContain("1 The ONS, Newport, NP10 8XG, Wales");
    });

    it("Given I enter values in multiple questions, When I navigate to the multiple piping question, Then I should see both values piped into the question", async () => {
      await $(AddressPage.addressLine1()).setValue("1 The ONS");
      await click(AddressPage.submit());
      await $(TextfieldPage.firstText()).setValue("Fireman");
      await $(TextfieldPage.secondText()).setValue("Sam");
      await click(TextfieldPage.submit());
      await expect(await $(MultiplePipingPage.questionText()).getText()).toContain("Does Fireman Sam live at 1 The ONS");
    });
  });
});
