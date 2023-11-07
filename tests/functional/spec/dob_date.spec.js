import DateOfBirthPage from "../generated_pages/dob_date/date-of-birth.page";
import UnderSixteenPage from "../generated_pages/dob_date/under-sixteen.page";
import { click } from "../helpers";

describe("Date of birth check", () => {
  beforeEach("Load the survey", async () => {
    await browser.openQuestionnaire("test_dob_date.json");
  });
  it("Given I am completing a date question, When I enter a value less than 16 years, Then I am routed to under 16 page", async () => {
    await $(DateOfBirthPage.day()).setValue(12);
    await $(DateOfBirthPage.month()).setValue(4);
    await $(DateOfBirthPage.year()).setValue(2021);
    await click(DateOfBirthPage.submit());
    await expect(await $(UnderSixteenPage.legend()).getText()).toBe("You are under 16!");
  });
  it("Given I am completing a date question, When I enter a value less than 16 years, Then I am routed to over 16 page", async () => {
    await $(DateOfBirthPage.day()).setValue(12);
    await $(DateOfBirthPage.month()).setValue(4);
    await $(DateOfBirthPage.year()).setValue(1980);
    await click(DateOfBirthPage.submit());
    await expect(await $(UnderSixteenPage.legend()).getText()).toBe("You are over 16!");
  });
});
