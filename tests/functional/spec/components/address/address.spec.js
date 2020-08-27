import Address from "../../../generated_pages/address/address-block.page";
import Summary from "../../../generated_pages/address/summary.page";

describe("Address Answer Type", () => {
  beforeEach("Launch survey", () => {
    browser.openQuestionnaire("test_address.json");
  });

  describe("Given the user is on an address input question", () => {
    it("When the user enters all address fields, Then, the summary displays the address fields", () => {
      $(Address.Line1()).setValue("Evelyn Street");
      $(Address.Line2()).setValue("Apt 7");
      $(Address.Town()).setValue("Barry");
      $(Address.Postcode()).setValue("CF63 4JG");

      $(Address.submit()).click();
      expect(browser.getUrl()).to.contain(Summary.pageName);
      expect($(Summary.address()).getText()).to.contain("Evelyn Street\nApt 7\nBarry\nCF63 4JG");
      expect($(Summary.address()).getHTML()).to.contain("Evelyn Street<br>Apt 7<br>Barry<br>CF63 4JG");
    });
  });

  describe("Given the user is on an address input question", () => {
    it("When the user enters only address line 1, Then, the summary only displays address line 1", () => {
      $(Address.Line1()).setValue("Evelyn Street");

      $(Address.submit()).click();
      expect(browser.getUrl()).to.contain(Summary.pageName);
      expect($(Summary.address()).getText()).to.contain("Evelyn Street");
    });
  });

  describe("Given the user is on an address input question", () => {
    it("When the user submits the page without entering any fields, Then, an error is displayed", () => {
      $(Address.submit()).click();
      expect($(Address.error()).getText()).to.contain("Enter an address to continue");
    });
  });

  describe("Given the user submitted an adddress answer type question", () => {
    it("When the user revisits the address question page, Then, all entered fields are filled in", () => {
      $(Address.Line1()).setValue("Evelyn Street");
      $(Address.Line2()).setValue("Apt 7");
      $(Address.Town()).setValue("Barry");
      $(Address.Postcode()).setValue("CF63 4JG");

      $(Address.submit()).click();
      expect(browser.getUrl()).to.contain(Summary.pageName);

      browser.url(Address.url());

      expect($(Address.Line1()).getValue()).to.contain("Evelyn Street");
      expect($(Address.Line2()).getValue()).to.contain("Apt 7");
      expect($(Address.Town()).getValue()).to.contain("Barry");
      expect($(Address.Postcode()).getValue()).to.contain("CF63 4JG");
    });
  });
});
