import MobileNumberBlockPage from "../generated_pages/mobile_number/mobile-number-block.page";
import submitPage from "../generated_pages/mobile_number/submit.page";

describe("Mobile number validation", () => {
  beforeEach("Load the survey", () => {
    browser.openQuestionnaire("test_mobile_number.json");
  });
  it("When i enter a valid mobile number with no prefix and submit,then confirmation section is displayed with entered mobile number", () => {
    $(MobileNumberBlockPage.mobileNumber()).setValue(7712345678);
    $(MobileNumberBlockPage.submit()).click();
    expect($(submitPage.mobileNumberAnswer()).getText()).to.contain("7712345678");
  });
  it("When i enter a valid mobile number with prefix (+44) and submit,then confirmation section is displayed with entered mobile number", () => {
    $(MobileNumberBlockPage.mobileNumber()).setValue("+447712345678");
    $(MobileNumberBlockPage.submit()).click();
    expect($(submitPage.mobileNumberAnswer()).getText()).to.contain("+447712345678");
  });
  it("When i enter an invalid mobile number and submit,then an error screen with invalid number information is displayed ", () => {
    $(MobileNumberBlockPage.mobileNumber()).setValue("12345678");
    $(MobileNumberBlockPage.submit()).click();
    expect($("body").getText()).to.contain("Enter a UK mobile number in a valid format");
  });
});
