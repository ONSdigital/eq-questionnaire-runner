import IncorrectAnswerPage from "../../../generated_pages/routing_date_equals/incorrect-answer.page.js";
import CorrectAnswerPage from "../../../generated_pages/routing_date_equals/correct-answer.page.js";

import DateEqualsComparisonQuestionPage from "../../../generated_pages/routing_date_equals/comparison-date-block.page";
import DateEqualsQuestionPage from "../../../generated_pages/routing_date_equals/date-question.page";
import DateNotEqualsQuestionPage from "../../../generated_pages/routing_date_not_equals/date-question.page";
import DateGreaterThanQuestionPage from "../../../generated_pages/routing_date_greater_than/date-question.page";
import DateGreaterThanOrEqualsQuestionPage from "../../../generated_pages/routing_date_greater_than_or_equals/date-question.page";
import DateLessThanQuestionPage from "../../../generated_pages/routing_date_less_than/date-question.page";
import DateLessThanOrEqualsQuestionPage from "../../../generated_pages/routing_date_less_than_or_equals/date-question.page";
import { click, verifyUrlContains } from "../../../helpers";
const today = new Date();
const dayToday = today.getDate();
const monthToday = today.getMonth() + 1; // January is 0!
const yearToday = today.getFullYear();

const yesterday = new Date();
yesterday.setDate(today.getDate() - 1);
const dayYesterday = yesterday.getDate();
const monthYesterday = yesterday.getMonth() + 1;
const yearYesterday = yesterday.getFullYear();

const tomorrow = new Date();
tomorrow.setDate(today.getDate() + 1);
const dayTomorrow = tomorrow.getDate();
const monthTomorrow = tomorrow.getMonth() + 1;
const yearTomorrow = tomorrow.getFullYear();

