import AddressConfirmation from "../../../generated_pages/address/address-confirmation.page";
import AddressMandatory from "../../../generated_pages/address/address-block-mandatory.page";
import AddressOptional from "../../../generated_pages/address/address-block-optional.page";
import SubmitPage from "../../../generated_pages/address/submit.page";
import { click, verifyUrlContains } from "../../../helpers";

describe("Address Answer Type", () => {
  beforeEach("Launch survey", async () => {
    await browser.openQuestionnaire("test_address.json");
  });

  describe("Given the user is on an address input question", () => {
    it("When the user enters all address fields, Then the summary displays the address fields", async () => {
      await $(AddressMandatory.Line1()).setValue("Evelyn Street");
      await $(AddressMandatory.Line2()).setValue("Apt 7");
      await $(AddressMandatory.Town()).setValue("Barry");
      await $(AddressMandatory.Postcode()).setValue("CF63 4JG");

      await click(AddressMandatory.submit());
      await click(AddressOptional.submit());
      await click(AddressConfirmation.submit());
      await verifyUrlContains(SubmitPage.pageName);
      await expect(await $(SubmitPage.addressMandatory()).getText()).toBe("Evelyn Street\nApt 7\nBarry\nCF63 4JG");
      await expect(await $(SubmitPage.addressMandatory()).getHTML()).toContain("Evelyn Street<br>Apt 7<br>Barry<br>CF63 4JG");
    });
  });

  describe("Given the user is on an address input question", () => {
    it("When the user enters only address line 1, Then the summary only displays address line 1", async () => {
      await $(AddressMandatory.Line1()).setValue("Evelyn Street");

      await click(AddressMandatory.submit());
      await click(AddressOptional.submit());
      await click(AddressConfirmation.submit());
      await verifyUrlContains(SubmitPage.pageName);
      await expect(await $(SubmitPage.addressMandatory()).getText()).toBe("Evelyn Street");
    });
  });

  describe("Given the user is on an mandatory address input question", () => {
    it("When the user submits the page without entering address line 1, Then an error is displayed", async () => {
      await click(AddressMandatory.submit());
      await expect(await $(AddressMandatory.error()).getText()).toBe("Enter an address");
    });
  });

  describe("Given the user is on an optional address input question", () => {
    it("When the user submits the page without entering any fields, Then the summary should display `No answer provided`.", async () => {
      // Get to optional address question
      await $(AddressMandatory.Line1()).setValue("Evelyn Street");
      await click(AddressMandatory.submit());

      await click(AddressOptional.submit());
      await click(AddressConfirmation.submit());
      await expect(await $(SubmitPage.addressOptional()).getText()).toBe("No answer provided");
    });
  });

  describe("Given the user has submitted an address answer type question", () => {
    it("When the user revisits the address question page, Then all entered fields are filled in", async () => {
      await $(AddressMandatory.Line1()).setValue("Evelyn Street");
      await $(AddressMandatory.Line2()).setValue("Apt 7");
      await $(AddressMandatory.Town()).setValue("Barry");
      await $(AddressMandatory.Postcode()).setValue("CF63 4JG");

      await click(AddressMandatory.submit());
      await verifyUrlContains(AddressOptional.pageName);

      await browser.url(AddressMandatory.url());

      await expect(await $(AddressMandatory.Line1()).getValue()).toBe("Evelyn Street");
      await expect(await $(AddressMandatory.Line2()).getValue()).toBe("Apt 7");
      await expect(await $(AddressMandatory.Town()).getValue()).toBe("Barry");
      await expect(await $(AddressMandatory.Postcode()).getValue()).toBe("CF63 4JG");
    });
  });
  describe("Given the user has submitted an address answer type question", () => {
    it("When the user visits the address confirmation question page, Then the first line of the address is displayed", async () => {
      await $(AddressMandatory.Line1()).setValue("Evelyn Street");
      await $(AddressMandatory.Line2()).setValue("Apt 7");
      await $(AddressMandatory.Town()).setValue("Barry");
      await $(AddressMandatory.Postcode()).setValue("CF63 4JG");
      await click(AddressMandatory.submit());
      await click(AddressOptional.submit());
      await expect(await $(AddressConfirmation.questionText()).getText()).toBe("Please confirm the first line of your address is Evelyn Street");
    });
  });
});
