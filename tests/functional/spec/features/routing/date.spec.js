import IncorrectAnswerPage from "../../../generated_pages/routing_date_equals/incorrect-answer.page.js";
import CorrectAnswerPage from "../../../generated_pages/routing_date_equals/correct-answer.page.js";

import DateEqualsComparisonQuestionPage from "../../../generated_pages/routing_date_equals/comparison-date-block.page";
import DateEqualsQuestionPage from "../../../generated_pages/routing_date_equals/date-question.page";
import DateNotEqualsQuestionPage from "../../../generated_pages/routing_date_not_equals/date-question.page";
import DateGreaterThanQuestionPage from "../../../generated_pages/routing_date_greater_than/date-question.page";
import DateLessThanQuestionPage from "../../../generated_pages/routing_date_less_than/date-question.page";

describe("Feature: Routing on a Date", () => {
  describe("Equals", () => {
    describe("Given I start date routing equals survey", () => {
      beforeEach(() => {
        browser.openQuestionnaire("test_routing_date_equals.json");

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
        browser.openQuestionnaire("test_routing_date_not_equals.json");
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
        browser.openQuestionnaire("test_routing_date_greater_than.json");
      });

      it("When I enter a date greater than March 2017, Then I should be routed to the correct page", () => {
        $(DateGreaterThanQuestionPage.Month()).setValue(4);
        $(DateGreaterThanQuestionPage.Year()).setValue(2017);
        $(DateGreaterThanQuestionPage.submit()).click();

        const expectedUrl = browser.getUrl();

        expect(expectedUrl).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter a date less than or equal to March 2017, Then I should be routed to the incorrect page", () => {
        $(DateGreaterThanQuestionPage.Month()).setValue(3);
        $(DateGreaterThanQuestionPage.Year()).setValue(2017);
        $(DateGreaterThanQuestionPage.submit()).click();

        const expectedUrl = browser.getUrl();

        expect(expectedUrl).to.contain(IncorrectAnswerPage.pageName);
      });
    });
  });

  describe("Less Than", () => {
    describe("Given I start date routing less than survey", () => {
      // TODAY
      const today = new Date();

      // YESTERDAY
      const yesterday = new Date(today);
      yesterday.setDate(today.getDate() - 1);

      const dayYesterday = yesterday.getDate(); // yesterday
      const monthYesterday = yesterday.getMonth() + 1; // January is 0!
      const yearYesterday = yesterday.getFullYear();

      beforeEach(() => {
        browser.openQuestionnaire("test_routing_date_less_than.json");
      });

      it("When I enter a date less than today, Then I should be routed to the correct page", () => {
        $(DateLessThanQuestionPage.day()).setValue(dayYesterday);
        $(DateLessThanQuestionPage.month()).setValue(monthYesterday);
        $(DateLessThanQuestionPage.year()).setValue(yearYesterday);
        $(DateLessThanQuestionPage.submit()).click();

        const browserUrl = browser.getUrl();

        expect(browserUrl).to.contain(CorrectAnswerPage.pageName);
      });
    });
  });
});
