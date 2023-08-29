import EmploymentStatusBlockPage from "../../../generated_pages/hub_and_spoke/employment-status.page.js";
import EmploymentTypePage from "../../../generated_pages/hub_and_spoke/employment-type.page.js";
import HubPage from "../../../base_pages/hub.page.js";
import ProxyPage from "../../../generated_pages/hub_and_spoke/proxy.page.js";
import { click } from "../../../helpers";
const schema = "test_hub_complete_sections.json";
describe("Choose another section link", () => {
  beforeEach(async () => {
    await browser.openQuestionnaire(schema);
  });

  it("When a user gets to initial question, then the previous location link should not be displayed", async () => {
    await expect(await $(EmploymentStatusBlockPage.previous()).isExisting()).to.be.false;
  });

  it("When a user gets to the hub, then the previous location link should not be displayed", async () => {
    await $(EmploymentStatusBlockPage.workingAsAnEmployee()).click();
    await click(EmploymentStatusBlockPage.submit());
    await expect(await $(HubPage.previous()).isExisting()).to.be.false;
  });

  it("When a user gets to subsequent question, then the previous location link should be displayed", async () => {
    await $(EmploymentStatusBlockPage.exclusiveNoneOfTheseApply()).click();
    await click(EmploymentStatusBlockPage.submit());
    await expect(await $(EmploymentTypePage.previous()).isExisting()).to.be.true;
  });

  it("When a user gets to subsequent questions past the hub, then the previous location link should be displayed", async () => {
    await $(EmploymentStatusBlockPage.workingAsAnEmployee()).click();
    await click(EmploymentStatusBlockPage.submit());
    await $(HubPage.summaryRowLink("accommodation-section")).click();
    await expect(await $(ProxyPage.previous()).isExisting()).to.be.true;
  });
});
