import DateOfBirthPage from "../generated_pages/dob_date/date-of-birth.page";
import UnderSixteenPage from "../generated_pages/dob_date/under-sixteen.page";
// import SubmitPage from "../generated_pages/dates/submit.page";

describe("Date of birth check", () => {
  beforeEach("Load the survey", () => {
    browser.openQuestionnaire("test_dob_date.json");
  });
  it("Given when i start survey, i see a date of birth page", () => {
    expect($(DateOfBirthPage.legend()).getText()).to.contain("date of birth");
  });
  it("Given when i enter date of birth less than 16 years, then on submit, you get a message of under 16 in subsequent question title", () => {
    $(DateOfBirthPage.day()).setValue(12);
    $(DateOfBirthPage.month()).setValue(4);
    $(DateOfBirthPage.year()).setValue(2021);
    $(DateOfBirthPage.submit()).click();
    expect($(UnderSixteenPage.legend()).getText()).to.contain("You are under 16!");
  });
  it("Given when i enter date of birth over 16 years, then on submit, you get a message of over 16 in subsequent question title", () => {
    $(DateOfBirthPage.day()).setValue(12);
    $(DateOfBirthPage.month()).setValue(4);
    $(DateOfBirthPage.year()).setValue(1980);
    $(DateOfBirthPage.submit()).click();
    expect($(UnderSixteenPage.legend()).getText()).to.contain("You are over 16!");
  });
});
