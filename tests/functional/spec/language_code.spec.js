const NamePage = require('../generated_pages/language/name-block.page');
const DobPage = require('../generated_pages/language/dob-block.page');
const NumberOfPeoplePage = require('../generated_pages/language/number-of-people-block.page');
const ConfirmNumberOfPeoplePage = require('../generated_pages/language/confirm-number-of-people.page');
const SummaryPage = require('../generated_pages/language/summary.page');
const ThankYouPage = require('../base_pages/thank-you.page.js');

const PLURAL_TEST_DATA_SETS = [
  {
    count: 0,
    question_title: {
      en: '0 people live here, is this correct?',
      cy: 'Mae 0 person yn byw yma, ydy hyn yn gywir? (zero)',
    },
    answer: {
      en: 'Yes, 0 people live here',
      cy: 'Ydy, mae 0 person yn byw yma (zero)',
    },
  },
  {
    count: 1,
    question_title: {
      en: '1 person lives here, is this correct?',
      cy: 'Mae 1 person yn byw yma, ydy hyn yn gywir? (one)',
    },
    answer: {
      en: 'Yes, 1 person lives here',
      cy: 'Ydy, mae 1 person yn byw yma (one)',
    },
  },
  {
    count: 2,
    question_title: {
      en: '2 people live here, is this correct?',
      cy: 'Mae 2 person yn byw yma, ydy hyn yn gywir? (two)',
    },
    answer: {
      en: 'Yes, 2 people live here',
      cy: 'Ydy, mae 2 person yn byw yma (two)',
    },
  },
  {
    count: 3,
    question_title: {
      en: '3 people live here, is this correct?',
      cy: 'Mae 3 pherson yn byw yma, ydy hyn yn gywir? (few)',
    },
    answer: {
      en: 'Yes, 3 people live here',
      cy: 'Ydy, mae 3 pherson yn byw yma (few)',
    },
  },
  {
    count: 6,
    question_title: {
      en: '6 people live here, is this correct?',
      cy: 'Mae 6 pherson yn byw yma, ydy hyn yn gywir? (many)',
    },
    answer: {
      en: 'Yes, 6 people live here',
      cy: 'Ydy, mae 6 pherson yn byw yma (many)',
    },
  },
  {
    count: 4,
    question_title: {
      en: '4 people live here, is this correct?',
      cy: 'Mae 4 pherson yn byw yma, ydy hyn yn gywir? (other)',
    },
    answer: {
      en: 'Yes, 4 people live here',
      cy: 'Ydy, mae 4 pherson yn byw yma (other)',
    },
  },
  {
    count: 5,
    question_title: {
      en: '5 people live here, is this correct?',
      cy: 'Mae 5 pherson yn byw yma, ydy hyn yn gywir? (other)',
    },
    answer: {
      en: 'Yes, 5 people live here',
      cy: 'Ydy, mae 5 pherson yn byw yma (other)',
    },
  },
  {
    count: 10,
    question_title: {
      en: '10 people live here, is this correct?',
      cy: 'Mae 10 pherson yn byw yma, ydy hyn yn gywir? (other)',
    },
    answer: {
      en: 'Yes, 10 people live here',
      cy: 'Ydy, mae 10 pherson yn byw yma (other)',
    },
  },
];

