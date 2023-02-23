import RouteComparison1Page from "../../../generated_pages/new_routing_answer_comparison/route-comparison-1.page.js";
import RouteComparison2Page from "../../../generated_pages/new_routing_answer_comparison/route-comparison-2.page.js";

describe("Test routing skip", () => {
  beforeEach(async () => {
    await browser.openQuestionnaire("test_new_routing_answer_comparison.json");
  });

  it("Given we start the routing test survey, When we enter a low number then a high number, Then, we should be routed to the fourth page", async () => {
    await $(RouteComparison1Page.answer()).setValue(1);
    await $(RouteComparison1Page.submit()).click();
    await $(RouteComparison2Page.answer()).setValue(2);
    await $(RouteComparison2Page.submit()).click();
    await expect(await $("#main-content > p").getText()).to.contain("This page should never be skipped");
  });

  it("Given we start the routing test survey, When we enter a high number then a low number, Then, we should be routed to the third page", async () => {
    await $(RouteComparison1Page.answer()).setValue(1);
    await $(RouteComparison1Page.submit()).click();
    await $(RouteComparison2Page.answer()).setValue(0);
    await $(RouteComparison2Page.submit()).click();
    await expect(await $("#main-content > p").getText()).to.contain("This page should be skipped if your second answer was higher than your first");
  });

  it("Given we start the routing test survey, When we enter an equal number on both questions, Then, we should be routed to the third page", async () => {
    await $(RouteComparison1Page.answer()).setValue(1);
    await $(RouteComparison1Page.submit()).click();
    await $(RouteComparison2Page.answer()).setValue(1);
    await $(RouteComparison2Page.submit()).click();
    await expect(await $("#main-content > p").getText()).to.contain("This page should be skipped if your second answer was higher than your first");
  });
});
