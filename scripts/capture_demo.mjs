import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "playwright";

const targets = [
  { name: "golibrary.xyz", url: "https://golibrary.xyz/" },
  { name: "lingxilearn.cn", url: "https://lingxilearn.cn" },
  { name: "christmas1314.xyz", url: "https://christmas1314.xyz" },
  { name: "lyyzka.xyz", url: "https://lyyzka.xyz/" },
  { name: "gen.letsapi.store", url: "https://gen.letsapi.store/overview" },
];

const outputDir = process.argv[2] ? path.resolve(process.argv[2]) : path.resolve("demo-captures");
await fs.mkdir(outputDir, { recursive: true });

const launchOptions = { headless: true };
if (process.env.PLAYWRIGHT_CHANNEL) {
  launchOptions.channel = process.env.PLAYWRIGHT_CHANNEL;
}

const browser = await chromium.launch(launchOptions);
const page = await browser.newPage({
  viewport: { width: 1440, height: 900 },
  deviceScaleFactor: 1,
});

const manifest = [];

for (const target of targets) {
  const fileName = `${target.name.replace(/[^a-z0-9.-]/gi, "_")}.png`;
  const filePath = path.join(outputDir, fileName);
  try {
    await page.goto(target.url, { waitUntil: "domcontentloaded", timeout: 30000 });
    await page.waitForTimeout(2500);
    await page.screenshot({ path: filePath, fullPage: false });
    manifest.push({ ...target, fileName, ok: true });
  } catch (error) {
    manifest.push({
      ...target,
      fileName,
      ok: false,
      error: error instanceof Error ? error.message : String(error),
    });
  }
}

await browser.close();
await fs.writeFile(path.join(outputDir, "manifest.json"), JSON.stringify(manifest, null, 2));
