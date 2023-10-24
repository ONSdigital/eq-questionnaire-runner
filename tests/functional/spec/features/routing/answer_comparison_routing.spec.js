import RouteComparison1Page from "../../../generated_pages/routing_answer_comparison/route-comparison-1.page.js";
import RouteComparison2Page from "../../../generated_pages/routing_answer_comparison/route-comparison-2.page.js";
import { click } from "../../../helpers";

describe("Test routing skip", () => {
  beforeEach(async () => {
    await browser.openQuestionnaire("test_routing_answer_comparison.json");
  });

  it("Given we start the routing test survey, When we enter a low number then a high number, Then, we should be routed to the fourth page", async () => {
    await $(RouteComparison1Page.answer()).setValue(1);
    await click(RouteComparison1Page.submit());
    await $(RouteComparison2Page.answer()).setValue(2);
    await click(RouteComparison2Page.submit());
    await expect(await $("#main-content > p").getText()).toBe("This page should never be skipped");
  });

  it("Given we start the routing test survey, When we enter a high number then a low number, Then, we should be routed to the third page", async () => {
    await $(RouteComparison1Page.answer()).setValue(1);
    await click(RouteComparison1Page.submit());
    await $(RouteComparison2Page.answer()).setValue(0);
    await click(RouteComparison2Page.submit());
    await expect(await $("#main-content > p").getText()).toBe(
      "This page should be skipped if your second answer was higher than your first"
    );
  });

  it("Given we start the routing test survey, When we enter an equal number on both questions, Then, we should be routed to the third page", async () => {
    await $(RouteComparison1Page.answer()).setValue(1);
    await click(RouteComparison1Page.submit());
    await $(RouteComparison2Page.answer()).setValue(1);
    await click(RouteComparison2Page.submit());
    await expect(await $("#main-content > p").getText()).toBe(
      "This page should be skipped if your second answer was higher than your first"
    );
  });
});
