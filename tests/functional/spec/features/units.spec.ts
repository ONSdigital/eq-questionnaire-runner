import { test, expect } from '../../fixtures/test'
import SetLengthUnitsBlockPage from '../../generated_pages/unit_patterns/set-length-units-block.page'
import SetDurationUnitsBlockPage from '../../generated_pages/unit_patterns/set-duration-units-block.page'
import SetAreaUnitsBlockPage from '../../generated_pages/unit_patterns/set-area-units-block.page'
import SetVolumeUnitsBlockPage from '../../generated_pages/unit_patterns/set-volume-units-block.page'
import SetWeightUnitsBlockPage from '../../generated_pages/unit_patterns/set-weight-units-block.page'
import SubmitPage from '../../generated_pages/unit_patterns/submit.page'

test.describe('Units', () => {
  test('Given we do not set a language code and run the questionnaire, When we enter values for durations, Then they should be displayed on the summary with their units.', async ({
    page,
    openQuestionnaire
  }) => {
    const setAreaUnitsBlockPage = new SetAreaUnitsBlockPage(page)
    const setDurationUnitsBlockPage = new SetDurationUnitsBlockPage(page)
    const setLengthUnitsBlockPage = new SetLengthUnitsBlockPage(page)
    const setVolumeUnitsBlockPage = new SetVolumeUnitsBlockPage(page)
    const setWeightUnitsBlockPage = new SetWeightUnitsBlockPage(page)
    const submitPage = new SubmitPage(page)
    await openQuestionnaire('test_unit_patterns.json', { language: 'en' })
    await setLengthUnitsBlockPage.submit().click()
    await expect(setDurationUnitsBlockPage.durationHourUnit()).toHaveText('hours')
    await expect(setDurationUnitsBlockPage.durationYearUnit()).toHaveText('years')
    await setDurationUnitsBlockPage.durationHour().fill('6')
    await setDurationUnitsBlockPage.durationYear().fill('20')
    await setDurationUnitsBlockPage.submit().click()
    await setAreaUnitsBlockPage.submit().click()
    await setVolumeUnitsBlockPage.submit().click()
    await setWeightUnitsBlockPage.submit().click()
    await expect(submitPage.durationHour()).toHaveText('6 hours')
    await expect(submitPage.durationYear()).toHaveText('20 years')
  })

  test('Given we set a language code for welsh and run the questionnaire, When we enter values for durations, Then they should be displayed on the summary with their units.', async ({
    page,
    openQuestionnaire
  }) => {
    const setAreaUnitsBlockPage = new SetAreaUnitsBlockPage(page)
    const setDurationUnitsBlockPage = new SetDurationUnitsBlockPage(page)
    const setLengthUnitsBlockPage = new SetLengthUnitsBlockPage(page)
    const setVolumeUnitsBlockPage = new SetVolumeUnitsBlockPage(page)
    const setWeightUnitsBlockPage = new SetWeightUnitsBlockPage(page)
    const submitPage = new SubmitPage(page)
    await openQuestionnaire('test_unit_patterns.json', { language: 'cy' })
    await setLengthUnitsBlockPage.submit().scrollIntoViewIfNeeded()
    await setLengthUnitsBlockPage.submit().click()
    await expect(setDurationUnitsBlockPage.durationHourUnit()).toHaveText('awr')
    await expect(setDurationUnitsBlockPage.durationYearUnit()).toHaveText('flynedd')
    await setDurationUnitsBlockPage.durationHour().fill('6')
    await setDurationUnitsBlockPage.durationYear().fill('20')
    await setDurationUnitsBlockPage.submit().scrollIntoViewIfNeeded()
    await setDurationUnitsBlockPage.submit().click()
    await setAreaUnitsBlockPage.submit().click()
    await setVolumeUnitsBlockPage.submit().click()
    await setWeightUnitsBlockPage.submit().click()
    await expect(submitPage.durationHour()).toHaveText('6 awr')
    await expect(submitPage.durationYear()).toHaveText('20 mlynedd')
  })

  test('Given we open a questionnaire with unit labels, When the label is highlighted by the tooltip, Then the long unit label should be displayed.', async ({
    page,
    openQuestionnaire
  }) => {
    const setLengthUnitsBlockPage = new SetLengthUnitsBlockPage(page)
    await openQuestionnaire('test_unit_patterns.json', { language: 'en' })
    await expect(setLengthUnitsBlockPage.centimetresUnit()).toHaveAttribute('title', 'centimetres')
    await expect(setLengthUnitsBlockPage.metresUnit()).toHaveAttribute('title', 'metres')
    await expect(setLengthUnitsBlockPage.kilometresUnit()).toHaveAttribute('title', 'kilometres')
    await expect(setLengthUnitsBlockPage.milesUnit()).toHaveAttribute('title', 'miles')
  })

  test('Given we open a questionnaire with unit labels, When the weight unit label is highlighted by the tooltip, Then the correct unit label should be displayed.', async ({
    page,
    openQuestionnaire
  }) => {
    const setAreaUnitsBlockPage = new SetAreaUnitsBlockPage(page)
    const setDurationUnitsBlockPage = new SetDurationUnitsBlockPage(page)
    const setLengthUnitsBlockPage = new SetLengthUnitsBlockPage(page)
    const setVolumeUnitsBlockPage = new SetVolumeUnitsBlockPage(page)
    const setWeightUnitsBlockPage = new SetWeightUnitsBlockPage(page)
    await openQuestionnaire('test_unit_patterns.json', { language: 'en' })
    await setLengthUnitsBlockPage.submit().click()
    await setDurationUnitsBlockPage.submit().click()
    await setAreaUnitsBlockPage.submit().click()
    await setVolumeUnitsBlockPage.submit().click()
    await expect(setWeightUnitsBlockPage.massTonneUnit()).toHaveAttribute('title', 'tonnes')
  })

  test('Given we open a questionnaire with unit inputs, When the unit allows a maximum of 6 decimal places, Then the correct number of decimal places should be displayed on the summary.', async ({
    page,
    openQuestionnaire
  }) => {
    const setAreaUnitsBlockPage = new SetAreaUnitsBlockPage(page)
    const setDurationUnitsBlockPage = new SetDurationUnitsBlockPage(page)
    const setLengthUnitsBlockPage = new SetLengthUnitsBlockPage(page)
    const setVolumeUnitsBlockPage = new SetVolumeUnitsBlockPage(page)
    const setWeightUnitsBlockPage = new SetWeightUnitsBlockPage(page)
    const submitPage = new SubmitPage(page)
    await openQuestionnaire('test_unit_patterns.json', { language: 'en' })
    await setLengthUnitsBlockPage.submit().click()
    await setDurationUnitsBlockPage.submit().click()
    await setAreaUnitsBlockPage.submit().click()
    await setVolumeUnitsBlockPage.cubicCentimetres().fill('1.1')
    await setVolumeUnitsBlockPage.cubicMetres().fill('1.12')
    await setVolumeUnitsBlockPage.litres().fill('1.123')
    await setVolumeUnitsBlockPage.hectolitres().fill('1.1234')
    await setVolumeUnitsBlockPage.megalitres().fill('1.10000')
    await setVolumeUnitsBlockPage.submit().click()
    await setWeightUnitsBlockPage.submit().click()
    await expect(submitPage.cubicCentimetres()).toHaveText('1.1 cm³')
    await expect(submitPage.cubicMetres()).toHaveText('1.12 m³')
    await expect(submitPage.litres()).toHaveText('1.123 l')
    await expect(submitPage.hectolitres()).toHaveText('1.1234 hl')
    await expect(submitPage.megalitres()).toHaveText('1.10000 Ml')
  })
})
