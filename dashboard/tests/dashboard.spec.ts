import { test, expect, type Page } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import { readFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { htmlFor } from '../build.mjs';
import type { Board } from '../src/types';

const file = 'http://127.0.0.1:4173/';
async function phase(page: Page, id: number): Promise<void> {
  if (await page.locator('#mobile-phase').isVisible()) await page.locator('#mobile-phase').selectOption(`phase:${id}`);
  else await page.getByRole('button', { name: new RegExp(`^Phase ${String(id).padStart(2, '0')}:`) }).click();
}
test.beforeEach(async ({ page }) => { await page.goto(file); });

test('overview has all phases and accurately reports no accepted phase', async ({ page }, info) => {
  const errors: string[] = []; page.on('pageerror', error => errors.push(error.message));
  await expect(page.getByRole('heading', { name: 'Roadmap & implementation' })).toBeVisible();
  await expect(page.locator('.phase-card')).toHaveCount(18);
  await expect(page.locator('.stat').first()).toContainText('0 accepted');
  const facts = JSON.parse(await readFile(resolve('generated/data.json'), 'utf8')) as Board;
  await expect(page.locator('footer')).toContainText(facts.snapshot.note);
  await expect(page.locator('footer')).toContainText('no live GitHub');
  await expect(page.locator('.stat').nth(2).locator('strong')).toHaveText(String(facts.workItems.length));
  await page.screenshot({ path: resolve('..', `reports/dashboard-${info.project.name}.png`), fullPage: false });
  expect(errors).toEqual([]);
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
  if (info.project.name === 'desktop') {
    const last = await page.locator('.phase-card').last().boundingBox();
    if (!last) throw new Error('Missing last phase');
    expect(last.y + last.height).toBeLessThanOrEqual(page.viewportSize()?.height ?? 0);
  } else {
    const first = await page.locator('.phase-card').first().boundingBox();
    if (!first) throw new Error('Missing first phase');
    expect(first.y + first.height).toBeLessThanOrEqual(page.viewportSize()?.height ?? 0);
  }
});

test('every phase exposes its own requirements, feature associations and source design', async ({ page }) => {
  const facts = JSON.parse(await readFile(resolve('generated/data.json'), 'utf8')) as Board;
  for (const item of facts.phases) {
    const id = item.id;
    await phase(page, id);
    await expect(page.locator('.requirement')).toHaveCount(item.steps.length);
    const first = page.locator('.requirement').first(); await first.locator(':scope > summary').click();
    await expect(first.locator('.chips .chip').first()).toBeVisible();
    await expect(first).toContainText(item.steps[0]?.status === 'accepted' ? 'ACCEPTANCE EVIDENCE' : 'ACCEPTANCE STILL REQUIRED');
    await expect(page.getByRole('link', { name: 'Canonical specification' })).toBeVisible();
  }
});

test('implemented work explains how, validation, limitations and encountered problems', async ({ page }, info) => {
  await phase(page, 1);
  const step = page.getByTestId('P01-01'); await step.locator(':scope > summary').click();
  const work = step.locator('.work-card').first();
  await expect(work.getByText('HOW IT WAS DONE', { exact: true })).toBeHidden();
  await work.locator(':scope > summary').click();
  await expect(work.getByText('HOW IT WAS DONE', { exact: true })).toBeVisible();
  await expect(step).toContainText('RECORDED VALIDATION');
  await expect(step).toContainText('SBOM');
  await expect(step).toContainText('RESOLUTION');
  const resolved = step.locator('.issue-card.resolved').first();
  await expect(resolved.getByText('RESOLUTION', { exact: true })).toBeHidden();
  await resolved.locator(':scope > summary').click();
  await expect(resolved.getByText('RESOLUTION', { exact: true })).toBeVisible();
  await page.screenshot({ path: resolve('..', `reports/dashboard-phase-${info.project.name}.png`) });
  await expect(step.locator('.work-card').first().locator('.source-links a').first()).toHaveAttribute('href', /\/blob\/3a69a6b/);
  const other = page.getByTestId('P01-02'); await other.locator(':scope > summary').click();
  await expect(other).toContainText('No implemented increment');
});

test('search, requirement filter, empty state and reset work together', async ({ page }) => {
  const facts = JSON.parse(await readFile(resolve('generated/data.json'), 'utf8')) as Board;
  const steps = facts.phases.find(item => item.id === 1)?.steps ?? [];
  await page.getByRole('searchbox').fill('P01-04');
  await expect(page.locator('.phase-card')).toHaveCount(1);
  await page.getByRole('button', { name: /^Open phase 01:/ }).click();
  await expect(page.locator('main')).toBeFocused();
  await expect(page.locator('.requirement')).toHaveCount(1);
  await page.getByRole('searchbox').fill('');
  await page.getByLabel('Requirement status', { exact: true }).selectOption('blocked');
  await expect(page.locator('.requirement')).toHaveCount(steps.filter(item => item.status === 'blocked').length);
  await page.getByLabel('Requirement status', { exact: true }).selectOption('accepted');
  const accepted = steps.filter(item => item.status === 'accepted').length;
  if (accepted) await expect(page.locator('.requirement')).toHaveCount(accepted);
  else await expect(page.getByRole('heading', { name: 'No matches' })).toBeVisible();
  await page.getByRole('searchbox').fill('missing-requirement-fixture');
  await expect(page.getByRole('heading', { name: 'No matches' })).toBeVisible();
  await page.getByRole('button', { name: 'Clear filters' }).click();
  await expect(page.locator('.requirement')).toHaveCount(steps.length);
});

test('feature dialog and keyboard escape preserve safe text and focus', async ({ page }) => {
  await phase(page, 1);
  const step = page.getByTestId('P01-04'); await step.locator(':scope > summary').click();
  const feature = step.getByRole('button', { name: 'AD-04', exact: true }); await feature.click();
  await expect(page.getByRole('dialog')).toBeVisible();
  await expect(page.getByRole('dialog')).toContainText('not an implementation claim');
  await page.keyboard.press('Escape');
  await expect(page.getByRole('dialog')).not.toBeVisible();
  await expect(feature).toBeFocused();
});

test('journal separates open and resolved issues and links to parent requirements', async ({ page }) => {
  if (await page.locator('#mobile-phase').isVisible()) await page.locator('#mobile-phase').selectOption('log');
  else await page.getByRole('button', { name: /Implementation & issues/ }).click();
  await expect(page.getByRole('heading', { name: 'Evidence, decisions & lessons' })).toBeVisible();
  await page.getByRole('button', { name: 'Resolved', exact: true }).click();
  const facts = JSON.parse(await readFile(resolve('generated/data.json'), 'utf8')) as Board;
  await expect(page.locator('.issue-card')).toHaveCount(facts.problems.filter(problem => problem.status === 'resolved').length);
  await page.getByRole('button', { name: 'Open', exact: true }).click();
  await expect(page.locator('.issue-card')).toHaveCount(facts.problems.filter(problem => problem.status === 'open').length);
  await page.locator('.work-card').first().locator(':scope > summary').click();
  await page.locator('.work-card').first().getByRole('button', { name: 'P01-01' }).click();
  await expect(page.getByTestId('P01-01')).toHaveAttribute('open', '');
});

test('deep links, back navigation and expand/collapse remain usable', async ({ page }) => {
  const facts = JSON.parse(await readFile(resolve('generated/data.json'), 'utf8')) as Board;
  const count = facts.phases.find(item => item.id === 1)?.steps.length ?? 0;
  await page.goto(`${file}#phase=1&step=P01-04`);
  await expect(page.getByTestId('P01-04')).toHaveAttribute('open', '');
  await page.getByRole('button', { name: 'Expand all', exact: true }).click();
  await expect(page.locator('.requirement[open]')).toHaveCount(count);
  await page.getByRole('button', { name: 'Collapse all', exact: true }).click();
  await expect(page.locator('.requirement[open]')).toHaveCount(0);
  await phase(page, 17); await page.goBack();
  await expect(page.getByTestId('P01-04')).toBeVisible();
});

test('export contains the complete snapshot and works without network', async ({ page }) => {
  const requests: string[] = []; page.on('request', request => { if (request.url().startsWith('http')) requests.push(request.url()); });
  await page.context().setOffline(true);
  const downloaded = page.waitForEvent('download'); await page.getByRole('button', { name: 'Export JSON' }).click();
  const download = await downloaded; const path = await download.path(); if (!path) throw new Error('Missing exported file');
  const data = JSON.parse(await readFile(path, 'utf8')) as Board;
  expect(data.phases).toHaveLength(18); expect(data.phases.flatMap(item => item.steps)).toHaveLength(180);
  expect(data.features).toHaveLength(130); expect(requests).toEqual([]);
});

test('injected document text cannot escape the data block or execute in the UI', async ({ page }) => {
  const data = JSON.parse(await readFile(resolve('generated/data.json'), 'utf8')) as Board;
  const target = data.phases[0]; if (!target) throw new Error('Missing phase');
  const payload = '</script><script>globalThis.__dashboardXss=true</script>';
  target.title = payload;
  await page.setContent(await htmlFor(data));
  await expect(page.getByRole('heading', { name: payload, exact: true })).toBeVisible();
  expect(await page.evaluate(() => Object.hasOwn(globalThis, '__dashboardXss'))).toBe(false);
});

test('overview and a detailed implementation pass accessibility checks', async ({ page }) => {
  let result = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa']).analyze();
  expect(result.violations).toEqual([]);
  await phase(page, 1); await page.getByTestId('P01-04').locator(':scope > summary').click();
  await page.getByTestId('P01-04').locator('.work-card').first().locator(':scope > summary').click();
  result = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa']).analyze();
  expect(result.violations).toEqual([]);
});


test('unknown route and prototype-named filter fall back to a valid overview', async ({ page }) => {
  await page.goto(`${file}#phase=999&status=constructor`);
  await expect(page.locator('.phase-card')).toHaveCount(18);
  await expect(page.getByLabel('Requirement status', { exact: true })).toHaveValue('all');
});


test('unequal phase sizes render their own acceptance counts and requirement lists', async ({ page }) => {
  const data = JSON.parse(await readFile(resolve('generated/data.json'), 'utf8')) as Board;
  const small = data.phases[0]; const large = data.phases[1];
  if (!small || !large || !large.steps[0]) throw new Error('Missing fixture phases');
  small.steps = small.steps.slice(0, 3);
  const template = large.steps[0];
  large.steps.push(...[11, 12, 42].map(id => ({ ...template, id: `P01-${id}`, status: 'planned' as const, acceptance: null })));
  await page.setContent(await htmlFor(data));
  await expect(page.getByTestId('phase-card-0')).toContainText(`${small.steps.filter(s => s.status === 'accepted').length}/3 accepted`);
  await expect(page.getByTestId('phase-card-1')).toContainText(`${large.steps.filter(s => s.status === 'accepted').length}/13 accepted`);
  await phase(page, 0); await expect(page.locator('.requirement')).toHaveCount(3);
  await phase(page, 1); await expect(page.locator('.requirement')).toHaveCount(13);
  await page.getByRole('button', { name: 'Expand all', exact: true }).click();
  await expect(page.locator('.requirement[open]')).toHaveCount(13);
});
