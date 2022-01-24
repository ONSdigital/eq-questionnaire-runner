import NamePage from "../generated_pages/language/name-block.page";
import DobPage from "../generated_pages/language/dob-block.page";
import NumberOfPeoplePage from "../generated_pages/language/number-of-people-block.page";
import ConfirmNumberOfPeoplePage from "../generated_pages/language/confirm-number-of-people.page";
import HubPage from "../base_pages/hub.page.js";

const PLURAL_TEST_DATA_SETS = [
  {
    count: 0,
    question_title: {
      en: "0 people live here, is this correct?",
      cy: "Mae 0 person yn byw yma, ydy hyn yn gywir? (zero)",
    },
    answer: {
      en: "Yes, 0 people live here",
      cy: "Ydy, mae 0 person yn byw yma (zero)",
    },
  },
  {
    count: 1,
    question_title: {
      en: "1 person lives here, is this correct?",
      cy: "Mae 1 person yn byw yma, ydy hyn yn gywir? (one)",
    },
    answer: {
      en: "Yes, 1 person lives here",
      cy: "Ydy, mae 1 person yn byw yma (one)",
    },
  },
  {
    count: 2,
    question_title: {
      en: "2 people live here, is this correct?",
      cy: "Mae 2 person yn byw yma, ydy hyn yn gywir? (two)",
    },
    answer: {
      en: "Yes, 2 people live here",
      cy: "Ydy, mae 2 person yn byw yma (two)",
    },
  },
  {
    count: 3,
    question_title: {
      en: "3 people live here, is this correct?",
      cy: "Mae 3 pherson yn byw yma, ydy hyn yn gywir? (few)",
    },
    answer: {
      en: "Yes, 3 people live here",
      cy: "Ydy, mae 3 pherson yn byw yma (few)",
    },
  },
  {
    count: 6,
    question_title: {
      en: "6 people live here, is this correct?",
      cy: "Mae 6 pherson yn byw yma, ydy hyn yn gywir? (many)",
    },
    answer: {
      en: "Yes, 6 people live here",
      cy: "Ydy, mae 6 pherson yn byw yma (many)",
    },
  },
  {
    count: 4,
    question_title: {
      en: "4 people live here, is this correct?",
      cy: "Mae 4 pherson yn byw yma, ydy hyn yn gywir? (other)",
    },
    answer: {
      en: "Yes, 4 people live here",
      cy: "Ydy, mae 4 pherson yn byw yma (other)",
    },
  },
  {
    count: 5,
    question_title: {
      en: "5 people live here, is this correct?",
      cy: "Mae 5 pherson yn byw yma, ydy hyn yn gywir? (other)",
    },
    answer: {
      en: "Yes, 5 people live here",
      cy: "Ydy, mae 5 pherson yn byw yma (other)",
    },
  },
  {
    count: 10,
    question_title: {
      en: "10 people live here, is this correct?",
      cy: "Mae 10 pherson yn byw yma, ydy hyn yn gywir? (other)",
    },
    answer: {
      en: "Yes, 10 people live here",
      cy: "Ydy, mae 10 pherson yn byw yma (other)",
    },
  },
];

