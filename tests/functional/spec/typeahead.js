const TypeaheadPage = require('../generated_pages/textfield_typeahead/country-block.page.js');

describe('Typeahead', function() {
  it('Given I open a typeahead, when I have entered text, then it will show suggestions', function() {
    browser.openQuestionnaire('test_textfield_typeahead.json');
    $(TypeaheadPage.country()).setValue("Uni");
    $("#country-answer-listbox li").waitForDisplayed();
    expect($$('.js-typeahead-listbox li').length).to.not.equal(0);
  });
});
