import MobileNumberBlockPage from "../generated_pages/mobile_number/mobile-number-block.page";
import submitPage from "../generated_pages/mobile_number/submit.page";
import { click } from "../helpers";

describe("Mobile number validation", () => {
  beforeEach("Load the survey", async () => {
    await browser.openQuestionnaire("test_mobile_number.json");
  });
  it("Given I am asked to enter Mobile no, When I enter a valid mobile number with no prefix and submit, Then confirmation section is displayed with entered mobile number", async () => {
    await $(MobileNumberBlockPage.mobileNumber()).setValue(7712345678);
    await click(MobileNumberBlockPage.submit());
    await expect(await $(submitPage.mobileNumberAnswer()).getText()).toContain("7712345678");
  });
  it("Given I am asked to enter Mobile no, When I enter a valid mobile number with prefix (+44) and submit, Then confirmation section is displayed with entered mobile number", async () => {
    await $(MobileNumberBlockPage.mobileNumber()).setValue("+447712345678");
    await click(MobileNumberBlockPage.submit());
    await expect(await $(submitPage.mobileNumberAnswer()).getText()).toContain("+447712345678");
  });
  it("Given I am asked to enter Mobile no, When I enter an invalid mobile number and submit, Then an error screen with invalid number information is displayed", async () => {
    await $(MobileNumberBlockPage.mobileNumber()).setValue("12345678");
    await click(MobileNumberBlockPage.submit());
    await expect(await $("body").getText()).toContain("Enter a UK mobile number in a valid format");
  });
});
