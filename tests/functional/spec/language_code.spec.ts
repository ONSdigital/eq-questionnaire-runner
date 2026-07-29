import { test, expect } from '../fixtures/test'
import type { Locator, Page } from '../fixtures/test'
import NamePage from '../generated_pages/language/name-block.page'
import DobPage from '../generated_pages/language/dob-block.page'
import NumberOfPeoplePage from '../generated_pages/language/number-of-people-block.page'
import ConfirmNumberOfPeoplePage from '../generated_pages/language/confirm-number-of-people.page'
import HubPage from '../base_pages/hub.page'

const switchLanguage = async (page: Page, languageLink: Locator): Promise<void> => {
  const href = await languageLink.getAttribute('href')
  if (href === null || href.length === 0) {
    throw new Error('Language switch link has no href')
  }

  await page.goto(new URL(href, page.url()).toString())
}

const PLURAL_TEST_DATA_SETS = [
  {
    count: 0,
    question_title: {
      en: '0 people live here, is this correct?',
      cy: 'Mae 0 person yn byw yma, ydy hyn yn gywir? (zero)'
    },
    answer: {
      en: 'Yes, 0 people live here',
      cy: 'Ydy, mae 0 person yn byw yma (zero)'
    }
  },
  {
    count: 1,
    question_title: {
      en: '1 person lives here, is this correct?',
      cy: 'Mae 1 person yn byw yma, ydy hyn yn gywir? (one)'
    },
    answer: {
      en: 'Yes, 1 person lives here',
      cy: 'Ydy, mae 1 person yn byw yma (one)'
    }
  },
  {
    count: 2,
    question_title: {
      en: '2 people live here, is this correct?',
      cy: 'Mae 2 person yn byw yma, ydy hyn yn gywir? (two)'
    },
    answer: {
      en: 'Yes, 2 people live here',
      cy: 'Ydy, mae 2 person yn byw yma (two)'
    }
  },
  {
    count: 3,
    question_title: {
      en: '3 people live here, is this correct?',
      cy: 'Mae 3 pherson yn byw yma, ydy hyn yn gywir? (few)'
    },
    answer: {
      en: 'Yes, 3 people live here',
      cy: 'Ydy, mae 3 pherson yn byw yma (few)'
    }
  },
  {
    count: 6,
    question_title: {
      en: '6 people live here, is this correct?',
      cy: 'Mae 6 pherson yn byw yma, ydy hyn yn gywir? (many)'
    },
    answer: {
      en: 'Yes, 6 people live here',
      cy: 'Ydy, mae 6 pherson yn byw yma (many)'
    }
  },
  {
    count: 4,
    question_title: {
      en: '4 people live here, is this correct?',
      cy: 'Mae 4 pherson yn byw yma, ydy hyn yn gywir? (other)'
    },
    answer: {
      en: 'Yes, 4 people live here',
      cy: 'Ydy, mae 4 pherson yn byw yma (other)'
    }
  },
  {
    count: 5,
    question_title: {
      en: '5 people live here, is this correct?',
      cy: 'Mae 5 pherson yn byw yma, ydy hyn yn gywir? (other)'
    },
    answer: {
      en: 'Yes, 5 people live here',
      cy: 'Ydy, mae 5 pherson yn byw yma (other)'
    }
  },
  {
    count: 10,
    question_title: {
      en: '10 people live here, is this correct?',
      cy: 'Mae 10 pherson yn byw yma, ydy hyn yn gywir? (other)'
    },
    answer: {
      en: 'Yes, 10 people live here',
      cy: 'Ydy, mae 10 pherson yn byw yma (other)'
    }
  }
]

