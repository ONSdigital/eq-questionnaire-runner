import Block1Page from "../../../generated_pages/metadata_routing/block1.page"
import Block2Page from "../../../generated_pages/metadata_routing/block2.page"
import Block3Page from "../../../generated_pages/metadata_routing/block3.page"
import { click } from "../../../helpers";

describe("Feature: Routing - Boolean Flag", () =>{
    it("Given Boolean Flag is False, When I press continue, Then I should be taken to the Block2Page", async ()=> {
        await browser.openQuestionnaire("test_metadata_routing.json",{
            booleanFlag: false,
        });
        await click(Block1Page.submit());
        await expect(browser).toHaveUrlContaining(Block2Page.pageName);
    })

    it("Given Boolean Flag is True, When I press continue, Then I should skip Block2Page and be taken to Block3Page", async() =>{
        await browser.openQuestionnaire("test_metadata_routing.json",{
            booleanFlag: true
        });
        await click(Block1Page.submit());
        await expect(browser).toHaveUrlContaining(Block3Page.pageName);
    })
})