import { test, expect } from '../fixtures/test'
import TextFieldPage from '../generated_pages/textfield/name-block.page'
import SubmitPage from '../generated_pages/textfield/submit.page'

test.describe('Textfield', () => {
  test('Given a textfield option, a user should be able to click the label of the textfield to focus', async ({ page, openQuestionnaire }) => {
    const textFieldPage = new TextFieldPage(page)
    await openQuestionnaire('test_textfield.json')
    await textFieldPage.nameLabel().click()
    await expect(textFieldPage.name()).toBeFocused()
  })

  test('Given a text entered in textfield , When user submits and revisits the textfield, Then the textfield must contain the text entered previously', async ({
    page,
    openQuestionnaire
  }) => {
    const submitPage = new SubmitPage(page)
    const textFieldPage = new TextFieldPage(page)
    await openQuestionnaire('test_textfield.json')
    await textFieldPage.name().fill("'Twenty><&Five'")
    await textFieldPage.submit().click()
    await expect(page).toHaveURL(new RegExp(submitPage.pageName))
    await expect(submitPage.nameAnswer()).toHaveText("'Twenty><&Five'")
    await submitPage.nameAnswerEdit().click()
    await textFieldPage.name().inputValue()
  })

  test('Given the string entered to the textfield is too long, When the user submits, then the correct error message is displayed', async ({
    page,
    openQuestionnaire
  }) => {
    const textFieldPage = new TextFieldPage(page)
    await openQuestionnaire('test_textfield.json')
    await textFieldPage.name().fill('This string is too long')
    await textFieldPage.submit().click()
    await expect(textFieldPage.errorNumber(1)).toHaveText('You have entered too many characters. Enter up to 20 characters')
  })
})
