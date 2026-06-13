
import json
import re
import requests

SAT_URL = "https://gist.githubusercontent.com/salgo60/f2e36b3be3aaea11e93805418b825c27/raw/7d0cb02e94f2ac43ab3d497ab9302b2e9388956e/SAT.geojson"

sat = requests.get(SAT_URL, timeout=60)
sat.raise_for_status()
data = sat.json()

mapping = {}

for feature in data.get("features", []):
    props = feature.get("properties", {})
    sat_id = props.get("id")
    if not sat_id:
        continue

    for ref in props.get("sameAs", []):
        m = re.match(r"osm:(node|way|relation):(\d+)", ref)
        if m:
            mapping[(m.group(1), int(m.group(2)))] = sat_id

print(f"Found {len(mapping)} OSM-linked SAT objects")

print("[out:json][timeout:300];")
for osm_type, osm_id in mapping:
    print(f"{osm_type}({osm_id});")
print("out tags;")

# After downloading OSM data, compare:
#
# expected = mapping[(osm_type, osm_id)]
# actual = tags.get("ref:stockholmarchipelagotrail")
#
# if actual != expected:
#     print(osm_type, osm_id, actual, "=> should be", expected)