describe('Language Code', function() {
  it('Given a launch language of Welsh, I should see Welsh text', function() {
    browser.openQuestionnaire('test_language.json', {
      language: 'cy'
    });

    expect($(NamePage.questionText()).getText()).to.contain('Rhowch enw');

    $(NamePage.firstName()).setValue('Catherine');
    $(NamePage.lastName()).setValue('Zeta-Jones');
    $(NamePage.submit()).click();

    $(DobPage.day()).setValue(25);
    $(DobPage.month()).setValue(9);
    $(DobPage.year()).setValue(1969);
    $(DobPage.submit()).click();

    $(NumberOfPeoplePage.numberOfPeople()).setValue(0);
    $(NumberOfPeoplePage.submit()).click();
    $(ConfirmNumberOfPeoplePage.yes()).click();
    $(ConfirmNumberOfPeoplePage.submit()).click();

    expect(browser.getUrl()).to.contain(SummaryPage.pageName);
    expect($(SummaryPage.dobQuestion()).getText()).to.contain('Beth yw dyddiad geni Catherine Zeta-Jones?');
    expect($(SummaryPage.dateOfBirthAnswer()).getText()).to.contain('25 Medi 1969');
    $(SummaryPage.submit()).click();

    expect(browser.getUrl()).to.contain('thank-you');
    expect($(ThankYouPage.submissionSuccessfulTitle()).getText()).to.contain('Diolch am gyflwyno eich cyfrifiad');
  });

  it('Given a launch language of English, I should see English text', function() {
    browser.openQuestionnaire('test_language.json', {
      language: 'en'
    });

    expect($(NamePage.questionText()).getText()).to.contain('Please enter a name');
    $(NamePage.firstName()).setValue('Catherine');
    $(NamePage.lastName()).setValue('Zeta-Jones');
    $(NamePage.submit()).click();

    $(DobPage.day()).setValue(25);
    $(DobPage.month()).setValue(9);
    $(DobPage.year()).setValue(1969);
    $(DobPage.submit()).click();

    $(NumberOfPeoplePage.numberOfPeople()).setValue(0);
    $(NumberOfPeoplePage.submit()).click();
    $(ConfirmNumberOfPeoplePage.yes()).click();
    $(ConfirmNumberOfPeoplePage.submit()).click();

    expect(browser.getUrl()).to.contain(SummaryPage.pageName);
    expect($(SummaryPage.dobQuestion()).getText()).to.contain('What is Catherine Zeta-Jones’ date of birth?');
    expect($(SummaryPage.dateOfBirthAnswer()).getText()).to.contain('25 September 1969');
    $(SummaryPage.submit()).click();

    expect(browser.getUrl()).to.contain('thank-you');
    expect($(ThankYouPage.submissionSuccessfulTitle()).getText()).to.contain('Thank you for submitting your census');
  });

  it('Given a launch language of English, When I select Cymraeg, Then the language should be switched to Welsh', function() {
    browser.openQuestionnaire('test_language.json', {
      language: 'en'
    });

    expect($(NamePage.questionText()).getText()).to.contain('Please enter a name');
    $(NamePage.switchLanguage('cy')).click();
    expect($(NamePage.questionText()).getText()).to.contain('Rhowch enw');
    $(NamePage.switchLanguage('en')).click();

    $(NamePage.firstName()).setValue('Catherine');
    $(NamePage.lastName()).setValue('Zeta-Jones');
    $(NamePage.submit()).click();

    $(DobPage.day()).setValue(25);
    $(DobPage.month()).setValue(9);
    $(DobPage.year()).setValue(1969);
    $(DobPage.submit()).click();

    $(NumberOfPeoplePage.numberOfPeople()).setValue(0);
    $(NumberOfPeoplePage.submit()).click();
    $(ConfirmNumberOfPeoplePage.yes()).click();
    $(ConfirmNumberOfPeoplePage.submit()).click();

    expect(browser.getUrl()).to.contain(SummaryPage.pageName);
    expect($(SummaryPage.dateOfBirthAnswer()).getText()).to.contain('25 September 1969');
    $(SummaryPage.switchLanguage('cy')).click();
    expect($(SummaryPage.dateOfBirthAnswer()).getText()).to.contain('25 Medi 1969');
    $(SummaryPage.submit()).click();

    expect(browser.getUrl()).to.contain('thank-you');
    expect($(ThankYouPage.submissionSuccessfulTitle()).getText()).to.contain('Diolch am gyflwyno eich cyfrifiad');
    $(ThankYouPage.switchLanguage('en')).click();
    expect($(ThankYouPage.submissionSuccessfulTitle()).getText()).to.contain('Thank you for submitting your census');
  });

  it('Given a launch language of Welsh, When I select English, Then the language should be switched to English', function() {
    browser.openQuestionnaire('test_language.json', {
      language: 'cy'
    });

    expect($(NamePage.questionText()).getText()).to.contain('Rhowch enw');
    $(NamePage.switchLanguage('en')).click();
    expect($(NamePage.questionText()).getText()).to.contain('Please enter a name');
  });

  describe('Given a launch language of English and a question with plural forms, When I select switch languages, Then the plural forms are displayed correctly for the chosen language', function() {

    for (let dataSet of PLURAL_TEST_DATA_SETS) {
      let numberOfPeople = dataSet['count'];

      it(`Test plural count: ${numberOfPeople}`, function() {
        browser.openQuestionnaire('test_language.json', {
          language: 'en'
        });

        expect($(NamePage.questionText()).getText()).to.contain('Please enter a name');
        $(NamePage.firstName()).setValue('Catherine');
        $(NamePage.lastName()).setValue('Zeta-Jones');
        $(NamePage.submit()).click();

        $(DobPage.day()).setValue(25);
        $(DobPage.month()).setValue(9);
        $(DobPage.year()).setValue(1969);
        $(DobPage.submit()).click();

        $(NumberOfPeoplePage.numberOfPeople()).setValue(numberOfPeople);
        $(NumberOfPeoplePage.submit()).click();

        expect($(ConfirmNumberOfPeoplePage.questionText()).getText()).to.contain(dataSet.question_title.en);
        expect($(ConfirmNumberOfPeoplePage.yesLabel()).getText()).to.contain(dataSet.answer.en);

        $(ConfirmNumberOfPeoplePage.switchLanguage('cy')).click();

        expect($(ConfirmNumberOfPeoplePage.questionText()).getText()).to.contain(dataSet.question_title.cy);
        expect($(ConfirmNumberOfPeoplePage.yesLabel()).getText()).to.contain(dataSet.answer.cy);

        $(ConfirmNumberOfPeoplePage.yes()).click();
        $(ConfirmNumberOfPeoplePage.submit()).click();

        expect(browser.getUrl()).to.contain(SummaryPage.pageName);
        expect($(SummaryPage.totalPeopleQuestion()).getText()).to.contain(dataSet.question_title.cy);
        expect($(SummaryPage.confirmCount()).getText()).to.contain(dataSet.answer.cy);

        $(ConfirmNumberOfPeoplePage.switchLanguage('en')).click();

        expect($(SummaryPage.totalPeopleQuestion()).getText()).to.contain(dataSet.question_title.en);
        expect($(SummaryPage.confirmCount()).getText()).to.contain(dataSet.answer.en);
      });
    }
  });

});
