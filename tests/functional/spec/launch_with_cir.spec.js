import { click, verifyUrlContains } from "../helpers";
import NameBlockPage from "../generated_pages/textfield/name-block.page.js";
import HubPage from "../base_pages/hub.page";
import ThankYouPage from "../base_pages/thank-you.page";

describe("Launch a survey from the collection instrument registry", () => {
  it("Given I retrieve a Collection Instrument, When I Launch, Then I am able to complete the survey as normal", async () => {
    await browser.openQuestionnaire(null, {
      version: "v2",
      cirInstrumentId: "fd4a527f-c126-da2d-8ee6-51663a43e416",
    });
    await verifyUrlContains(NameBlockPage.pageName);
    await $(NameBlockPage.name()).setValue("Joe");
    await click(NameBlockPage.submit());
    await click(HubPage.submit());
    await verifyUrlContains(ThankYouPage.pageName);
  });
});
