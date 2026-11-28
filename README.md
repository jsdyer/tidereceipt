# Tide Receipt

Save future astronomical tide predictions at seven Canadian stations, then match them to later CHS gauge readings.

Open https://coolcode.ca/tidereceipt/. To share a gauge, select it and copy the address. For example, [Halifax station 00490](https://coolcode.ca/tidereceipt/?station=00490) opens that station’s recent receipts. [Browse station summaries](https://coolcode.ca/tidereceipt/stations/) for the latest saved reading, recent comparisons and direct evidence. The method section links to the historical storm records for nearby Bedford Institute, which uses a separate gauge.

<!-- coolcode:guide -->
Choose a harbour to see how its latest measured water levels compared with predictions saved in advance. Each station summary links back to the gauge and the exact saved comparison. A prediction of 3.2 m followed by a 3.5 m gauge reading gives a −0.3 m signed difference. That residual includes non-tidal effects and is not a storm-surge forecast score.
<!-- /coolcode:guide -->

## Collection

No API key is required. Collection uses seven CHS IWLS stations (Charlottetown 01700, Churchill 05010, Halifax 00490, Port aux Basques 00665, Rimouski 02985, Saint John 00065 and Vancouver 07735), `wlp` predictions and `wlo` observations at hourly UTC timestamps. Both use local chart datum. Newly added gauges begin prospective comparison at their first saved prediction. Earlier observed levels can provide context but cannot produce a retrospective forecast score. If CHS returns no Halifax gauge readings, the site explicitly marks them unavailable and keeps its predictions pending; Vancouver is never substituted for Halifax. Future predictions span 72 hours; observations cover the preceding 14 days. Only observation QC flag `1` is scored. Forecast QC flag `2` is retained as metadata and does not imply an observed measurement.

Schedule: **Every six hours at minute 29 (UTC)**. GitHub schedules are best effort, not a precise timer. Scheduled and manual runs collect; code pushes and pull requests only validate/build the saved archive.

```sh
python3 scripts/collect.py
node --test tests/*.test.mjs
python3 -m unittest discover -s tests -v
python3 scripts/build.py
```

The default build is offline. Collectors validate before saving; failed collection does not replace the good deployment. All dated normalized receipts are permanent tracked files under `archive/YYYY-MM/*.json.gz`. Each includes the capture time, source URL, SHA-256 of the downloaded response, selected values and provenance. These files preserve the selected data, not necessarily the full upstream response. Identical receipts deduplicate; old receipts are never overwritten. No Zenodo configuration is needed.

The dashboard loads the most recent 14 days of captures. Older receipts remain downloadable through `data/archive.json` and retained in Git history. Every build regenerates the station directory, one HTML summary for each archived station and sitemap.xml. Each hourly comparison uses the latest prediction saved before its target. A recent range uses quality-flag-1 hourly readings in the 24 hours ending at the latest such reading. The archive is the durable record; Actions artifact retention is unrelated. Observation revisions remain in their dated source receipts; the dashboard uses the latest reading (or earliest stop encounter for transit). CSV export covers the selected receipt and filter. JSON and individual compressed receipt downloads preserve source links.

## Interpretation

A blank score means outcomes are missing, not zero error. A selected receipt's mean absolute difference is the mean of absolute matched differences; signed bias retains direction. Different receipts can refer to the same outcome, so points across receipts are not independent events. Live lead time is measured from capture to target.

## Publishing and monitoring

The main workflow checks models, collection logic, the static builder and browser behaviour, then commits new source receipts before deploying. Set repository Pages source to **GitHub Actions**. PRs cannot collect, commit or deploy. No Cloudflare Worker changes are required.

Optionally add an Actions secret **HEALTHCHECKS_PING_URL**. Scheduled/manual collection sends start/success/failure pings; the collector itself does not send email or accuracy reports. Match the Healthchecks schedule to the cron above and allow enough grace for GitHub queue delays (90 minutes is reasonable). A success ping confirms archive collection and commit; it does not certify forecast accuracy or Pages deployment.

Optional monitoring is inactive without the secret. The site reports the last successful collection and marks it overdue when stale.

## Privacy

Visitors load public saved data from this site. Filtering and CSV export run in the browser without accounts, storage or upstream API calls. The shared CoolCode counter records aggregate page opens without filter values. Source collection happens in GitHub Actions.

## Sources and attribution

CHS data: https://tides.gc.ca/en/web-services-offered-canadian-hydrographic-service

Licence: https://tides.gc.ca/en/licence-agreement

Contains information from the Canadian Hydrographic Service. This independent product is not an official navigational product. Predictions and observations retain source checksums and station identifiers.

## Software

Application code is MIT licensed. Upstream datasets retain their original licences. Browser screenshots are saved as seven-day CI artifacts; all data receipts remain in the repository.

<!-- schedule-reliability -->
## Schedule reliability

Public GitHub repositories can have scheduled workflows disabled after 60 days of inactivity. A separate weekly [schedule guard](.github/workflows/schedule-guard.yml) calls GitHub's enable-workflow API for an explicit list of refresh workflows and itself. It can restore workflows disabled for inactivity, preserves manually disabled workflows, and runs independently of collection failures.

This is an interim mitigation, not a scheduling guarantee: GitHub does not document active-workflow renewal as a permanent exemption, and scheduled runs can be delayed or dropped. A scheduler on our own Linux server is the planned independent trigger. The guard does not collect data, create dummy commits, or change source/check timestamps; successful collection and published data freshness still need monitoring.
<!-- /schedule-reliability -->
