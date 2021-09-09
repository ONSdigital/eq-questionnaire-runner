import IncorrectAnswerPage from "../../../generated_pages/new_routing_date_equals/incorrect-answer.page.js";
import CorrectAnswerPage from "../../../generated_pages/new_routing_date_equals/correct-answer.page.js";

import DateEqualsComparisonQuestionPage from "../../../generated_pages/new_routing_date_equals/comparison-date-block.page";
import DateEqualsQuestionPage from "../../../generated_pages/new_routing_date_equals/date-question.page";
import DateNotEqualsQuestionPage from "../../../generated_pages/new_routing_date_not_equals/date-question.page";
import DateGreaterThanQuestionPage from "../../../generated_pages/new_routing_date_greater_than/date-question.page";
import DateGreaterThanOrEqualsQuestionPage from "../../../generated_pages/new_routing_date_greater_than_or_equals/date-question.page";
import DateLessThanQuestionPage from "../../../generated_pages/new_routing_date_less_than/date-question.page";
import DateLessThanOrEqualsQuestionPage from "../../../generated_pages/new_routing_date_less_than_or_equals/date-question.page";

const today = new Date();
const dayToday = today.getDate(); // yesterday
const monthToday = today.getMonth() + 1; // January is 0!
const yearToday = today.getFullYear();

