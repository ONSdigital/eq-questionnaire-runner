const SuggestionsPage = require('../generated_pages/textfield_suggestions/country-block.page.js');

describe('Suggestions', function() {
  it('Given text entered into a textfield typeahead, it will show suggestions', function() {
    browser.openQuestionnaire('test_textfield_lookup.json');
    $(SuggestionsPage.country()).setValue("Uni");
    $("#country-answer-listbox li").waitForDisplayed();
    expect($$('.js-typeahead-listbox li').length).to.not.equal(0);
  });
});
