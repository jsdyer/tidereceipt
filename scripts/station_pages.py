"""Readable station summaries from the same saved receipts used by the explorer."""
from datetime import timedelta
from html import escape
from xml.etree import ElementTree as ET

from common import date
from stations import STATIONS

LICENCE = "https://tides.gc.ca/en/licence-agreement"
NOTICE = f'''<aside class="chs-notice"><strong>This product is not to be used for navigation.</strong>
<p>This product was made by or for Jeffrey Dyer and contains intellectual property (Data) of the Canadian Hydrographic Service of the Department of Fisheries and Oceans.</p>
<p>The copyrights in the Data are and remain the property of His Majesty the King in Right of Canada and shall not be sold, licensed, leased, assigned or given to a third party.</p>
<p>The incorporation of the Data in this product does not constitute an endorsement or an approval of this product by the Canadian Hydrographic Service, the Department of Fisheries and Oceans or His Majesty the King in Right of Canada.</p><a href="{LICENCE}">CHS licence agreement</a></aside>'''


def stamp(value):
    return date(value).strftime("%b %d, %Y at %H:%M UTC")


def evidence(point, label, prefix):
    return f'<a href="{prefix}{escape(point["file"], quote=True)}">{label}</a>'


def compare_hours(receipts, readings):
    # One comparison per hour. Prefer the latest receipt actually saved before that hour.
    by_hour = {}
    for receipt in sorted(receipts, key=lambda item: item["captured_at"], reverse=True):
        for point in receipt["items"]:
            target = point["target"]
            if target in readings and target not in by_hour:
                by_hour[target] = (point, receipt, readings[target])
    return sorted(by_hour.items(), reverse=True)


def station_summary(station, data, manifest):
    receipts = [r for r in data["receipts"] if r["entity"] == station.code]
    station_files = [r for r in manifest if r["entity"] == station.code]
    readings = {p["target"]: p for key, p in data["observations"].items()
                if key.partition("|")[0] == station.code and p["quality"] == "1"}
    matched = compare_hours(receipts, readings)
    source = f"https://tides.gc.ca/en/stations/{station.code}"
    first = min(r["captured_at"] for r in station_files)
    checked = data["collection"]["checked_at"]
    parts = [f'<p class="intro">Explore hourly water levels at Canadian Hydrographic Service station {station.code} in {escape(station.province)}. Compare what the tide table predicted with what the gauge recorded.</p>',
             f'<p class="station-actions"><a href="../../?station={station.code}#explorer">Compare saved predictions</a> · <a href="{source}">Official {escape(station.name)} station</a></p>']
    if readings:
        last = readings[max(readings)]
        window_start = date(last["target"]) - timedelta(hours=24)
        day = [p for p in readings.values() if date(p["target"]) > window_start]
        levels = [p["value"] for p in day]
        parts += ['<section><h2>Latest saved gauge reading</h2>',
                  f'<p><strong>{last["value"]:.2f} m</strong> relative to local chart datum at {stamp(last["target"])}. '
                  f'The {len(day)} quality-flag-1 hourly readings in the 24 hours ending then ranged from {min(levels):.2f} to {max(levels):.2f} m. '
                  f'{evidence(last, "Saved gauge readings", "../../")}</p></section>']
    else:
        parts += ['<section><h2>Gauge coverage</h2><p>The recent archive contains no quality-flag-1 hourly readings for this station. Its saved predictions are available below.</p></section>']
    if matched:
        recent = matched[:6]
        rows = []
        for target, (point, receipt, observed) in recent:
            rows.append(f'<tr><td>{stamp(target)}</td><td>{point["value"]:.2f}</td><td>{observed["value"]:.2f}</td><td>{point["value"] - observed["value"]:+.2f}</td>'
                        f'<td><a href="../../?station={station.code}&amp;receipt={receipt["id"]}#explorer">Open receipt</a></td></tr>')
        parts += ['<section><h2>Recent matched hours</h2><p>Each row uses the latest archived prediction saved before that hour. A positive difference means the tide table predicted a higher level than the gauge recorded. All levels use this station’s chart datum.</p>',
                  '<div class="table-wrap"><table><caption>Most recent hourly comparisons, in metres</caption><thead><tr><th>Hour (UTC)</th><th>Predicted</th><th>Gauge</th><th>Prediction − gauge</th><th>Evidence</th></tr></thead><tbody>',
                  ''.join(rows), '</tbody></table></div></section>']
    elif receipts:
        parts += ['<section><h2>When will a comparison appear?</h2><p>A comparison needs a prediction saved before its target hour and a quality-flag-1 reading from the same gauge for that hour. The recent receipts have no matching pair yet.</p></section>']
    if receipts:
        latest = receipts[0]
        hours = latest["items"]
        parts += ['<section><h2>Most recent saved prediction</h2>',
                  f'<p>At {stamp(latest["captured_at"])} CoolCode saved {len(hours)} hourly predictions for {stamp(hours[0]["target"])} through {stamp(hours[-1]["target"])}. '
                  f'{evidence(latest, "Saved prediction file", "../../")}</p></section>']
    parts.append(f'<p>First station receipt {stamp(first)}. Last collection check {stamp(checked)}. Comparisons use the latest 14 days of captures. <a href="../../data/archive.json">Complete archive index</a>.</p>')
    return ''.join(parts)


