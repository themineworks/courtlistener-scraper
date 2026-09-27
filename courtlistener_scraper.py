#!/usr/bin/env python3
"""US court opinions, dockets, and case law as structured JSON. Python, Node.js and cURL clients for the CourtListener Scraper on Apify, pay per result.

Command-line client for the themineworks/courtlistener-court-records actor on Apify: runs it, waits for it
to finish and saves every result as JSON and CSV. Flags map 1:1 to the actor's input.
Free Apify account and API token: https://console.apify.com/sign-up
Docs and pricing: https://themineworks.com/actors/courtlistener-court-records/
"""
import argparse, csv, json, os, sys
from apify_client import ApifyClient

ACTOR = "themineworks/courtlistener-court-records"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--token", default=os.environ.get("APIFY_TOKEN"), help="Apify API token (or set APIFY_TOKEN)")
    ap.add_argument("--out", default="results", help="Output basename, writes .json and .csv")
    ap.add_argument("--query", help="Words or a quoted phrase to search across case text (for example patent infringement…")
    ap.add_argument("--result-type", help="Opinions (case law) or RECAP dockets (federal case dockets)")
    ap.add_argument("--court", help="Restrict to a court by CourtListener court id (for example scotus, ca9, ded)")
    ap.add_argument("--date-from", help="Only cases filed on or after this date, for example '2024-01-01'")
    ap.add_argument("--date-to", help="Only cases filed on or before this date, for example '2024-12-31'")
    ap.add_argument("--max-results", type=int, help="Maximum number of records to return")
    a = ap.parse_args()
    if not a.token:
        sys.exit("Provide --token or set APIFY_TOKEN. Free token: https://console.apify.com/sign-up")

    run_input = {}
    if a.query is not None: run_input["query"] = a.query
    if a.result_type is not None: run_input["resultType"] = a.result_type
    if a.court is not None: run_input["court"] = a.court
    if a.date_from is not None: run_input["dateFrom"] = a.date_from
    if a.date_to is not None: run_input["dateTo"] = a.date_to
    if a.max_results is not None: run_input["maxResults"] = a.max_results

    client = ApifyClient(a.token)
    print(f"Running {ACTOR} ...")
    run = client.actor(ACTOR).call(run_input=run_input)
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

    with open(a.out + ".json", "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
    keys = []
    for it in items:
        keys += [k for k in it if k not in keys]
    if items:
        with open(a.out + ".csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
            w.writeheader()
            for it in items:
                w.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v for k, v in it.items()})
    print(f"Done: {len(items)} results saved to {a.out}.json and {a.out}.csv")


if __name__ == "__main__":
    main()