test.describe('Language Code', () => {
  test('Given a launch language of Welsh, I should see Welsh text', async ({ page, openQuestionnaire }) => {
    const confirmNumberOfPeoplePage = new ConfirmNumberOfPeoplePage(page)
    const dobPage = new DobPage(page)
    const hubPage = new HubPage(page)
    const namePage = new NamePage(page)
    const numberOfPeoplePage = new NumberOfPeoplePage(page)
    await openQuestionnaire('test_language.json', {
      language: 'cy'
    })
    await hubPage.submit().click()
    await expect(namePage.questionText()).toHaveText('Rhowch enw')

    await namePage.firstName().fill('Catherine')
    await namePage.lastName().fill('Zeta-Jones')
    await namePage.submit().click()

    await dobPage.day().fill('25')
    await dobPage.month().fill('9')
    await dobPage.year().fill('1969')
    await dobPage.submit().click()

    await numberOfPeoplePage.numberOfPeople().fill('0')
    await numberOfPeoplePage.submit().click()
    await confirmNumberOfPeoplePage.yes().click()
    await confirmNumberOfPeoplePage.submit().click()

    await expect(hubPage.heading()).toHaveText('Teitl cyflwyno')
    await expect(hubPage.warning()).toHaveText('Rhybudd cyflwyno')
    await expect(hubPage.guidance()).toHaveText('Canllawiau cyflwyno')
    await expect(hubPage.submit()).toHaveText('Botwm cyflwyno')
    await hubPage.submit().click()

    await expect(page).toHaveURL(/thank-you/)
  })

  test('Given a launch language of English, I should see English text', async ({ page, openQuestionnaire }) => {
    const confirmNumberOfPeoplePage = new ConfirmNumberOfPeoplePage(page)
    const dobPage = new DobPage(page)
    const hubPage = new HubPage(page)
    const namePage = new NamePage(page)
    const numberOfPeoplePage = new NumberOfPeoplePage(page)
    await openQuestionnaire('test_language.json', {
      language: 'en'
    })

    await hubPage.submit().click()
    await expect(namePage.questionText()).toHaveText('Please enter a name')
    await namePage.firstName().fill('Catherine')
    await namePage.lastName().fill('Zeta-Jones')
    await namePage.submit().click()

    await dobPage.day().fill('25')
    await dobPage.month().fill('9')
    await dobPage.year().fill('1969')
    await dobPage.submit().click()

    await numberOfPeoplePage.numberOfPeople().fill('0')
    await numberOfPeoplePage.submit().click()
    await confirmNumberOfPeoplePage.yes().click()
    await confirmNumberOfPeoplePage.submit().click()

    await expect(hubPage.heading()).toHaveText('Submission title')
    await expect(hubPage.warning()).toHaveText('Submission warning')
    await expect(hubPage.guidance()).toHaveText('Submission guidance')
    await expect(hubPage.submit()).toHaveText('Submission button')
    await hubPage.submit().click()

    await expect(page).toHaveURL(/thank-you/)
  })

  test('Given a launch language of English, When I select Cymraeg, Then the language should be switched to Welsh', async ({ page, openQuestionnaire }) => {
    const confirmNumberOfPeoplePage = new ConfirmNumberOfPeoplePage(page)
    const dobPage = new DobPage(page)
    const hubPage = new HubPage(page)
    const namePage = new NamePage(page)
    const numberOfPeoplePage = new NumberOfPeoplePage(page)
    await openQuestionnaire('test_language.json', {
      language: 'en'
    })

    await hubPage.submit().click()
    await expect(namePage.questionText()).toHaveText('Please enter a name')
    await expect(page.locator('header')).toContainText('Test Language')
    await switchLanguage(page, namePage.switchLanguage('cy'))
    await expect(namePage.questionText()).toHaveText('Rhowch enw')
    await expect(page.locator('header')).toContainText('Arolwg Iaith Prawf')
    await switchLanguage(page, namePage.switchLanguage('en'))

    await namePage.firstName().fill('Catherine')
    await namePage.lastName().fill('Zeta-Jones')
    await namePage.submit().click()

    await dobPage.day().fill('25')
    await dobPage.month().fill('9')
    await dobPage.year().fill('1969')
    await dobPage.submit().click()

    await numberOfPeoplePage.numberOfPeople().fill('0')
    await numberOfPeoplePage.submit().click()
    await confirmNumberOfPeoplePage.yes().click()
    await confirmNumberOfPeoplePage.submit().click()

    await expect(hubPage.heading()).toHaveText('Submission title')
    await expect(hubPage.warning()).toHaveText('Submission warning')
    await expect(hubPage.guidance()).toHaveText('Submission guidance')
    await expect(hubPage.submit()).toHaveText('Submission button')
    await switchLanguage(page, hubPage.switchLanguage('cy'))
    await expect(hubPage.heading()).toHaveText('Teitl cyflwyno')
    await expect(hubPage.warning()).toHaveText('Rhybudd cyflwyno')
    await expect(hubPage.guidance()).toHaveText('Canllawiau cyflwyno')
    await expect(hubPage.submit()).toHaveText('Botwm cyflwyno')
    await hubPage.submit().click()

    await expect(page).toHaveURL(/thank-you/)
  })

  test('Given a launch language of Welsh, When I select English, Then the language should be switched to English', async ({ page, openQuestionnaire }) => {
    const hubPage = new HubPage(page)
    const namePage = new NamePage(page)
    await openQuestionnaire('test_language.json', {
      language: 'cy'
    })

    await hubPage.submit().click()
    await expect(namePage.questionText()).toHaveText('Rhowch enw')
    await switchLanguage(page, namePage.switchLanguage('en'))
    await expect(namePage.questionText()).toHaveText('Please enter a name')
  })

  test.describe(
    'Given a launch language of English and a question with plural forms, ' +
      'When I select switch languages, Then the plural forms are displayed correctly for the chosen language',
    () => {
      for (const dataSet of PLURAL_TEST_DATA_SETS) {
        const numberOfPeople = dataSet.count

        test(`Test plural count: ${numberOfPeople}`, async ({ page, openQuestionnaire }) => {
          const confirmNumberOfPeoplePage = new ConfirmNumberOfPeoplePage(page)
          const dobPage = new DobPage(page)
          const hubPage = new HubPage(page)
          const namePage = new NamePage(page)
          const numberOfPeoplePage = new NumberOfPeoplePage(page)
          await openQuestionnaire('test_language.json', {
            language: 'en'
          })

          await hubPage.submit().click()
          await expect(namePage.questionText()).toHaveText('Please enter a name')
          await namePage.firstName().fill('Catherine')
          await namePage.lastName().fill('Zeta-Jones')
          await namePage.submit().click()

          await dobPage.day().fill('25')
          await dobPage.month().fill('9')
          await dobPage.year().fill('1969')
          await dobPage.submit().click()

          await numberOfPeoplePage.numberOfPeople().fill(String(numberOfPeople))
          await numberOfPeoplePage.submit().click()

          await expect(confirmNumberOfPeoplePage.questionText()).toHaveText(dataSet.question_title.en)
          await expect(confirmNumberOfPeoplePage.yesLabel()).toHaveText(dataSet.answer.en)

          await switchLanguage(page, confirmNumberOfPeoplePage.switchLanguage('cy'))

          await expect(confirmNumberOfPeoplePage.questionText()).toHaveText(dataSet.question_title.cy)
          await expect(confirmNumberOfPeoplePage.yesLabel()).toHaveText(dataSet.answer.cy)

          await confirmNumberOfPeoplePage.yes().click()
          await confirmNumberOfPeoplePage.submit().click()
        })
      }
    }
  )
})
