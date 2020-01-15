const RadioVisibleTruePage = require('../../../generated_pages/radio_detail_answer_visible/radio-visible-true.page.js');
const RadioVisibleFalsePage = require('../../../generated_pages/radio_detail_answer_visible/radio-visible-false.page.js');
const RadioVisibleNonePage = require('../../../generated_pages/radio_detail_answer_visible/radio-visible-none.page.js');

describe('Given I start a Radio survey with a write-in option', function() {
  beforeEach(function() {
    browser.openQuestionnaire('test_radio_detail_answer_visible.json');
  });

  it('When I view a write-in radio and the visible option is set to true, Then the detail answer label should be displayed', function() {
    expect($(RadioVisibleTruePage.otherDetail()).isDisplayed()).to.equal(true);
  });

  it('When I view a write-in radio and the visible option is set to true, Then after choosing non write-in option the detail answer label should be displayed', function() {
    $(RadioVisibleTruePage.coffee()).click();
    expect($(RadioVisibleTruePage.otherDetail()).isDisplayed()).to.equal(true);
  });

  it('When I view a write-in radio and the visible option is set to false, Then the detail answer label should not be displayed', function() {
    $(RadioVisibleTruePage.coffee()).click();
    $(RadioVisibleTruePage.submit()).click();
    expect($(RadioVisibleFalsePage.otherDetail()).isDisplayed()).to.equal(false);
  });

  it('When I view a write-in radio and the visible option is not set, Then the detail answer label should not be displayed', function() {
    $(RadioVisibleTruePage.coffee()).click();
    $(RadioVisibleFalsePage.submit()).click();
    $(RadioVisibleFalsePage.iceCream()).click();
    $(RadioVisibleFalsePage.submit()).click();
    expect($(RadioVisibleNonePage.otherDetail()).isDisplayed()).to.equal(false);
  });
});
