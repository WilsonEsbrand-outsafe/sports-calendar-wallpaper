// tools/jamsil/jamsil.svg → assets/stadium/jamsil.jpg (2560x1440)
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const svg = path.join(__dirname, 'jamsil.svg');
  const out = path.join(__dirname, '..', '..', 'assets', 'stadium', 'jamsil.jpg');
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 2560, height: 1440 } });
  await page.goto('file://' + svg);
  await page.screenshot({ path: out, type: 'jpeg', quality: 90 });
  await browser.close();
  console.log(out);
})();