describe("Feature: Routing on a Date", () => {
  describe("Equals", () => {
    describe("Given I start date routing equals survey", () => {
      beforeEach(async () => {
        await browser.openQuestionnaire("test_routing_date_equals.json");
        await $(DateEqualsComparisonQuestionPage.day()).setValue(31);
        await $(DateEqualsComparisonQuestionPage.month()).setValue(3);
        await $(DateEqualsComparisonQuestionPage.year()).setValue(2020);
        await click(DateEqualsComparisonQuestionPage.submit());
      });

      it("When I enter the same date, Then I should be routed to the correct page", async () => {
        await $(DateEqualsQuestionPage.day()).setValue(31);
        await $(DateEqualsQuestionPage.month()).setValue(3);
        await $(DateEqualsQuestionPage.year()).setValue(2020);
        await click(DateEqualsQuestionPage.submit());
        await verifyUrlContains(CorrectAnswerPage.pageName);
      });

      it("When I enter the yesterday date, Then I should be routed to the correct page", async () => {
        await $(DateEqualsQuestionPage.day()).setValue(30);
        await $(DateEqualsQuestionPage.month()).setValue(3);
        await $(DateEqualsQuestionPage.year()).setValue(2020);
        await click(DateEqualsQuestionPage.submit());
        await verifyUrlContains(CorrectAnswerPage.pageName);
      });

      it("When I enter the tomorrow date, Then I should be routed to the correct page", async () => {
        await $(DateEqualsQuestionPage.day()).setValue(1);
        await $(DateEqualsQuestionPage.month()).setValue(4);
        await $(DateEqualsQuestionPage.year()).setValue(2020);
        await click(DateEqualsQuestionPage.submit());
        await verifyUrlContains(CorrectAnswerPage.pageName);
      });

      it("When I enter the last month date, Then I should be routed to the correct page", async () => {
        await $(DateEqualsQuestionPage.day()).setValue(29);
        await $(DateEqualsQuestionPage.month()).setValue(2);
        await $(DateEqualsQuestionPage.year()).setValue(2020);
        await click(DateEqualsQuestionPage.submit());
        await verifyUrlContains(CorrectAnswerPage.pageName);
      });

      it("When I enter the next month date, Then I should be routed to the correct page", async () => {
        await $(DateEqualsQuestionPage.day()).setValue(30);
        await $(DateEqualsQuestionPage.month()).setValue(4);
        await $(DateEqualsQuestionPage.year()).setValue(2020);
        await click(DateEqualsQuestionPage.submit());
        await verifyUrlContains(CorrectAnswerPage.pageName);
      });

      it("When I enter the last year date, Then I should be routed to the correct page", async () => {
        await $(DateEqualsQuestionPage.day()).setValue(31);
        await $(DateEqualsQuestionPage.month()).setValue(3);
        await $(DateEqualsQuestionPage.year()).setValue(2019);
        await click(DateEqualsQuestionPage.submit());
        await verifyUrlContains(CorrectAnswerPage.pageName);
      });

      it("When I enter the next year date, Then I should be routed to the correct page", async () => {
        await $(DateEqualsQuestionPage.day()).setValue(31);
        await $(DateEqualsQuestionPage.month()).setValue(3);
        await $(DateEqualsQuestionPage.year()).setValue(2021);
        await click(DateEqualsQuestionPage.submit());
        await verifyUrlContains(CorrectAnswerPage.pageName);
      });

      it("When I enter an incorrect date, Then I should be routed to the incorrect page", async () => {
        await $(DateEqualsQuestionPage.day()).setValue(1);
        await $(DateEqualsQuestionPage.month()).setValue(3);
        await $(DateEqualsQuestionPage.year()).setValue(2020);
        await click(DateEqualsComparisonQuestionPage.submit());
        await verifyUrlContains(CorrectAnswerPage.pageName);
      });
    });
  });

  describe("Not Equals", () => {
    describe("Given I start date routing not equals survey", () => {
      beforeEach(async () => {
        await browser.openQuestionnaire("test_routing_date_not_equals.json");
      });

      it("When I enter a different date to February 2018, Then I should be routed to the correct page", async () => {
        await $(DateNotEqualsQuestionPage.Month()).setValue(3);
        await $(DateNotEqualsQuestionPage.Year()).setValue(2018);
        await click(DateNotEqualsQuestionPage.submit());

        await verifyUrlContains(CorrectAnswerPage.pageName);
      });

      it("When I enter February 2018, Then I should be routed to the incorrect page", async () => {
        await $(DateNotEqualsQuestionPage.Month()).setValue(2);
        await $(DateNotEqualsQuestionPage.Year()).setValue(2018);
        await click(DateNotEqualsQuestionPage.submit());
        await verifyUrlContains(IncorrectAnswerPage.pageName);
      });
    });
  });

  describe("Greater Than", () => {
    describe("Given I start date routing greater than survey", () => {
      beforeEach(async () => {
        await browser.openQuestionnaire("test_routing_date_greater_than.json");
      });

      it("When I enter a date greater than the 1st March 2017, Then I should be routed to the correct page", async () => {
        await $(DateGreaterThanQuestionPage.day()).setValue(2);
        await $(DateGreaterThanQuestionPage.month()).setValue(3);
        await $(DateGreaterThanQuestionPage.year()).setValue(2017);
        await click(DateGreaterThanQuestionPage.submit());
        await verifyUrlContains(CorrectAnswerPage.pageName);
      });

      it("When I enter the 1st March 2017, Then I should be routed to the incorrect page", async () => {
        await $(DateGreaterThanQuestionPage.day()).setValue(1);
        await $(DateGreaterThanQuestionPage.month()).setValue(3);
        await $(DateGreaterThanQuestionPage.year()).setValue(2017);
        await click(DateGreaterThanQuestionPage.submit());
        await verifyUrlContains(CorrectAnswerPage.pageName);
      });

      it("When I enter a date less than the 1st March 2017, Then I should be routed to the incorrect page", async () => {
        await $(DateGreaterThanQuestionPage.day()).setValue(28);
        await $(DateGreaterThanQuestionPage.month()).setValue(2);
        await $(DateGreaterThanQuestionPage.year()).setValue(2017);
        await click(DateGreaterThanQuestionPage.submit());
        await verifyUrlContains(IncorrectAnswerPage.pageName);
      });
    });
  });

  describe("Greater Than Or Equals", () => {
    describe("Given I start date routing greater than or equals survey", () => {
      beforeEach(async () => {
        await browser.openQuestionnaire("test_routing_date_greater_than_or_equals.json");
      });

      it("When I enter a date greater than 2017, Then I should be routed to the correct page", async () => {
        await $(DateGreaterThanOrEqualsQuestionPage.Year()).setValue(2018);
        await click(DateGreaterThanOrEqualsQuestionPage.submit());
        await verifyUrlContains(CorrectAnswerPage.pageName);
      });

      it("When I enter 2017, Then I should be routed to the correct page", async () => {
        await $(DateGreaterThanOrEqualsQuestionPage.Year()).setValue(2017);
        await click(DateGreaterThanOrEqualsQuestionPage.submit());
        await verifyUrlContains(CorrectAnswerPage.pageName);
      });

      it("When I enter a date less than March 2017, Then I should be routed to the incorrect page", async () => {
        await $(DateGreaterThanOrEqualsQuestionPage.Year()).setValue(2016);
        await click(DateGreaterThanOrEqualsQuestionPage.submit());
        await verifyUrlContains(IncorrectAnswerPage.pageName);
      });
    });
  });

  describe("Less Than", () => {
    describe("Given I start date routing less than survey", () => {
      beforeEach(async () => {
        await browser.openQuestionnaire("test_routing_date_less_than.json");
      });

      it("When I enter a date less than today, Then I should be routed to the correct page", async () => {
        await $(DateLessThanQuestionPage.day()).setValue(dayYesterday);
        await $(DateLessThanQuestionPage.month()).setValue(monthYesterday);
        await $(DateLessThanQuestionPage.year()).setValue(yearYesterday);
        await click(DateLessThanQuestionPage.submit());
        await verifyUrlContains(CorrectAnswerPage.pageName);
      });

      it("When I enter a date equal to today, Then I should be routed to the incorrect page", async () => {
        await $(DateLessThanQuestionPage.day()).setValue(dayToday);
        await $(DateLessThanQuestionPage.month()).setValue(monthToday);
        await $(DateLessThanQuestionPage.year()).setValue(yearToday);
        await click(DateLessThanQuestionPage.submit());
        await verifyUrlContains(IncorrectAnswerPage.pageName);
      });

      it("When I enter a date greater than today, Then I should be routed to the incorrect page", async () => {
        await $(DateLessThanQuestionPage.day()).setValue(dayTomorrow);
        await $(DateLessThanQuestionPage.month()).setValue(monthTomorrow);
        await $(DateLessThanQuestionPage.year()).setValue(yearTomorrow);
        await click(DateLessThanQuestionPage.submit());
        await verifyUrlContains(IncorrectAnswerPage.pageName);
      });
    });
  });

  describe("Less Than Or Equals", () => {
    describe("Given I start date routing less than or equals survey", () => {
      beforeEach(async () => {
        await browser.openQuestionnaire("test_routing_date_less_than_or_equals.json");
      });

      it("When I enter a date less than today, Then I should be routed to the correct page", async () => {
        await $(DateLessThanOrEqualsQuestionPage.day()).setValue(dayYesterday);
        await $(DateLessThanOrEqualsQuestionPage.month()).setValue(monthYesterday);
        await $(DateLessThanOrEqualsQuestionPage.year()).setValue(yearYesterday);
        await click(DateLessThanOrEqualsQuestionPage.submit());
        await verifyUrlContains(CorrectAnswerPage.pageName);
      });

      it("When I enter a date equal to today, Then I should be routed to the correct page", async () => {
        await $(DateLessThanOrEqualsQuestionPage.day()).setValue(dayToday);
        await $(DateLessThanOrEqualsQuestionPage.month()).setValue(monthToday);
        await $(DateLessThanOrEqualsQuestionPage.year()).setValue(yearToday);
        await click(DateLessThanOrEqualsQuestionPage.submit());
        await verifyUrlContains(CorrectAnswerPage.pageName);
      });

      it("When I enter a date greater than today, Then I should be routed to the incorrect page", async () => {
        await $(DateLessThanOrEqualsQuestionPage.day()).setValue(dayTomorrow);
        await $(DateLessThanOrEqualsQuestionPage.month()).setValue(monthTomorrow);
        await $(DateLessThanOrEqualsQuestionPage.year()).setValue(yearTomorrow);
        await click(DateLessThanOrEqualsQuestionPage.submit());
        await verifyUrlContains(IncorrectAnswerPage.pageName);
      });
    });
  });
});
