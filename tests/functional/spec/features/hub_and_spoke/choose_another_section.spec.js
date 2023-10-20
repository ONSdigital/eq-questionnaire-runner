import EmploymentStatusBlockPage from "../../../generated_pages/hub_and_spoke/employment-status.page.js";
import ProxyPage from "../../../generated_pages/hub_and_spoke/proxy.page.js";
import HubPage from "../../../base_pages/hub.page.js";
import { click } from "../../../helpers";
describe("Choose another section link", () => {
  it("When a user first views the Hub, then the link should not be displayed", async () => {
    await browser.openQuestionnaire("test_hub_and_spoke.json");
    await expect(await $("body").getText()).not.toContain("Choose another section and return to this later");
  });

  it("When a user views the first question and the hub is not available, then the link should not be displayed", async () => {
    await browser.openQuestionnaire("test_hub_complete_sections.json");
    await expect(await $("body").getText()).not.toContain("Choose another section and return to this later");
  });

  it("When a user starts a new section and the hub is available, then the link should be displayed", async () => {
    await browser.openQuestionnaire("test_hub_complete_sections.json");
    await $(EmploymentStatusBlockPage.workingAsAnEmployee()).click();
    await click(EmploymentStatusBlockPage.submit());
    await $(HubPage.summaryRowLink("accommodation-section")).click();
    await expect(await $("body").getText()).toContain("Choose another section and return to this later");
  });

  it("When a user gets to a section summary and the hub is available, then the link should not be displayed", async () => {
    await browser.openQuestionnaire("test_hub_complete_sections.json");
    await $(EmploymentStatusBlockPage.workingAsAnEmployee()).click();
    await click(EmploymentStatusBlockPage.submit());
    await $(HubPage.summaryRowLink("accommodation-section")).click();
    await $(ProxyPage.noIMAnsweringForMyself()).click();
    await click(ProxyPage.submit());
    await expect(await $("body").getText()).not.toContain("Choose another section and return to this later");
  });
});
