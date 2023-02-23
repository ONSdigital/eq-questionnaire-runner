import EmploymentStatusBlockPage from "../../../generated_pages/hub_and_spoke/employment-status.page.js";
import ProxyPage from "../../../generated_pages/hub_and_spoke/proxy.page.js";
import HubPage from "../../../base_pages/hub.page.js";

describe("Choose another section link", () => {
  it("When a user first views the Hub, then the link should not be displayed", async () => {
    await browser.openQuestionnaire("test_hub_and_spoke.json");
    await expect(await $("body").getText()).to.not.have.string("Choose another section and return to this later");
  });

  it("When a user views the first question and the hub is not available, then the link should not be displayed", async () => {
    await browser.openQuestionnaire("test_hub_complete_sections.json");
    await expect(await $("body").getText()).to.not.have.string("Choose another section and return to this later");
  });

  it("When a user starts a new section and the hub is available, then the link should be displayed", async () => {
    await browser.openQuestionnaire("test_hub_complete_sections.json");
    await $(EmploymentStatusBlockPage.workingAsAnEmployee()).click();
    await $(EmploymentStatusBlockPage.submit()).click();
    await $(HubPage.summaryRowLink("accommodation-section")).click();
    await expect(await $("body").getText()).to.contain("Choose another section and return to this later");
  });

  it("When a user gets to a section summary and the hub is available, then the link should not be displayed", async () => {
    await browser.openQuestionnaire("test_hub_complete_sections.json");
    await $(EmploymentStatusBlockPage.workingAsAnEmployee()).click();
    await $(EmploymentStatusBlockPage.submit()).click();
    await $(HubPage.summaryRowLink("accommodation-section")).click();
    await $(ProxyPage.noIMAnsweringForMyself()).click();
    await $(ProxyPage.submit()).click();
    await expect(await $("body").getText()).to.not.have.string("Choose another section and return to this later");
  });
});
