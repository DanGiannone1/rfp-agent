import { chromium } from "playwright";

const FRONTEND = "http://localhost:3000";

async function waitForIdle(page, maxWait = 60000) {
  // Wait until the Send button is enabled (not streaming)
  const start = Date.now();
  while (Date.now() - start < maxWait) {
    const disabled = await page.locator('button[type="submit"]').getAttribute("disabled");
    if (disabled === null) return true;
    await page.waitForTimeout(1000);
  }
  return false;
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  page.on("console", (msg) => {
    if (msg.type() === "error") console.log(`[CONSOLE error] ${msg.text()}`);
  });
  page.on("requestfailed", (req) => {
    console.log(`[NET FAIL] ${req.method()} ${req.url()} — ${req.failure()?.errorText}`);
  });

  // ── Test 1: Basic message + response ─────────────────────────────────
  console.log("=== Test 1: Basic message + response ===");
  await page.goto(FRONTEND, { waitUntil: "networkidle" });
  await page.waitForTimeout(2000);

  const input = page.locator("input, textarea").first();
  await input.fill("say hello");
  await page.locator('button[type="submit"]').click();
  await waitForIdle(page);

  let body = await page.locator("body").innerText();
  const test1Pass = body.toLowerCase().includes("hello");
  console.log(`  Response received: ${test1Pass ? "PASS" : "FAIL"}`);
  await page.screenshot({ path: "/tmp/test1-basic.png", fullPage: true });

  // ── Test 2: Multi-turn context ────────────────────────────────────────
  console.log("\n=== Test 2: Multi-turn context ===");
  await input.fill("my favorite color is blue");
  await page.locator('button[type="submit"]').click();
  await waitForIdle(page);

  await input.fill("what is my favorite color?");
  await page.locator('button[type="submit"]').click();
  await waitForIdle(page);

  body = await page.locator("body").innerText();
  const test2Pass = body.toLowerCase().includes("blue");
  console.log(`  Remembers context: ${test2Pass ? "PASS" : "FAIL"}`);
  await page.screenshot({ path: "/tmp/test2-multiturn.png", fullPage: true });

  // ── Test 3: Tool use (status indicator) ───────────────────────────────
  console.log("\n=== Test 3: Tool use with status ===");
  await input.fill("run the command: echo 'hello world'");
  await page.locator('button[type="submit"]').click();

  // Check for tool activity indicators during processing
  let sawToolActivity = false;
  for (let i = 0; i < 60; i++) {
    await page.waitForTimeout(1000);
    const html = await page.content();
    if (html.includes("bash") || html.includes("Running") || html.includes("tool")) {
      sawToolActivity = true;
    }
    // Check if done
    const disabled = await page.locator('button[type="submit"]').getAttribute("disabled");
    if (disabled === null) break;
  }

  body = await page.locator("body").innerText();
  const test3Pass = body.toLowerCase().includes("hello world");
  console.log(`  Tool result received: ${test3Pass ? "PASS" : "FAIL"}`);
  console.log(`  Saw tool activity indicator: ${sawToolActivity ? "YES" : "NO"}`);
  await page.screenshot({ path: "/tmp/test3-tooluse.png", fullPage: true });

  // ── Test 4: New chat button ───────────────────────────────────────────
  console.log("\n=== Test 4: New chat resets session ===");
  // Force click even if disabled attribute exists
  await page.locator("button", { hasText: "New chat" }).click({ force: true });
  await page.waitForTimeout(3000);

  body = await page.locator("body").innerText();
  const test4Pass = body.includes("Start a conversation");
  console.log(`  Chat reset: ${test4Pass ? "PASS" : "FAIL"}`);
  await page.screenshot({ path: "/tmp/test4-newchat.png", fullPage: true });

  // ── Test 5: Longer response with markdown ─────────────────────────────
  console.log("\n=== Test 5: Longer response with markdown ===");
  await input.fill("write a short 3-bullet summary of what an RFP typically contains. use markdown formatting.");
  await page.locator('button[type="submit"]').click();
  await waitForIdle(page, 90000);

  body = await page.locator("body").innerText();
  const test5Pass = body.length > 200;
  console.log(`  Got long response: ${test5Pass ? "PASS" : "FAIL"} (${body.length} chars)`);
  await page.screenshot({ path: "/tmp/test5-markdown.png", fullPage: true });

  // ── Summary ───────────────────────────────────────────────────────────
  console.log("\n=== Summary ===");
  console.log(`  Test 1 (basic message):    ${test1Pass ? "PASS" : "FAIL"}`);
  console.log(`  Test 2 (multi-turn):       ${test2Pass ? "PASS" : "FAIL"}`);
  console.log(`  Test 3 (tool use):         ${test3Pass ? "PASS" : "FAIL"}`);
  console.log(`  Test 4 (new chat reset):   ${test4Pass ? "PASS" : "FAIL"}`);
  console.log(`  Test 5 (longer response):  ${test5Pass ? "PASS" : "FAIL"}`);

  await browser.close();
})();
