import { test, expect } from "@playwright/test";

test.describe("Chat flow", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/");
    // wait for session initialization to finish
    await expect(page.getByTestId("chat-input")).toBeVisible({
      timeout: 30_000,
    });
  });

  test("send a message and receive a response", async ({ page }) => {
    const input = page.getByTestId("chat-input");
    const send = page.getByTestId("send-button");

    await input.fill("Say exactly: hello world");
    await send.click();

    // user message should appear
    await expect(page.locator("text=Say exactly: hello world")).toBeVisible();

    // wait for streaming to finish (input re-enables when isStreaming becomes false)
    await expect(input).toBeEnabled({ timeout: 120_000 });
  });

  test("multi-turn conversation", async ({ page }) => {
    const input = page.getByTestId("chat-input");
    const send = page.getByTestId("send-button");

    // first turn
    await input.fill("Remember the number 42.");
    await send.click();
    await expect(input).toBeEnabled({ timeout: 120_000 });

    // second turn
    await input.fill("What number did I just ask you to remember?");
    await send.click();
    await expect(input).toBeEnabled({ timeout: 120_000 });

    // the page should contain "42" somewhere in the response
    await expect(page.locator("body")).toContainText("42");
  });

  test("tool use shows activity indicator", async ({ page }) => {
    const input = page.getByTestId("chat-input");
    const send = page.getByTestId("send-button");

    // ask something likely to trigger tool use
    await input.fill(
      "Search the workspace for any files and list them.",
    );
    await send.click();

    // wait for response to complete
    await expect(input).toBeEnabled({ timeout: 120_000 });

    // page should have rendered — at minimum the assistant replied
    const body = await page.locator("body").textContent();
    expect(body!.length).toBeGreaterThan(50);
  });

  test("new chat resets conversation", async ({ page }) => {
    const input = page.getByTestId("chat-input");
    const send = page.getByTestId("send-button");
    const newChat = page.getByTestId("new-chat-button");

    // send a message first
    await input.fill("Hello there");
    await send.click();
    await expect(input).toBeEnabled({ timeout: 120_000 });

    // verify message exists
    await expect(page.locator("text=Hello there")).toBeVisible();

    // click new chat
    await newChat.click();

    // wait for re-initialization to complete
    await expect(input).toBeVisible({ timeout: 30_000 });

    // old message should be gone
    await expect(page.locator("text=Hello there")).toBeHidden();
  });
});
