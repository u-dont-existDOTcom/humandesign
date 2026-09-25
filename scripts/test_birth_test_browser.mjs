// Run against a local or deployed pilot with synthetic data only.
// PLAYWRIGHT_MODULE may name an installed playwright-core ESM module.
import assert from 'node:assert/strict';
import { writeFile, mkdir } from 'node:fs/promises';
import { pathToFileURL } from 'node:url';
const modulePath = process.env.PLAYWRIGHT_MODULE || 'playwright-core';
const { chromium } = await import(modulePath.startsWith('/') ? pathToFileURL(modulePath).href : modulePath);
const base = process.env.BIRTH_TEST_BASE_URL || 'http://127.0.0.1:8094';
const output = process.env.BIRTH_TEST_BROWSER_OUTPUT || '/tmp/birth-test-browser';
await mkdir(output, { recursive: true });
const browser = await chromium.launch({ headless: true, executablePath: process.env.BROWSER_EXECUTABLE || '/usr/bin/brave-browser' });
const context = await browser.newContext({ viewport: { width: 1100, height: 900 } });
const page = await context.newPage();
const errors = [];
page.on('pageerror', error => errors.push(error.message));
const state = () => page.evaluate(() => JSON.parse(localStorage.getItem('life-patterns-birth-test-v15')));
try {
  await page.goto(base + '/birth-test', { waitUntil: 'networkidle' });
  await page.waitForSelector('#domain-insight_translation');
  assert.match(await page.locator('#question').innerText(), /worked out why two sets of plans/);
  await page.locator('#consent').check();
  await page.locator('#answer').fill('Synthetic browser fixture: I explain the discrepancy.');
  await page.locator('#next').click();
  await page.locator('#previous').click();
  assert.equal(await page.locator('#answer').inputValue(), 'Synthetic browser fixture: I explain the discrepancy.');
  await page.locator('#latitude').fill('39.9526');
  await page.locator('#longitude').fill('-75.1652');
  await page.locator('#timezone').fill('America/New_York');
  for (const id of ['insight_translation', 'retreat_privacy', 'romantic_attachment', 'persuasion_strategy', 'recognition_entry']) {
    await page.locator('#domain-' + id).selectOption('supported');
  }
  await page.locator('#reviewed').check();
  await page.locator('#run').click();
  await page.waitForFunction(() => !document.getElementById('result-section').classList.contains('hidden'), { timeout: 60000 });
  const first = (await state()).run;
  assert.equal(first.decoy_count, 999);
  assert.deepEqual(first.answer_signs, [1, 1, 1, 1, 1, 1]);
  await page.locator('#birth-local').fill('1985-01-29T05:25:00');
  await page.locator('#time-source').selectOption('record');
  await page.locator('#check').click();
  await page.waitForFunction(() => document.getElementById('checked-result').innerText.includes('Your score is 6'), { timeout: 60000 });
  const checked = (await state()).check;
  assert.equal(checked.score, 6);
  await page.locator('#answer').fill('Synthetic edited fixture: I keep the explanation to myself.');
  assert.equal(await page.locator('#reviewed').isChecked(), false);
  assert.equal(await page.locator('#result-section').isVisible(), false);
  let current = await state();
  assert.equal(current.run, null);
  assert.equal(current.history.at(-1).run.profile_sha256, first.profile_sha256);
  assert.equal(current.history.at(-1).profile.insight_translation, 'supported');
  await page.locator('#domain-insight_translation').selectOption('contradicted');
  await page.locator('#reviewed').check();
  await page.locator('#run').click();
  await page.waitForFunction(() => !document.getElementById('result-section').classList.contains('hidden'), { timeout: 60000 });
  const second = (await state()).run;
  assert.equal(second.model_id, first.model_id);
  assert.notEqual(second.profile_sha256, first.profile_sha256);
  assert.equal(second.result_class, 'EXPLORATORY_AFTER_REVEAL');
  assert.deepEqual(second.answer_signs, [-1, 1, 1, 1, 1, 1]);
  await page.locator('#check').click();
  await page.waitForFunction(() => document.getElementById('checked-result').innerText.includes('Your score is 4'), { timeout: 60000 });
  const secondCheck = (await state()).check;
  assert.equal(secondCheck.score, 4);
  // A delayed suggested interpretation must not overwrite subsequently edited answers.
  await page.locator('#model-consent').check();
  let resolveRequest;
  const received = new Promise(resolve => { resolveRequest = resolve; });
  await page.route('**/birth-test/api/interpret', route => resolveRequest(route));
  await page.locator('#suggest').click();
  const intercepted = await received;
  await page.locator('#answer').fill('Synthetic newer text entered while the interpretation was pending.');
  await intercepted.fulfill({ contentType: 'application/json', body: JSON.stringify({ interpretations: [], source_answers_sha256: '0'.repeat(64), review_required: true }) });
  await page.waitForFunction(() => document.getElementById('interpret-status').innerText.includes('old suggestion was not applied'));
  assert.equal((await state()).suggestions.length, 0);
  await page.setViewportSize({ width: 390, height: 844 });
  await page.locator('#answer-section').scrollIntoViewIfNeeded();
  await page.screenshot({ path: output + '/mobile.png' });
  assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1), true);
  assert.deepEqual(errors, []);
  const receipt = { status: 'PASS', data_class: 'SYNTHETIC_BROWSER_FIXTURE_NOT_HUMAN_VALIDATION',
    base_url: base, default_decoys: first.decoy_count, original_score: checked.score,
    changed_answer_score: secondCheck.score, original_rank: [checked.rank_best, checked.rank_worst],
    changed_answer_rank: [secondCheck.rank_best, secondCheck.rank_worst],
    model_unchanged: first.model_id === second.model_id, profile_hash_changed: first.profile_sha256 !== second.profile_sha256,
    original_inputs_preserved: true, stale_interpretation_discarded: true,
    old_ranking_invalidated_on_edit: true, mobile_horizontal_overflow: false, page_errors: errors,
    observed_utc: new Date().toISOString() };
  await writeFile(output + '/result.json', JSON.stringify(receipt, null, 2));
  console.log(JSON.stringify(receipt));
  await page.request.delete(base + '/birth-test/api/run/' + first.run_id);
  await page.request.delete(base + '/birth-test/api/run/' + second.run_id);
} finally {
  await context.close();
  await browser.close();
}
