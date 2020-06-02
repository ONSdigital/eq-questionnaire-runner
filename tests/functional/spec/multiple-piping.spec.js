import AddressPage from "../generated_pages/multiple_piping/what-is-your-address.page";
import TextfieldPage from "../generated_pages/multiple_piping/textfield.page";
import MultiplePipingPage from "../generated_pages/multiple_piping/piping-question.page";

describe("Piping", () => {
  const pipingSchema = "test_multiple_piping.json";

  describe("Multiple piping into question and answer", () => {
    beforeEach("load the survey", () => {
      browser.openQuestionnaire(pipingSchema);
    });

    it("Given I enter multiple fields in one question, When I navigate to the multiple piping answer, Then I should see all values piped into an answer", () => {
      $(AddressPage.addressLine1()).setValue("1 The ONS");
      $(AddressPage.townCity()).setValue("Newport");
      $(AddressPage.postcode()).setValue("NP10 8XG");
      $(AddressPage.country()).setValue("Wales");
      $(AddressPage.submit()).click();
      $(TextfieldPage.firstText()).setValue("Fireman");
      $(TextfieldPage.secondText()).setValue("Sam");
      $(TextfieldPage.submit()).click();
      expect($(MultiplePipingPage.answerAddressLabel()).getText()).to.contain("1 The ONS, Newport, NP10 8XG, Wales");
    });

    it("Given I enter values in multiple questions, When I navigate to the multiple piping question, Then I should see both values piped into the question", () => {
      $(AddressPage.addressLine1()).setValue("1 The ONS");
      $(AddressPage.submit()).click();
      $(TextfieldPage.firstText()).setValue("Fireman");
      $(TextfieldPage.secondText()).setValue("Sam");
      $(TextfieldPage.submit()).click();
      expect($(MultiplePipingPage.questionText()).getText()).to.contain("Does Fireman Sam live at 1 The ONS");
    });
  });
});