describe("Language Code", () => {
  it("Given a launch language of Welsh, I should see Welsh text", () => {
    browser.openQuestionnaire("test_language.json", {
      language: "cy",
    });
    $(HubPage.submit()).click();
    expect($(NamePage.questionText()).getText()).to.contain("Rhowch enw");

    $(NamePage.firstName()).setValue("Catherine");
    $(NamePage.lastName()).setValue("Zeta-Jones");
    $(NamePage.submit()).click();

    $(DobPage.day()).setValue(25);
    $(DobPage.month()).setValue(9);
    $(DobPage.year()).setValue(1969);
    $(DobPage.submit()).click();

    $(NumberOfPeoplePage.numberOfPeople()).setValue(0);
    $(NumberOfPeoplePage.submit()).click();
    $(ConfirmNumberOfPeoplePage.yes()).click();
    $(ConfirmNumberOfPeoplePage.submit()).click();

    expect($(HubPage.heading()).getText()).to.contain("Teitl cyflwyno");
    expect($(HubPage.warning()).getText()).to.contain("Rhybudd cyflwyno");
    expect($(HubPage.guidance()).getText()).to.contain("Canllawiau cyflwyno");
    expect($(HubPage.submit()).getText()).to.contain("Botwm cyflwyno");
    $(HubPage.submit()).click();

    expect(browser.getUrl()).to.contain("thank-you");
  });

  it("Given a launch language of English, I should see English text", () => {
    browser.openQuestionnaire("test_language.json", {
      language: "en",
    });

    $(HubPage.submit()).click();
    expect($(NamePage.questionText()).getText()).to.contain("Please enter a name");
    $(NamePage.firstName()).setValue("Catherine");
    $(NamePage.lastName()).setValue("Zeta-Jones");
    $(NamePage.submit()).click();

    $(DobPage.day()).setValue(25);
    $(DobPage.month()).setValue(9);
    $(DobPage.year()).setValue(1969);
    $(DobPage.submit()).click();

    $(NumberOfPeoplePage.numberOfPeople()).setValue(0);
    $(NumberOfPeoplePage.submit()).click();
    $(ConfirmNumberOfPeoplePage.yes()).click();
    $(ConfirmNumberOfPeoplePage.submit()).click();

    expect($(HubPage.heading()).getText()).to.contain("Submission title");
    expect($(HubPage.warning()).getText()).to.contain("Submission warning");
    expect($(HubPage.guidance()).getText()).to.contain("Submission guidance");
    expect($(HubPage.submit()).getText()).to.contain("Submission button");
    $(HubPage.submit()).click();

    expect(browser.getUrl()).to.contain("thank-you");
  });

  it("Given a launch language of English, When I select Cymraeg, Then the language should be switched to Welsh", () => {
    browser.openQuestionnaire("test_language.json", {
      language: "en",
    });

    $(HubPage.submit()).click();
    expect($(NamePage.questionText()).getText()).to.contain("Please enter a name");
    $(NamePage.switchLanguage("cy")).click();
    expect($(NamePage.questionText()).getText()).to.contain("Rhowch enw");
    $(NamePage.switchLanguage("en")).click();

    $(NamePage.firstName()).setValue("Catherine");
    $(NamePage.lastName()).setValue("Zeta-Jones");
    $(NamePage.submit()).click();

    $(DobPage.day()).setValue(25);
    $(DobPage.month()).setValue(9);
    $(DobPage.year()).setValue(1969);
    $(DobPage.submit()).click();

    $(NumberOfPeoplePage.numberOfPeople()).setValue(0);
    $(NumberOfPeoplePage.submit()).click();
    $(ConfirmNumberOfPeoplePage.yes()).click();
    $(ConfirmNumberOfPeoplePage.submit()).click();

    expect($(HubPage.heading()).getText()).to.contain("Submission title");
    expect($(HubPage.warning()).getText()).to.contain("Submission warning");
    expect($(HubPage.guidance()).getText()).to.contain("Submission guidance");
    expect($(HubPage.submit()).getText()).to.contain("Submission button");
    $(HubPage.switchLanguage("cy")).click();
    expect($(HubPage.heading()).getText()).to.contain("Teitl cyflwyno");
    expect($(HubPage.warning()).getText()).to.contain("Rhybudd cyflwyno");
    expect($(HubPage.guidance()).getText()).to.contain("Canllawiau cyflwyno");
    expect($(HubPage.submit()).getText()).to.contain("Botwm cyflwyno");
    $(HubPage.submit()).click();

    expect(browser.getUrl()).to.contain("thank-you");
  });

  it("Given a launch language of Welsh, When I select English, Then the language should be switched to English", () => {
    browser.openQuestionnaire("test_language.json", {
      language: "cy",
    });

    $(HubPage.submit()).click();
    expect($(NamePage.questionText()).getText()).to.contain("Rhowch enw");
    $(NamePage.switchLanguage("en")).click();
    expect($(NamePage.questionText()).getText()).to.contain("Please enter a name");
  });

  describe("Given a launch language of English and a question with plural forms, When I select switch languages, Then the plural forms are displayed correctly for the chosen language", () => {
    for (const dataSet of PLURAL_TEST_DATA_SETS) {
      const numberOfPeople = dataSet.count;

      it(`Test plural count: ${numberOfPeople}`, () => {
        browser.openQuestionnaire("test_language.json", {
          language: "en",
        });

        $(HubPage.submit()).click();
        expect($(NamePage.questionText()).getText()).to.contain("Please enter a name");
        $(NamePage.firstName()).setValue("Catherine");
        $(NamePage.lastName()).setValue("Zeta-Jones");
        $(NamePage.submit()).click();

        $(DobPage.day()).setValue(25);
        $(DobPage.month()).setValue(9);
        $(DobPage.year()).setValue(1969);
        $(DobPage.submit()).click();

        $(NumberOfPeoplePage.numberOfPeople()).setValue(numberOfPeople);
        $(NumberOfPeoplePage.submit()).click();

        expect($(ConfirmNumberOfPeoplePage.questionText()).getText()).to.contain(dataSet.question_title.en);
        expect($(ConfirmNumberOfPeoplePage.yesLabel()).getText()).to.contain(dataSet.answer.en);

        $(ConfirmNumberOfPeoplePage.switchLanguage("cy")).click();

        expect($(ConfirmNumberOfPeoplePage.questionText()).getText()).to.contain(dataSet.question_title.cy);
        expect($(ConfirmNumberOfPeoplePage.yesLabel()).getText()).to.contain(dataSet.answer.cy);

        $(ConfirmNumberOfPeoplePage.yes()).click();
        $(ConfirmNumberOfPeoplePage.submit()).click();
      });
    }
  });
});
