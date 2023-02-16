import DateOfBirthPage from "../generated_pages/dob_date/date-of-birth.page";
import UnderSixteenPage from "../generated_pages/dob_date/under-sixteen.page";

describe("Date of birth check", () => {
  beforeEach("Load the survey", async ()=> {
    await browser.openQuestionnaire("test_dob_date.json");
  });
  it("Given I am completing a date question, When I enter a value less than 16 years, Then I am routed to under 16 page", async ()=> {
    await $(await DateOfBirthPage.day()).setValue(12);
    await $(await DateOfBirthPage.month()).setValue(4);
    await $(await DateOfBirthPage.year()).setValue(2021);
    await $(await DateOfBirthPage.submit()).click();
    await expect(await $(await UnderSixteenPage.legend()).getText()).to.contain("You are under 16!");
  });
  it("Given I am completing a date question, When I enter a value less than 16 years, Then I am routed to over 16 page", async ()=> {
    await $(await DateOfBirthPage.day()).setValue(12);
    await $(await DateOfBirthPage.month()).setValue(4);
    await $(await DateOfBirthPage.year()).setValue(1980);
    await $(await DateOfBirthPage.submit()).click();
    await expect(await $(await UnderSixteenPage.legend()).getText()).to.contain("You are over 16!");
  });
});
