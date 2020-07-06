import EmploymentStatusBlockPage from "../../../generated_pages/hub_and_spoke/employment-status.page.js";
import EmploymentTypePage from "../../../generated_pages/hub_and_spoke/employment-type.page.js";
import HubPage from "../../../base_pages/hub.page.js";
import ProxyPage from "../../../generated_pages/hub_and_spoke/proxy.page.js";
const schema = "test_hub_complete_sections.json";

describe("Choose another section link", () => {
  beforeEach(() => {
    browser.openQuestionnaire(schema);
  });

  it("When a user gets to initial question, then the previous location link should not be displayed", () => {
    expect($(EmploymentStatusBlockPage.previous()).isExisting()).to.be.false;
  });

  it("When a user gets to the hub, then the previous location link should not be displayed", () => {
    $(EmploymentStatusBlockPage.workingAsAnEmployee()).click();
    $(EmploymentStatusBlockPage.submit()).click();
    expect($(HubPage.previous()).isExisting()).to.be.false;
  });

  it("When a user gets to subsequent question, then the previous location link should be displayed", () => {
    $(EmploymentStatusBlockPage.exclusiveNoneOfTheseApply()).click();
    $(EmploymentStatusBlockPage.submit()).click();
    expect($(EmploymentTypePage.previous()).isExisting()).to.be.true;
  });

  it("When a user gets to subsequent questions past the hub, then the previous location link should be displayed", () => {
    $(EmploymentStatusBlockPage.workingAsAnEmployee()).click();
    $(EmploymentStatusBlockPage.submit()).click();
    $(HubPage.summaryRowLink("accommodation-section")).click();
    expect($(ProxyPage.previous()).isExisting()).to.be.true;
  });
});
