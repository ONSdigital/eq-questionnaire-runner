import SuggestionsPage from "../generated_pages/textfield_suggestions/country-block.page.js";
import MultipleSuggestionsPage from "../generated_pages/textfield_suggestions/multiple-country-block.page.js";
import SubmitPage from "../generated_pages/textfield_suggestions/submit.page.js";
import { click } from "../helpers";
describe("Suggestions", () => {
  it("Given I open a textfield with a suggestions url, when I have entered text, then it will show suggestions", async () => {
    await browser.openQuestionnaire("test_textfield_suggestions.json");
    await $(SuggestionsPage.country()).setValue("Uni");
    $("#country-answer-listbox li").waitForDisplayed();
    await expect(await $$(".ons-js-autosuggest-listbox li").length).not.toBe(0);
  });
});

describe("Suggestions", () => {
  it("Given I open a textfield with a suggestions url that allows multiple suggestions, when I have entered text and picked suggestion from a list, then after typing more text it will show new suggestions", async () => {
    await browser.openQuestionnaire("test_textfield_suggestions.json");
    const suggestionsList = $("#multiple-country-answer-listbox li");
    const suggestionsOption = $("#multiple-country-answer-listbox__option--0");

    await $(SuggestionsPage.country()).setValue("United States of America");
    await click(SuggestionsPage.submit());
    await $(MultipleSuggestionsPage.multipleCountry()).click();
    // Browser needs to pause before typing starts to allow for the autosuggest Javascript to initialise
    await browser.pause(500);
    await browser.keys("Ita");
    await suggestionsList.waitForExist();
    await suggestionsOption.click();
    await $(MultipleSuggestionsPage.multipleCountry()).click();
    // Browser needs to pause before typing starts to allow for the autosuggest Javascript to initialise
    await browser.pause(500);
    await browser.keys(" United");
    await suggestionsList.waitForExist();
    await expect(await $$(".ons-js-autosuggest-listbox li").length).not.toBe(0);
    // TODO there is an issue with the load-time of the auto-suggest dropdown causing this test to fail. Uncomment when this has been resolved.
    // await suggestionsOption.click();
    await click(MultipleSuggestionsPage.submit());
    await expect(browser).toHaveUrlContaining(SubmitPage.url());
  });
});