describe("Feature: Routing on a Date", () => {
  describe("Equals", () => {
    describe("Given I start date routing equals survey", () => {
      beforeEach(() => {
        browser.openQuestionnaire("test_new_routing_date_equals.json");

        $(DateEqualsComparisonQuestionPage.day()).setValue(31);
        $(DateEqualsComparisonQuestionPage.month()).setValue(3);
        $(DateEqualsComparisonQuestionPage.year()).setValue(2020);
        $(DateEqualsComparisonQuestionPage.submit()).click();
      });

      it("When I enter the same date, Then I should be routed to the correct page", () => {
        $(DateEqualsQuestionPage.day()).setValue(31);
        $(DateEqualsQuestionPage.month()).setValue(3);
        $(DateEqualsQuestionPage.year()).setValue(2020);
        $(DateEqualsQuestionPage.submit()).click();
        expect(browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter the yesterday date, Then I should be routed to the correct page", () => {
        $(DateEqualsQuestionPage.day()).setValue(30);
        $(DateEqualsQuestionPage.month()).setValue(3);
        $(DateEqualsQuestionPage.year()).setValue(2020);
        $(DateEqualsQuestionPage.submit()).click();
        expect(browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter the tomorrow date, Then I should be routed to the correct page", () => {
        $(DateEqualsQuestionPage.day()).setValue(1);
        $(DateEqualsQuestionPage.month()).setValue(4);
        $(DateEqualsQuestionPage.year()).setValue(2020);
        $(DateEqualsQuestionPage.submit()).click();
        expect(browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter the last month date, Then I should be routed to the correct page", () => {
        $(DateEqualsQuestionPage.day()).setValue(29);
        $(DateEqualsQuestionPage.month()).setValue(2);
        $(DateEqualsQuestionPage.year()).setValue(2020);
        $(DateEqualsQuestionPage.submit()).click();
        expect(browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter the next month date, Then I should be routed to the correct page", () => {
        $(DateEqualsQuestionPage.day()).setValue(30);
        $(DateEqualsQuestionPage.month()).setValue(4);
        $(DateEqualsQuestionPage.year()).setValue(2020);
        $(DateEqualsQuestionPage.submit()).click();
        expect(browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter the last year date, Then I should be routed to the correct page", () => {
        $(DateEqualsQuestionPage.day()).setValue(31);
        $(DateEqualsQuestionPage.month()).setValue(3);
        $(DateEqualsQuestionPage.year()).setValue(2019);
        $(DateEqualsQuestionPage.submit()).click();
        expect(browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter the next year date, Then I should be routed to the correct page", () => {
        $(DateEqualsQuestionPage.day()).setValue(31);
        $(DateEqualsQuestionPage.month()).setValue(3);
        $(DateEqualsQuestionPage.year()).setValue(2021);
        $(DateEqualsQuestionPage.submit()).click();
        expect(browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter an incorrect date, Then I should be routed to the incorrect page", () => {
        $(DateEqualsQuestionPage.day()).setValue(1);
        $(DateEqualsQuestionPage.month()).setValue(3);
        $(DateEqualsQuestionPage.year()).setValue(2020);
        $(DateEqualsComparisonQuestionPage.submit()).click();
        expect(browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });
    });
  });

  describe("Not Equals", () => {
    describe("Given I start date routing not equals survey", () => {
      beforeEach(() => {
        browser.openQuestionnaire("test_new_routing_date_not_equals.json");
      });

      it("When I enter a different date to 28/02/2018, Then I should be routed to the correct page", () => {
        $(DateNotEqualsQuestionPage.day()).setValue(27);
        $(DateNotEqualsQuestionPage.month()).setValue(2);
        $(DateNotEqualsQuestionPage.year()).setValue(2018);
        $(DateNotEqualsQuestionPage.submit()).click();

        const expectedUrl = browser.getUrl();

        expect(expectedUrl).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter 28/02/2018, Then I should be routed to the incorrect page", () => {
        $(DateNotEqualsQuestionPage.day()).setValue(28);
        $(DateNotEqualsQuestionPage.month()).setValue(2);
        $(DateNotEqualsQuestionPage.year()).setValue(2018);
        $(DateNotEqualsQuestionPage.submit()).click();

        const expectedUrl = browser.getUrl();

        expect(expectedUrl).to.contain(IncorrectAnswerPage.pageName);
      });
    });
  });

  describe("Greater Than", () => {
    describe("Given I start date routing greater than survey", () => {
      beforeEach(() => {
        browser.openQuestionnaire("test_new_routing_date_greater_than.json");
      });

      it("When I enter a date greater than the 1st March 2017, Then I should be routed to the correct page", () => {
        $(DateGreaterThanQuestionPage.day()).setValue(2);
        $(DateGreaterThanQuestionPage.month()).setValue(3);
        $(DateGreaterThanQuestionPage.year()).setValue(2017);
        $(DateGreaterThanQuestionPage.submit()).click();

        const expectedUrl = browser.getUrl();

        expect(expectedUrl).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter the 1st March 2017, Then I should be routed to the incorrect page", () => {
        $(DateGreaterThanQuestionPage.day()).setValue(1);
        $(DateGreaterThanQuestionPage.month()).setValue(3);
        $(DateGreaterThanQuestionPage.year()).setValue(2017);
        $(DateGreaterThanQuestionPage.submit()).click();

        const expectedUrl = browser.getUrl();

        expect(expectedUrl).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter a date less than the 1st March 2017, Then I should be routed to the incorrect page", () => {
        $(DateGreaterThanQuestionPage.day()).setValue(28);
        $(DateGreaterThanQuestionPage.month()).setValue(2);
        $(DateGreaterThanQuestionPage.year()).setValue(2017);
        $(DateGreaterThanQuestionPage.submit()).click();

        const expectedUrl = browser.getUrl();

        expect(expectedUrl).to.contain(IncorrectAnswerPage.pageName);
      });
    });
  });

  describe("Greater Than Or Equals", () => {
    describe("Given I start date routing greater than or equals survey", () => {
      beforeEach(() => {
        browser.openQuestionnaire("test_new_routing_date_greater_than_or_equals.json");
      });

      it("When I enter a date greater than the 1st March 2017, Then I should be routed to the correct page", () => {
        $(DateGreaterThanOrEqualsQuestionPage.day()).setValue(2);
        $(DateGreaterThanOrEqualsQuestionPage.month()).setValue(4);
        $(DateGreaterThanOrEqualsQuestionPage.year()).setValue(2017);
        $(DateGreaterThanOrEqualsQuestionPage.submit()).click();

        const expectedUrl = browser.getUrl();

        expect(expectedUrl).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter the 1st March 2017, Then I should be routed to the correct page", () => {
        $(DateGreaterThanOrEqualsQuestionPage.day()).setValue(1);
        $(DateGreaterThanOrEqualsQuestionPage.month()).setValue(3);
        $(DateGreaterThanOrEqualsQuestionPage.year()).setValue(2017);
        $(DateGreaterThanOrEqualsQuestionPage.submit()).click();

        const expectedUrl = browser.getUrl();

        expect(expectedUrl).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter a date less than the 1st March 2017, Then I should be routed to the incorrect page", () => {
        $(DateGreaterThanOrEqualsQuestionPage.day()).setValue(28);
        $(DateGreaterThanOrEqualsQuestionPage.month()).setValue(2);
        $(DateGreaterThanOrEqualsQuestionPage.year()).setValue(2017);
        $(DateGreaterThanOrEqualsQuestionPage.submit()).click();

        const expectedUrl = browser.getUrl();

        expect(expectedUrl).to.contain(IncorrectAnswerPage.pageName);
      });
    });
  });

  describe("Less Than", () => {
    describe("Given I start date routing less than survey", () => {
      beforeEach(() => {
        browser.openQuestionnaire("test_new_routing_date_less_than.json");
      });

      it("When I enter a date less than today, Then I should be routed to the correct page", () => {
        $(DateLessThanQuestionPage.day()).setValue(dayToday - 1);
        $(DateLessThanQuestionPage.month()).setValue(monthToday);
        $(DateLessThanQuestionPage.year()).setValue(yearToday);
        $(DateLessThanQuestionPage.submit()).click();

        const browserUrl = browser.getUrl();

        expect(browserUrl).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter a date equal to today, Then I should be routed to the incorrect page", () => {
        $(DateLessThanQuestionPage.day()).setValue(dayToday);
        $(DateLessThanQuestionPage.month()).setValue(monthToday);
        $(DateLessThanQuestionPage.year()).setValue(yearToday);
        $(DateLessThanQuestionPage.submit()).click();

        const browserUrl = browser.getUrl();

        expect(browserUrl).to.contain(IncorrectAnswerPage.pageName);
      });

      it("When I enter a date greater than today, Then I should be routed to the incorrect page", () => {
        $(DateLessThanQuestionPage.day()).setValue(dayToday + 1);
        $(DateLessThanQuestionPage.month()).setValue(monthToday);
        $(DateLessThanQuestionPage.year()).setValue(yearToday);
        $(DateLessThanQuestionPage.submit()).click();

        const browserUrl = browser.getUrl();

        expect(browserUrl).to.contain(IncorrectAnswerPage.pageName);
      });
    });
  });

  describe("Less Than Or Equals", () => {
    describe("Given I start date routing less than or equals survey", () => {
      beforeEach(() => {
        browser.openQuestionnaire("test_new_routing_date_less_than_or_equals.json");
      });

      it("When I enter a date less than today, Then I should be routed to the correct page", () => {
        $(DateLessThanOrEqualsQuestionPage.day()).setValue(dayToday - 1);
        $(DateLessThanOrEqualsQuestionPage.month()).setValue(monthToday);
        $(DateLessThanOrEqualsQuestionPage.year()).setValue(yearToday);
        $(DateLessThanOrEqualsQuestionPage.submit()).click();

        const browserUrl = browser.getUrl();

        expect(browserUrl).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter a date equal to today, Then I should be routed to the correct page", () => {
        $(DateLessThanOrEqualsQuestionPage.day()).setValue(dayToday);
        $(DateLessThanOrEqualsQuestionPage.month()).setValue(monthToday);
        $(DateLessThanOrEqualsQuestionPage.year()).setValue(yearToday);
        $(DateLessThanOrEqualsQuestionPage.submit()).click();

        const browserUrl = browser.getUrl();

        expect(browserUrl).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter a date greater than today, Then I should be routed to the incorrect page", () => {
        $(DateLessThanOrEqualsQuestionPage.day()).setValue(dayToday + 1);
        $(DateLessThanOrEqualsQuestionPage.month()).setValue(monthToday);
        $(DateLessThanOrEqualsQuestionPage.year()).setValue(yearToday);
        $(DateLessThanOrEqualsQuestionPage.submit()).click();

        const browserUrl = browser.getUrl();

        expect(browserUrl).to.contain(IncorrectAnswerPage.pageName);
      });
    });
  });
});
