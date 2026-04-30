export async function checkPeopleInList(peopleExpected, listLabel) {
  await $(listLabel(1)).waitForDisplayed();

  for (let i = 1; i <= peopleExpected.length; i++) {
    expect(await $(listLabel(i)).getText()).to.equal(peopleExpected[i - 1]);
  }
}

export async function waitForPage(pagePath) {
  await browser.waitUntil(async () => (await browser.getUrl()).includes(pagePath), {
    timeout: 10000,
    timeoutMsg: `Expected to be on page ${pagePath}`,
  });
}

export async function waitForText(selector, expectedText) {
  await browser.waitUntil(async () => (await $(selector).getText()).includes(expectedText), {
    timeout: 10000,
    timeoutMsg: `Expected text '${expectedText}' for selector ${selector}`,
  });
}

