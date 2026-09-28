# CourtListener Scraper: US Case Law & Court Dockets

Search US federal and state court opinions, dockets, and case law from CourtListener. Returns case name, court, judge, date, citations, and direct URLs. No API key required. Pay only per record returned.

**Run it on Apify:** [apify.com/themineworks/courtlistener-court-records](https://apify.com/themineworks/courtlistener-court-records)
**Docs, FAQ and pricing:** [themineworks.com/actors/courtlistener-court-records](https://themineworks.com/actors/courtlistener-court-records/)

**Price:** From $0.60 per 1,000 records on Apify's higher plans ($1.00 on the free plan), plus a $0.005 start fee per run. Failed and empty results are never charged.

## What it returns

* Federal and state court opinions and dockets
* Case name, court, judge, and citation data
* Full-text search across millions of decisions
* Direct links to source documents
* Empty results are never charged

## Quick start

You need a free [Apify account](https://console.apify.com/sign-up) and its API token (Settings, API & Integrations).

### Python

```bash
pip install apify-client
```

```python
from apify_client import ApifyClient

client = ApifyClient("YOUR_APIFY_TOKEN")
run = client.actor("themineworks/courtlistener-court-records").call(run_input={
    "query": "patent infringement",
    "court": "scotus",
    "dateFrom": "2024-01-01",
    "dateTo": "2024-12-31"
})

for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)
```

### Node.js

```bash
npm install apify-client
```

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: 'YOUR_APIFY_TOKEN' });
const run = await client.actor('themineworks/courtlistener-court-records').call({
    "query": "patent infringement",
    "court": "scotus",
    "dateFrom": "2024-01-01",
    "dateTo": "2024-12-31"
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

### cURL

One request that runs the actor and returns the results in the response (for runs under 5 minutes):

```bash
curl -X POST "https://api.apify.com/v2/acts/themineworks~courtlistener-court-records/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "patent infringement", "court": "scotus", "dateFrom": "2024-01-01", "dateTo": "2024-12-31"}'
```

### Command line

This repo includes ready-made clients that save results to JSON and CSV:

```bash
python3 courtlistener_scraper.py --token YOUR_APIFY_TOKEN --query "patent infringement" --court "scotus" --date-from "2024-01-01" --date-to "2024-12-31"
node courtlistener_scraper.mjs --token YOUR_APIFY_TOKEN --query "patent infringement" --court "scotus" --date-from "2024-01-01" --date-to "2024-12-31"
```

## Input

| Field | Type | Default | Description |
|---|---|---|---|
| `query` (required) | string |  | Words or a quoted phrase to search across case text (for example patent infringement, "summary judgment") |
| `resultType` | string | `"opinions"` | Opinions (case law) or RECAP dockets (federal case dockets) |
| `court` | string |  | Restrict to a court by CourtListener court id (for example scotus, ca9, ded) |
| `dateFrom` | string |  | Only cases filed on or after this date, for example "2024-01-01" |
| `dateTo` | string |  | Only cases filed on or before this date, for example "2024-12-31" |
| `maxResults` | integer | `5` | Maximum number of records to return |

## Output

One row per result, as JSON, CSV, Excel or through the API.

| Field | Type | Description |
|---|---|---|
| `case_name` | string | Short case name (for example Smith v |
| `case_name_full` | string | Full official case name |
| `court` | string | Court name (for example Court of Appeals for the Ninth Circuit) |
| `court_id` | string | CourtListener court identifier slug |
| `date_filed` | string | Date the case or opinion was filed (YYYY-MM-DD) |
| `date_argued` | string | Date oral arguments were heard (YYYY-MM-DD) |
| `docket_number` | string | Court docket number |
| `judge` | string | Authoring or presiding judge |
| `citations` | array | Reporter citations for this opinion |
| `cite_count` | number | Number of times this opinion has been cited |
| `status` | string | Publication status of the opinion (Published, Unpublished, etc.) |
| `nature_of_suit` | string | Nature of suit code or description |
| `cluster_id` | number | CourtListener opinion cluster ID |
| `docket_id` | number | CourtListener docket ID |
| `url` | string | Full URL to the record on CourtListener |
| `scraped_at` | string | ISO timestamp when this record was scraped |

## Use it from an AI agent

The actor works as a tool in Claude, Cursor or any MCP client through Apify's MCP server:

```
https://mcp.apify.com/?tools=themineworks/courtlistener-court-records
```

## FAQ

### What is CourtListener?

CourtListener is a free legal research platform run by the Free Law Project. It contains 10 million+ court opinions, dockets, and oral argument recordings from federal and state courts going back to 1754.

### Is CourtListener free to use?

Yes. CourtListener is a nonprofit platform with a free REST API. An API key is required for more than 1,000 requests per day, and registration is free.

### How is CourtListener different from PACER?

PACER is the official federal court system and charges $0.10 per page. CourtListener provides free access to opinions and some docket data. PACER filing documents (PDFs of motions, briefs) are still paywalled.

### What courts are covered?

All 13 US federal circuit courts, the Supreme Court, all 94 federal district courts, and a growing number of state appellate courts. Coverage depth varies by court.

### What data model does CourtListener use?

Three main entities: Docket (a case with all its filings), Cluster (a group of related opinions from the same case), and Opinion (a single written decision). Each opinion links back to its docket.

### How much does the CourtListener Scraper cost?

From $0.60 per 1,000 records on Apify's higher plans ($1.00 on the free plan), plus a $0.005 start fee per run. Failed and empty results are never charged. You can cap what a single run may spend with the maximum cost setting on Apify.

### Can I export the results to CSV or Excel?

Yes. Every run saves to an Apify dataset you can download as JSON, CSV, Excel or XML, or read through the API. The Python and Node clients in this repo also write the results to local files.

### Can I run it on a schedule?

Yes. Save your input as a task on Apify and attach a schedule, or call the API from your own cron job. Scheduled runs are billed the same way as manual ones.

## Related scrapers

* [India Gov Data](https://themineworks.com/actors/india-data-gov-scraper/): Trade, prices, and thousands of datasets from data.gov.in
* [Socrata Open Data](https://themineworks.com/actors/socrata-open-data/): Any government data portal: CDC, HHS, NYC, Texas, and hundreds more
* [FDA 510(k) Scraper](https://themineworks.com/actors/fda-510k-device-clearances/): Medical device clearances by company, device, or code

Part of [The Mine Works](https://themineworks.com/): 151 pay-per-result scrapers with no login and no browser setup on your side.

## License

MIT © The Mine Works
