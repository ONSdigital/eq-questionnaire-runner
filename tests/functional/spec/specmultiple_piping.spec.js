import AddressPage from "../generated_pages/multiple_piping/what-is-your-address.page";
import TextfieldPage from "../generated_pages/multiple_piping/textfield.page";
import MultiplePipingPage from "../generated_pages/multiple_piping/piping-question.page";

describe("Piping", () => {
  const pipingSchema = "test_multiple_piping.json";

  describe("Multiple piping into question and answer", () => {
    beforeEach("load the survey", async ()=> {
      await browser.openQuestionnaire(pipingSchema);
    });

    it("Given I enter multiple fields in one question, When I navigate to the multiple piping answer, Then I should see all values piped into an answer", async ()=> {
      await $(await AddressPage.addressLine1()).setValue("1 The ONS");
      await $(await AddressPage.townCity()).setValue("Newport");
      await $(await AddressPage.postcode()).setValue("NP10 8XG");
      await $(await AddressPage.country()).setValue("Wales");
      await $(await AddressPage.submit()).click();
      await $(await TextfieldPage.firstText()).setValue("Fireman");
      await $(await TextfieldPage.secondText()).setValue("Sam");
      await $(await TextfieldPage.submit()).click();
      await expect(await $(await MultiplePipingPage.answerAddressLabel()).getText()).to.contain("1 The ONS, Newport, NP10 8XG, Wales");
    });

    it("Given I enter values in multiple questions, When I navigate to the multiple piping question, Then I should see both values piped into the question", async ()=> {
      await $(await AddressPage.addressLine1()).setValue("1 The ONS");
      await $(await AddressPage.submit()).click();
      await $(await TextfieldPage.firstText()).setValue("Fireman");
      await $(await TextfieldPage.secondText()).setValue("Sam");
      await $(await TextfieldPage.submit()).click();
      await expect(await $(await MultiplePipingPage.questionText()).getText()).to.contain("Does Fireman Sam live at 1 The ONS");
    });
  });
});