def render_page(title, description, canonical, prefix, heading, body):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} · Tide Receipt</title><meta name="description" content="{escape(description, quote=True)}"><link rel="canonical" href="{canonical}"><link rel="stylesheet" href="{prefix}style.css"></head>
<body><a class="skip" href="#main">Skip to station data</a><header class="top"><a class="brand" href="{prefix}">Tide Receipt</a><a href="https://coolcode.ca/">CoolCode.ca</a></header>
<main id="main" class="station-page"><nav aria-label="Station navigation"><a href="{prefix}stations/">Browse all tide stations</a></nav>
<h1>{escape(heading)}</h1>{body}<p class="caption">No CoolCode account · No ads · <a href="https://coolcode.ca/about/#our-commitments">How CoolCode works</a></p>{NOTICE}</main></body></html>'''


def write_station_pages(output, tool, data, manifest):
    root_url = "https://coolcode.ca" + tool["url"]
    directory = output / "stations"
    directory.mkdir()
    paths = ["stations/"]
    entries = []
    codes = {r["entity"] for r in manifest}
    for station in STATIONS:
        if station.code not in codes:
            continue
        path = f"stations/{station.slug}/"
        paths.append(path)
        entries.append(f'<li><a href="{station.slug}/">{escape(station.name)}</a> · {escape(station.province)} · CHS {station.code}</li>')
        title = f"{station.name} tide predictions and gauge readings"
        description = f"Compare pre-recorded tide predictions with hourly water levels at {station.name}, {station.province}, CHS station {station.code}. See source receipts, dates and measured differences."
        body = station_summary(station, data, manifest)
        (output / path).mkdir()
        (output / path / "index.html").write_text(render_page(title, description, root_url + path, "../../", title, body), encoding="utf-8")
    intro = '<p class="intro">Choose a harbour to see the latest saved water level, compare predictions with readings, and open the original receipts.</p>'
    body = intro + '<ul class="station-list">' + ''.join(entries) + '</ul>'
    title = "Canadian tide stations and hourly water levels"
    (directory / "index.html").write_text(render_page(title, "Explore saved predictions and measured water levels by Canadian tide station.", root_url + "stations/", "../", title, body), encoding="utf-8")
    sitemap = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for path in paths:
        ET.SubElement(ET.SubElement(sitemap, "url"), "loc").text = root_url + path
    ET.ElementTree(sitemap).write(output / "sitemap.xml", encoding="utf-8", xml_declaration=True)
