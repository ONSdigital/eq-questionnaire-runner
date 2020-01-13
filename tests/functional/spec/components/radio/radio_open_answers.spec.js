const RadioOpenTruePage = require('../../../generated_pages/radio_open/radio-open-true.page.js');
const RadioOpenFalsePage = require('../../../generated_pages/radio_open/radio-open-false.page.js');
const RadioOpenNonePage = require('../../../generated_pages/radio_open/radio-open-none.page.js');

describe('Given I start a Radio survey with a write-in option', function() {
  beforeEach(function() {
    browser.openQuestionnaire('test_radio_open.json');
  });

  it('When I view a write-in radio and the open option is set to true, Then the detail answer label should be displayed', function() {
    $(RadioOpenTruePage.coffee()).click();
    expect($(RadioOpenTruePage.otherDetail()).isDisplayed()).to.equal(true);
  });

  it('When I view a write-in radio and the open option is set to false, Then the detail answer label should not be displayed', function() {
    $(RadioOpenTruePage.coffee()).click();
    $(RadioOpenTruePage.submit()).click();
    expect($(RadioOpenFalsePage.otherDetail()).isDisplayed()).to.equal(false);
  });

  it('When I view a write-in radio and the open option is not set, Then the detail answer label should not be displayed', function() {
    $(RadioOpenTruePage.coffee()).click();
    $(RadioOpenFalsePage.submit()).click();
    $(RadioOpenFalsePage.iceCream()).click();
    $(RadioOpenFalsePage.submit()).click();
    expect($(RadioOpenNonePage.otherDetail()).isDisplayed()).to.equal(false);
  });
});
