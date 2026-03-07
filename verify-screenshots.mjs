import { chromium } from 'playwright';

const API_BASE = 'http://localhost:8000';

async function main() {
  const browser = await chromium.launch({ headless: true });

  // ── Screenshot 1: Intake screen ──────────────────────────────────────────
  {
    const page = await browser.newPage();
    await page.setViewportSize({ width: 1400, height: 900 });
    await page.goto('http://localhost:3000', { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.evaluate(() => sessionStorage.clear());
    // Block createSession so intake stays showing (don't let it transition to chat)
    await page.route(`${API_BASE}/sessions`, async route => {
      if (route.request().method() === 'POST') {
        // Hang — we just want to take an intake screenshot
        // Actually, fulfill slowly. Let's just not respond so page stays on intake.
        // We'll abort to show error state? No — let's delay 5s, take screenshot first.
        await new Promise(r => setTimeout(r, 10000));
        await route.fulfill({ status: 503, body: 'unavailable' });
      } else {
        await route.continue();
      }
    });
    await page.goto('http://localhost:3000', { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(500);
    await page.screenshot({ path: '/tmp/verify-intake.png', fullPage: false });
    console.log('intake done');
    await page.close();
  }

  // ── Screenshot 2 & 3: Chat empty state + Canvas ─────────────────────────
  {
    const page = await browser.newPage();
    await page.setViewportSize({ width: 1400, height: 900 });

    // Mock session status — note: must return session_id not id
    await page.route(`${API_BASE}/sessions/ui-verify-01`, async route => {
      const url = route.request().url();
      console.log('session route hit:', url);
      if (url.includes('/files/content')) {
        // Should not land here; handled below
        await route.continue();
        return;
      }
      if (url.endsWith('/ui-verify-01')) {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({ session_id: 'ui-verify-01', status: 'ready' }),
        });
      } else {
        await route.continue();
      }
    });

    // Mock files list
    await page.route(`${API_BASE}/sessions/ui-verify-01/files`, async route => {
      const url = route.request().url();
      console.log('files route hit:', url);
      if (url.includes('/content')) {
        await route.continue();
        return;
      }
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          files: [
            { filename: 'RFP-2024-Q4.pdf', size: 524288, modified_at: '2026-03-07T10:00:00Z', has_markdown: true, origin: 'uploaded' },
            { filename: 'compliance_matrix.md', size: 12340, modified_at: '2026-03-07T10:30:00Z', has_markdown: false, origin: 'generated' },
            { filename: 'bid_score.md', size: 3210, modified_at: '2026-03-07T10:31:00Z', has_markdown: false, origin: 'generated' }
          ]
        }),
      });
    });

    // Mock file content
    await page.route(`${API_BASE}/sessions/ui-verify-01/files/content*`, async route => {
      console.log('file content route hit:', route.request().url());
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          filename: 'compliance_matrix.md',
          size: 12340,
          mime_type: 'text/markdown',
          content: '# Compliance Matrix\n\n## Summary\nAll mandatory requirements mapped.\n\n| Requirement | Owner | Status |\n|---|---|---|\n| Staffing plan | HR | Met |\n| Past performance | BD | Met |\n| Price proposal | Finance | Partial |\n\n## Risks\n- Staffing timeline is tight\n- Price ceiling may be exceeded'
        }),
      });
    });

    // Navigate, seed session, reload
    await page.goto('http://localhost:3000', { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.evaluate(() => sessionStorage.clear());
    await page.evaluate(() => sessionStorage.setItem('rfp_agent_session_id', 'ui-verify-01'));
    await page.reload({ waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(1500);

    // List all testids
    const allTestIds = await page.locator('[data-testid]').evaluateAll(els =>
      els.map(el => el.getAttribute('data-testid'))
    );
    console.log('All data-testids:', allTestIds);

    await page.screenshot({ path: '/tmp/verify-chat.png', fullPage: false });
    console.log('chat done');

    const docItems = page.locator('[data-testid="document-item"]');
    const count = await docItems.count();
    console.log(`document-item count: ${count}`);

    if (count > 0) {
      await docItems.first().click();
      await page.waitForTimeout(1500);
    } else {
      console.log('No document-item found — trying documents-drawer to open panel');
      const drawer = page.locator('[data-testid="documents-drawer"]');
      const drawerCount = await drawer.count();
      console.log('documents-drawer count:', drawerCount);
      if (drawerCount > 0) {
        await drawer.first().click();
        await page.waitForTimeout(800);
        const docItemsAfter = page.locator('[data-testid="document-item"]');
        const countAfter = await docItemsAfter.count();
        console.log(`document-item count after drawer click: ${countAfter}`);
        if (countAfter > 0) {
          await docItemsAfter.first().click();
          await page.waitForTimeout(1500);
        }
      }
    }

    await page.screenshot({ path: '/tmp/verify-canvas.png', fullPage: false });
    console.log('canvas done');

    await page.close();
  }

  await browser.close();
  console.log('All screenshots saved.');
}

main().catch(err => { console.error(err); process.exit(1); });
