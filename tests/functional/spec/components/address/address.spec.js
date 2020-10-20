import AddressConfirmation from "../../../generated_pages/address/address-confirmation.page";
import AddressMandatory from "../../../generated_pages/address/address-block-mandatory.page";
import AddressOptional from "../../../generated_pages/address/address-block-optional.page";
import Summary from "../../../generated_pages/address/summary.page";

describe("Address Answer Type", () => {
  beforeEach("Launch survey", () => {
    browser.openQuestionnaire("test_address.json");
  });

  describe("Given the user is on an address input question", () => {
    it("When the user enters all address fields, Then the summary displays the address fields", () => {
      $(AddressMandatory.Line1()).setValue("Evelyn Street");
      $(AddressMandatory.Line2()).setValue("Apt 7");
      $(AddressMandatory.Town()).setValue("Barry");
      $(AddressMandatory.Postcode()).setValue("CF63 4JG");

      $(AddressMandatory.submit()).click();
      $(AddressOptional.submit()).click();
      $(AddressConfirmation.submit()).click();
      expect(browser.getUrl()).to.contain(Summary.pageName);
      expect($(Summary.addressMandatory()).getText()).to.equal("Evelyn Street\nApt 7\nBarry\nCF63 4JG");
      expect($(Summary.addressMandatory()).getHTML()).to.contain("Evelyn Street<br>Apt 7<br>Barry<br>CF63 4JG");
    });
  });

  describe("Given the user is on an address input question", () => {
    it("When the user enters only address line 1, Then the summary only displays address line 1", () => {
      $(AddressMandatory.Line1()).setValue("Evelyn Street");

      $(AddressMandatory.submit()).click();
      $(AddressOptional.submit()).click();
      $(AddressConfirmation.submit()).click();
      expect(browser.getUrl()).to.contain(Summary.pageName);
      expect($(Summary.addressMandatory()).getText()).to.equal("Evelyn Street");
    });
  });

  describe("Given the user is on an mandatory address input question", () => {
    it("When the user submits the page without entering address line 1, Then an error is displayed", () => {
      $(AddressMandatory.submit()).click();
      expect($(AddressMandatory.error()).getText()).to.equal("Enter an address");
    });
  });

  describe("Given the user is on an optional address input question", () => {
    it("When the user submits the page without entering any fields, Then the summary should display `No answer provided`.", () => {
      // Get to optional address question
      $(AddressMandatory.Line1()).setValue("Evelyn Street");
      $(AddressMandatory.submit()).click();

      $(AddressOptional.submit()).click();
      $(AddressConfirmation.submit()).click();
      expect($(Summary.addressOptional()).getText()).to.equal("No answer provided");
    });
  });

  describe("Given the user has submitted an address answer type question", () => {
    it("When the user revisits the address question page, Then all entered fields are filled in", () => {
      $(AddressMandatory.Line1()).setValue("Evelyn Street");
      $(AddressMandatory.Line2()).setValue("Apt 7");
      $(AddressMandatory.Town()).setValue("Barry");
      $(AddressMandatory.Postcode()).setValue("CF63 4JG");

      $(AddressMandatory.submit()).click();
      expect(browser.getUrl()).to.contain(AddressOptional.pageName);

      browser.url(AddressMandatory.url());

      expect($(AddressMandatory.Line1()).getValue()).to.contain("Evelyn Street");
      expect($(AddressMandatory.Line2()).getValue()).to.contain("Apt 7");
      expect($(AddressMandatory.Town()).getValue()).to.contain("Barry");
      expect($(AddressMandatory.Postcode()).getValue()).to.contain("CF63 4JG");
    });
  });
  describe("Given the user has submitted an address answer type question", () => {
    it("When the user visits the address confirmation question page, Then the first line of the address is displayed", () => {
      $(AddressMandatory.Line1()).setValue("Evelyn Street");
      $(AddressMandatory.Line2()).setValue("Apt 7");
      $(AddressMandatory.Town()).setValue("Barry");
      $(AddressMandatory.Postcode()).setValue("CF63 4JG");
      $(AddressMandatory.submit()).click();
      $(AddressOptional.submit()).click();
      expect($(AddressConfirmation.questionText()).getText()).to.equal("Please confirm the first line of your address is Evelyn Street");
    });
  });
});
