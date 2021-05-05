import SuggestionsPage from "../generated_pages/textfield_suggestions/country-block.page.js";
import MultipleSuggestionsPage from "../generated_pages/textfield_suggestions/multiple-country-block.page.js";
import SummaryPage from "../generated_pages/textfield_suggestions/summary.page.js";

describe("Suggestions", () => {
  it("Given I open a textfield with a suggestions url, when I have entered text, then it will show suggestions", () => {
    browser.openQuestionnaire("test_textfield_suggestions.json");
    $(SuggestionsPage.country()).setValue("Uni");
    $("#country-answer-listbox li").waitForDisplayed();
    expect($$(".js-autosuggest-listbox li").length).to.not.equal(0);
  });
});

describe("Suggestions", () => {
  it("Given I open a textfield with a suggestions url that allows multiple suggestions, when I have entered text and picked suggestion from a list, then after typing more text it will show new suggestions", () => {
    browser.openQuestionnaire("test_textfield_suggestions.json");
    const suggestionsList = $("#multiple-country-answer-listbox li");
    const suggestionsOption = $("#multiple-country-answer-listbox__option--0");

    $(SuggestionsPage.country()).setValue("United States of America");
    $(SuggestionsPage.submit()).click();
    $(MultipleSuggestionsPage.multipleCountry()).click();
    // Browser needs to pause before typing starts to allow for the autosuggest Javascript to initialise
    browser.pause(500);
    browser.keys("Ita");
    suggestionsList.waitForExist();
    suggestionsOption.click();
    $(MultipleSuggestionsPage.multipleCountry()).click();
    // Browser needs to pause before typing starts to allow for the autosuggest Javascript to initialise
    browser.pause(500);
    browser.keys(" United");
    suggestionsList.waitForExist();
    expect($$(".js-autosuggest-listbox li").length).to.not.equal(0);
    suggestionsOption.click();
    $(MultipleSuggestionsPage.submit()).click();
    expect(browser.getUrl()).to.contain(SummaryPage.url());
  });
});
