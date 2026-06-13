
import argparse
import json
import re
from collections import Counter
from pathlib import Path

import requests

SAT_URL = "https://gist.githubusercontent.com/salgo60/f2e36b3be3aaea11e93805418b825c27/raw/7d0cb02e94f2ac43ab3d497ab9302b2e9388956e/SAT.geojson"
OVERPASS_URL = "https://overpass-api.de/api/interpreter"
REPORT_PATH = Path(__file__).with_name("sat_osm_ref_report.json")
REQUEST_HEADERS = {
    "User-Agent": "SAT ref checker/1.0 (https://github.com/salgo60/Stockholm_Archipelago_Trail)",
    "Accept": "application/json",
}


def raise_with_context(response):
    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        detail = response.text[:1000].replace("\n", " ")
        raise requests.HTTPError(f"{exc} Response body: {detail}") from exc


def load_sat_mapping():
    sat = requests.get(SAT_URL, headers=REQUEST_HEADERS, timeout=120)
    raise_with_context(sat)
    data = sat.json()

    mapping = {}
    duplicates = []
    for feature in data.get("features", []):
        props = feature.get("properties", {})
        sat_id = props.get("id")
        if not sat_id:
            continue

        for ref in props.get("sameAs", []):
            m = re.fullmatch(r"osm:(node|way|relation):(\d+)", ref)
            if not m:
                continue

            key = (m.group(1), int(m.group(2)))
            previous = mapping.get(key)
            if previous is not None and previous != sat_id:
                duplicates.append({
                    "type": key[0],
                    "osm_id": key[1],
                    "first_sat_id": previous,
                    "second_sat_id": sat_id,
                })
            mapping[key] = sat_id

    return mapping, duplicates


def build_overpass_query(mapping):
    parts = ["[out:json][timeout:300];("]
    for typ, oid in sorted(mapping):
        parts.append(f"{typ}({oid});")
    parts.append(");out tags;")
    return "\n".join(parts)


def classify(expected, actual):
    if actual is None:
        return "MISSING"
    if actual == "unknown":
        return "UNKNOWN"
    if actual == expected:
        return "OK"
    return "WRONG"


def main(dry_run=False):
    mapping, duplicates = load_sat_mapping()
    query = build_overpass_query(mapping)

    print(f"Checking {len(mapping)} linked OSM objects...")
    if duplicates:
        print(f"Warning: {len(duplicates)} duplicate OSM sameAs links found in SAT data")

    if dry_run:
        print("Dry run: SAT mapping and Overpass query built successfully.")
        return

    response = requests.post(
        OVERPASS_URL,
        data={"data": query},
        headers=REQUEST_HEADERS,
        timeout=300,
    )
    raise_with_context(response)
    osm = response.json()

    seen = set()
    results = []
    summary = Counter()

    for element in osm.get("elements", []):
        key = (element["type"], element["id"])
        seen.add(key)
        expected = mapping[key]
        actual = element.get("tags", {}).get("ref:stockholmarchipelagotrail")
        status = classify(expected, actual)
        summary[status] += 1
        results.append({
            "type": element["type"],
            "osm_id": element["id"],
            "expected": expected,
            "actual": actual,
            "status": status,
        })

    for typ, oid in sorted(set(mapping) - seen):
        summary["NOT_RETURNED"] += 1
        results.append({
            "type": typ,
            "osm_id": oid,
            "expected": mapping[(typ, oid)],
            "actual": None,
            "status": "NOT_RETURNED",
        })

    results.sort(key=lambda row: (row["status"], row["type"], row["osm_id"]))
    REPORT_PATH.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")

    print("Summary:")
    for status, count in sorted(summary.items()):
        print(status, count)
    print(f"Report written to {REPORT_PATH.resolve()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check SAT sameAs OSM objects against ref:stockholmarchipelagotrail tags.")
    parser.add_argument("--dry-run", action="store_true", help="Load SAT data and build the Overpass query without calling Overpass.")
    args = parser.parse_args()
    main(dry_run=args.dry_run)
