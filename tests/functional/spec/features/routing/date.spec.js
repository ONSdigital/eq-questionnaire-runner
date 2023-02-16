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
      beforeEach(async ()=> {
        await browser.openQuestionnaire("test_new_routing_date_equals.json");

        await $(await DateEqualsComparisonQuestionPage.day()).setValue(31);
        await $(await DateEqualsComparisonQuestionPage.month()).setValue(3);
        await $(await DateEqualsComparisonQuestionPage.year()).setValue(2020);
        await $(await DateEqualsComparisonQuestionPage.submit()).click();
      });

      it("When I enter the same date, Then I should be routed to the correct page", async ()=> {
        await $(await DateEqualsQuestionPage.day()).setValue(31);
        await $(await DateEqualsQuestionPage.month()).setValue(3);
        await $(await DateEqualsQuestionPage.year()).setValue(2020);
        await $(await DateEqualsQuestionPage.submit()).click();
        await expect(browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter the yesterday date, Then I should be routed to the correct page", async ()=> {
        await $(await DateEqualsQuestionPage.day()).setValue(30);
        await $(await DateEqualsQuestionPage.month()).setValue(3);
        await $(await DateEqualsQuestionPage.year()).setValue(2020);
        await $(await DateEqualsQuestionPage.submit()).click();
        await expect(browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter the tomorrow date, Then I should be routed to the correct page", async ()=> {
        await $(await DateEqualsQuestionPage.day()).setValue(1);
        await $(await DateEqualsQuestionPage.month()).setValue(4);
        await $(await DateEqualsQuestionPage.year()).setValue(2020);
        await $(await DateEqualsQuestionPage.submit()).click();
        await expect(browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter the last month date, Then I should be routed to the correct page", async ()=> {
        await $(await DateEqualsQuestionPage.day()).setValue(29);
        await $(await DateEqualsQuestionPage.month()).setValue(2);
        await $(await DateEqualsQuestionPage.year()).setValue(2020);
        await $(await DateEqualsQuestionPage.submit()).click();
        await expect(browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter the next month date, Then I should be routed to the correct page", async ()=> {
        await $(await DateEqualsQuestionPage.day()).setValue(30);
        await $(await DateEqualsQuestionPage.month()).setValue(4);
        await $(await DateEqualsQuestionPage.year()).setValue(2020);
        await $(await DateEqualsQuestionPage.submit()).click();
        await expect(browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter the last year date, Then I should be routed to the correct page", async ()=> {
        await $(await DateEqualsQuestionPage.day()).setValue(31);
        await $(await DateEqualsQuestionPage.month()).setValue(3);
        await $(await DateEqualsQuestionPage.year()).setValue(2019);
        await $(await DateEqualsQuestionPage.submit()).click();
        await expect(browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter the next year date, Then I should be routed to the correct page", async ()=> {
        await $(await DateEqualsQuestionPage.day()).setValue(31);
        await $(await DateEqualsQuestionPage.month()).setValue(3);
        await $(await DateEqualsQuestionPage.year()).setValue(2021);
        await $(await DateEqualsQuestionPage.submit()).click();
        await expect(browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter an incorrect date, Then I should be routed to the incorrect page", async ()=> {
        await $(await DateEqualsQuestionPage.day()).setValue(1);
        await $(await DateEqualsQuestionPage.month()).setValue(3);
        await $(await DateEqualsQuestionPage.year()).setValue(2020);
        await $(await DateEqualsComparisonQuestionPage.submit()).click();
        await expect(browser.getUrl()).to.contain(CorrectAnswerPage.pageName);
      });
    });
  });

  describe("Not Equals", () => {
    describe("Given I start date routing not equals survey", () => {
      beforeEach(async ()=> {
        await browser.openQuestionnaire("test_new_routing_date_not_equals.json");
      });

      it("When I enter a different date to February 2018, Then I should be routed to the correct page", async ()=> {
        await $(await DateNotEqualsQuestionPage.Month()).setValue(3);
        await $(await DateNotEqualsQuestionPage.Year()).setValue(2018);
        await $(await DateNotEqualsQuestionPage.submit()).click();

        const expectedUrl = browser.getUrl();

        await expect(expectedUrl).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter February 2018, Then I should be routed to the incorrect page", async ()=> {
        await $(await DateNotEqualsQuestionPage.Month()).setValue(2);
        await $(await DateNotEqualsQuestionPage.Year()).setValue(2018);
        await $(await DateNotEqualsQuestionPage.submit()).click();

        const expectedUrl = browser.getUrl();

        await expect(expectedUrl).to.contain(IncorrectAnswerPage.pageName);
      });
    });
  });

  describe("Greater Than", () => {
    describe("Given I start date routing greater than survey", () => {
      beforeEach(async ()=> {
        await browser.openQuestionnaire("test_new_routing_date_greater_than.json");
      });

      it("When I enter a date greater than the 1st March 2017, Then I should be routed to the correct page", async ()=> {
        await $(await DateGreaterThanQuestionPage.day()).setValue(2);
        await $(await DateGreaterThanQuestionPage.month()).setValue(3);
        await $(await DateGreaterThanQuestionPage.year()).setValue(2017);
        await $(await DateGreaterThanQuestionPage.submit()).click();

        const expectedUrl = browser.getUrl();

        await expect(expectedUrl).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter the 1st March 2017, Then I should be routed to the incorrect page", async ()=> {
        await $(await DateGreaterThanQuestionPage.day()).setValue(1);
        await $(await DateGreaterThanQuestionPage.month()).setValue(3);
        await $(await DateGreaterThanQuestionPage.year()).setValue(2017);
        await $(await DateGreaterThanQuestionPage.submit()).click();

        const expectedUrl = browser.getUrl();

        await expect(expectedUrl).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter a date less than the 1st March 2017, Then I should be routed to the incorrect page", async ()=> {
        await $(await DateGreaterThanQuestionPage.day()).setValue(28);
        await $(await DateGreaterThanQuestionPage.month()).setValue(2);
        await $(await DateGreaterThanQuestionPage.year()).setValue(2017);
        await $(await DateGreaterThanQuestionPage.submit()).click();

        const expectedUrl = browser.getUrl();

        await expect(expectedUrl).to.contain(IncorrectAnswerPage.pageName);
      });
    });
  });

  describe("Greater Than Or Equals", () => {
    describe("Given I start date routing greater than or equals survey", () => {
      beforeEach(async ()=> {
        await browser.openQuestionnaire("test_new_routing_date_greater_than_or_equals.json");
      });

      it("When I enter a date greater than 2017, Then I should be routed to the correct page", async ()=> {
        await $(await DateGreaterThanOrEqualsQuestionPage.Year()).setValue(2018);
        await $(await DateGreaterThanOrEqualsQuestionPage.submit()).click();

        const expectedUrl = browser.getUrl();

        await expect(expectedUrl).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter 2017, Then I should be routed to the correct page", async ()=> {
        await $(await DateGreaterThanOrEqualsQuestionPage.Year()).setValue(2017);
        await $(await DateGreaterThanOrEqualsQuestionPage.submit()).click();

        const expectedUrl = browser.getUrl();

        await expect(expectedUrl).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter a date less than March 2017, Then I should be routed to the incorrect page", async ()=> {
        await $(await DateGreaterThanOrEqualsQuestionPage.Year()).setValue(2016);
        await $(await DateGreaterThanOrEqualsQuestionPage.submit()).click();

        const expectedUrl = browser.getUrl();

        await expect(expectedUrl).to.contain(IncorrectAnswerPage.pageName);
      });
    });
  });

  describe("Less Than", () => {
    describe("Given I start date routing less than survey", () => {
      beforeEach(async ()=> {
        await browser.openQuestionnaire("test_new_routing_date_less_than.json");
      });

      it("When I enter a date less than today, Then I should be routed to the correct page", async ()=> {
        await $(await DateLessThanQuestionPage.day()).setValue(dayYesterday);
        await $(await DateLessThanQuestionPage.month()).setValue(monthYesterday);
        await $(await DateLessThanQuestionPage.year()).setValue(yearYesterday);
        await $(await DateLessThanQuestionPage.submit()).click();

        const browserUrl = browser.getUrl();

        await expect(browserUrl).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter a date equal to today, Then I should be routed to the incorrect page", async ()=> {
        await $(await DateLessThanQuestionPage.day()).setValue(dayToday);
        await $(await DateLessThanQuestionPage.month()).setValue(monthToday);
        await $(await DateLessThanQuestionPage.year()).setValue(yearToday);
        await $(await DateLessThanQuestionPage.submit()).click();

        const browserUrl = browser.getUrl();

        await expect(browserUrl).to.contain(IncorrectAnswerPage.pageName);
      });

      it("When I enter a date greater than today, Then I should be routed to the incorrect page", async ()=> {
        await $(await DateLessThanQuestionPage.day()).setValue(dayTomorrow);
        await $(await DateLessThanQuestionPage.month()).setValue(monthTomorrow);
        await $(await DateLessThanQuestionPage.year()).setValue(yearTomorrow);
        await $(await DateLessThanQuestionPage.submit()).click();

        const browserUrl = browser.getUrl();

        await expect(browserUrl).to.contain(IncorrectAnswerPage.pageName);
      });
    });
  });

  describe("Less Than Or Equals", () => {
    describe("Given I start date routing less than or equals survey", () => {
      beforeEach(async ()=> {
        await browser.openQuestionnaire("test_new_routing_date_less_than_or_equals.json");
      });

      it("When I enter a date less than today, Then I should be routed to the correct page", async ()=> {
        await $(await DateLessThanOrEqualsQuestionPage.day()).setValue(dayYesterday);
        await $(await DateLessThanOrEqualsQuestionPage.month()).setValue(monthYesterday);
        await $(await DateLessThanOrEqualsQuestionPage.year()).setValue(yearYesterday);
        await $(await DateLessThanOrEqualsQuestionPage.submit()).click();

        const browserUrl = browser.getUrl();

        await expect(browserUrl).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter a date equal to today, Then I should be routed to the correct page", async ()=> {
        await $(await DateLessThanOrEqualsQuestionPage.day()).setValue(dayToday);
        await $(await DateLessThanOrEqualsQuestionPage.month()).setValue(monthToday);
        await $(await DateLessThanOrEqualsQuestionPage.year()).setValue(yearToday);
        await $(await DateLessThanOrEqualsQuestionPage.submit()).click();

        const browserUrl = browser.getUrl();

        await expect(browserUrl).to.contain(CorrectAnswerPage.pageName);
      });

      it("When I enter a date greater than today, Then I should be routed to the incorrect page", async ()=> {
        await $(await DateLessThanOrEqualsQuestionPage.day()).setValue(dayTomorrow);
        await $(await DateLessThanOrEqualsQuestionPage.month()).setValue(monthTomorrow);
        await $(await DateLessThanOrEqualsQuestionPage.year()).setValue(yearTomorrow);
        await $(await DateLessThanOrEqualsQuestionPage.submit()).click();

        const browserUrl = browser.getUrl();

        await expect(browserUrl).to.contain(IncorrectAnswerPage.pageName);
      });
    });
  });
});
