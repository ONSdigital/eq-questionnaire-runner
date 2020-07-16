import EmploymentStatusBlockPage from "../../../generated_pages/hub_and_spoke/employment-status.page.js";
import ProxyPage from "../../../generated_pages/hub_and_spoke/proxy.page.js";
import HubPage from "../../../base_pages/hub.page.js";

describe("Choose another section link", () => {
  it("When a user first views the Hub, then the link should not be displayed", () => {
    browser.openQuestionnaire("test_hub_and_spoke.json");
    expect($("body").getText()).to.not.have.string("Choose another section and return to this later");
  });

  it("When a user views the first question and the hub is not available, then the link should not be displayed", () => {
    browser.openQuestionnaire("test_hub_complete_sections.json");
    expect($("body").getText()).to.not.have.string("Choose another section and return to this later");
  });

  it("When a user starts a new section and the hub is available, then the link should be displayed", () => {
    browser.openQuestionnaire("test_hub_complete_sections.json");
    $(EmploymentStatusBlockPage.workingAsAnEmployee()).click();
    $(EmploymentStatusBlockPage.submit()).click();
    $(HubPage.summaryRowLink("accommodation-section")).click();
    expect($("body").getText()).to.contain("Choose another section and return to this later");
  });

  it("When a user gets to a section summary and the hub is available, then the link should not be displayed", () => {
    browser.openQuestionnaire("test_hub_complete_sections.json");
    $(EmploymentStatusBlockPage.workingAsAnEmployee()).click();
    $(EmploymentStatusBlockPage.submit()).click();
    $(HubPage.summaryRowLink("accommodation-section")).click();
    $(ProxyPage.noIMAnsweringForMyself()).click();
    $(ProxyPage.submit()).click();
    expect($("body").getText()).to.not.have.string("Choose another section and return to this later");
  });
});
