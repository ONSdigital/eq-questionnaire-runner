import ConditionalCombinedRoutingPage from "../generated_pages/conditional_combined_routing/conditional-routing-block.page";
import ResponseAny from "../generated_pages/conditional_combined_routing/response-any.page";
import ResponseNotAny from "../generated_pages/conditional_combined_routing/response-not-any.page";
import SubmitPage from "../generated_pages/conditional_combined_routing/submit.page";

describe("Conditional combined routing.", () => {
  beforeEach(async ()=> {
    await browser.openQuestionnaire("test_conditional_combined_routing.json");
  });

  it('Given a list of radio options, when I choose the option "Yes" or the option "Sometimes" then I should be routed to the relevant page', async ()=> {
    // When
    await $(await ConditionalCombinedRoutingPage.yes()).click();
    await $(await ConditionalCombinedRoutingPage.submit()).click();
    // Then
    await expect(browser.getUrl()).to.contain(ResponseAny.pageName);

    // Or
    await $(await ResponseAny.previous()).click();

    // When
    await $(await ConditionalCombinedRoutingPage.sometimes()).click();
    await $(await ConditionalCombinedRoutingPage.submit()).click();

    // Then
    await expect(browser.getUrl()).to.contain(ResponseAny.pageName);
  });

  it('Given a list of radio options, when I choose the option "No, I prefer tea" then I should be routed to the relevant page', async ()=> {
    // When
    await $(await ConditionalCombinedRoutingPage.noIPreferTea()).click();
    await $(await ConditionalCombinedRoutingPage.submit()).click();
    // Then
    await expect(browser.getUrl()).to.contain(ResponseNotAny.pageName);
  });

  it('Given a list of radio options, when I choose the option "No, I don\'t drink any hot drinks" then I should be routed to the submit page', async ()=> {
    // When
    await $(await ConditionalCombinedRoutingPage.noIDonTDrinkAnyHotDrinks()).click();
    await $(await ConditionalCombinedRoutingPage.submit()).click();
    // Then
    await expect(browser.getUrl()).to.contain(SubmitPage.pageName);
  });
});
