import DateOfBirthPage from "../generated_pages/dob_date/date-of-birth.page";
import UnderSixteenPage from "../generated_pages/dob_date/under-sixteen.page";

describe("Date of birth check", () => {
  beforeEach("Load the survey", () => {
    browser.openQuestionnaire("test_dob_date.json");
  });
  it("Given I am completing a date question, When I enter a value less than 16 years, Then I am routed to under 16 page", () => {
    $(DateOfBirthPage.day()).setValue(12);
    $(DateOfBirthPage.month()).setValue(4);
    $(DateOfBirthPage.year()).setValue(2021);
    $(DateOfBirthPage.submit()).click();
    expect($(UnderSixteenPage.legend()).getText()).to.contain("You are under 16!");
  });
  it("Given I am completing a date question, When I enter a value less than 16 years, Then I am routed to over 16 page", () => {
    $(DateOfBirthPage.day()).setValue(12);
    $(DateOfBirthPage.month()).setValue(4);
    $(DateOfBirthPage.year()).setValue(1980);
    $(DateOfBirthPage.submit()).click();
    expect($(UnderSixteenPage.legend()).getText()).to.contain("You are over 16!");
  });
});
