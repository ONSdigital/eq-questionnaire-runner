import Block1Page from "../../../generated_pages/metadata_routing/block1.page";
import Block2Page from "../../../generated_pages/metadata_routing/block2.page";
import Block3Page from "../../../generated_pages/metadata_routing/block3.page";
import { click, verifyUrlContains } from "../../../helpers";

describe("Feature: Routing - Boolean Flag", () => {
  it("Given I have a routing rule that uses a boolean flag and it is False, When I press continue, Then I should be routed to the correct page", async () => {
    await browser.openQuestionnaire("test_metadata_routing.json", {
      booleanFlag: false,
    });
    await click(Block1Page.submit());
    await verifyUrlContains(Block2Page.pageName);
  });

  it("Given I have a routing rule that uses a boolean flag and it is True, When I press continue, Then I should be routed to the correct page ", async () => {
    await browser.openQuestionnaire("test_metadata_routing.json", {
      booleanFlag: true,
    });
    await click(Block1Page.submit());
    await verifyUrlContains(Block3Page.pageName);
  });
});
