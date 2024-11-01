import RoutingCheckboxContains from "../../../generated_pages/routing_checkbox_contains/country-checkbox.page";
import ContainsAllPage from "../../../generated_pages/routing_checkbox_contains/country-interstitial-all.page";
import ContainsAnyPage from "../../../generated_pages/routing_checkbox_contains/country-interstitial-any.page";
import SubmitPage from "../../../generated_pages/routing_checkbox_contains/submit.page";
import { click, verifyUrlContains } from "../../../helpers";
describe("Routing Checkbox Contains Condition.", () => {
  beforeEach(async () => {
    await browser.openQuestionnaire("test_routing_checkbox_contains.json");
  });

  it('Given a list of checkbox options, when I have don\'t select "Liechtenstein" and select the option "India" or the option "Azerbaijan" or both then I should be routed to the "contains any" condition page', async () => {
    // When
    await expect(await $(RoutingCheckboxContains.liechtenstein()).isSelected()).toBe(false);

    await $(RoutingCheckboxContains.india()).click();
    await click(RoutingCheckboxContains.submit());
    // Then
    await verifyUrlContains(ContainsAnyPage.pageName);

    // Or
    await $(ContainsAnyPage.previous()).click();

    // When
    await $(RoutingCheckboxContains.india()).click();
    await $(RoutingCheckboxContains.azerbaijan()).click();
    await click(RoutingCheckboxContains.submit());

    // Then
    await verifyUrlContains(ContainsAnyPage.pageName);

    // Or
    await $(ContainsAnyPage.previous()).click();

    // When
    await $(RoutingCheckboxContains.india()).click();
    await click(RoutingCheckboxContains.submit());

    // Then
    await verifyUrlContains(ContainsAnyPage.pageName);
  });

  it('Given a list of checkbox options, when I select the option "Malta" or the option "Liechtenstein" or both then I should be routed to the summary condition page', async () => {
    // When
    await $(RoutingCheckboxContains.liechtenstein()).click();
    await click(RoutingCheckboxContains.submit());
    // Then
    await verifyUrlContains(SubmitPage.pageName);

    // Or
    await $(ContainsAnyPage.previous()).click();

    // When
    await $(RoutingCheckboxContains.liechtenstein()).click();
    await $(RoutingCheckboxContains.malta()).click();
    await click(RoutingCheckboxContains.submit());

    // Then
    await verifyUrlContains(SubmitPage.pageName);

    // Or
    await $(ContainsAnyPage.previous()).click();

    // When
    await $(RoutingCheckboxContains.liechtenstein()).click();
    await click(RoutingCheckboxContains.submit());

    // Then
    await verifyUrlContains(SubmitPage.pageName);
  });

  it('Given a list of checkbox options, when I select the options "India", "Azerbaijan" and "Liechtenstein" then I should be routed to the "contains all" condition page', async () => {
    // When
    await $(RoutingCheckboxContains.india()).click();
    await $(RoutingCheckboxContains.azerbaijan()).click();
    await $(RoutingCheckboxContains.liechtenstein()).click();
    await click(RoutingCheckboxContains.submit());
    // Then
    await verifyUrlContains(ContainsAllPage.pageName);
  });
});
