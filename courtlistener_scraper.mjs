#!/usr/bin/env node
// Node.js client for the themineworks/courtlistener-court-records actor on Apify: runs it and saves results.json.
// Flags map 1:1 to the actor's input. Free API token: https://console.apify.com/sign-up
// Docs and pricing: https://themineworks.com/actors/courtlistener-court-records/
import { ApifyClient } from 'apify-client';
import { writeFileSync } from 'node:fs';

const ACTOR = 'themineworks/courtlistener-court-records';

function parseArgs(argv) {
    const out = {};
    for (let i = 0; i < argv.length; i++) {
        if (!argv[i].startsWith('--')) continue;
        const key = argv[i].slice(2);
        out[key] = argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[++i] : true;
    }
    return out;
}

const args = parseArgs(process.argv.slice(2));
const token = args.token || process.env.APIFY_TOKEN;
if (!token) {
    console.error('Provide --token or set APIFY_TOKEN. Free token: https://console.apify.com/sign-up');
    process.exit(1);
}

const runInput = {};
if (args['query'] !== undefined) runInput.query = String(args['query']);
if (args['result-type'] !== undefined) runInput.resultType = String(args['result-type']);
if (args['court'] !== undefined) runInput.court = String(args['court']);
if (args['date-from'] !== undefined) runInput.dateFrom = String(args['date-from']);
if (args['date-to'] !== undefined) runInput.dateTo = String(args['date-to']);
if (args['max-results'] !== undefined) runInput.maxResults = parseInt(args['max-results'], 10);

const client = new ApifyClient({ token });
console.log(`Running ${ACTOR} ...`);
const run = await client.actor(ACTOR).call(runInput);
const { items } = await client.dataset(run.defaultDatasetId).listItems();
writeFileSync('results.json', JSON.stringify(items, null, 2));
console.log(`Saved ${items.length} results to results.json`);
