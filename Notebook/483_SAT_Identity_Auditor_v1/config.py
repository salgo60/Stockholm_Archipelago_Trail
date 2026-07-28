from datetime import date

TODAY=date.today().strftime("%Y%m%d")
PREFIX="483"

CONCORDANCE_URL="https://map.stockholmarchipelagotrail.com/data/geojson/poi-concordance.json"

OVERPASS_ENDPOINTS=[
 "https://overpass-api.de/api/interpreter",
 "https://lz4.overpass-api.de/api/interpreter",
 "https://overpass.private.coffee/api/interpreter"
]

SPARQL_ENDPOINT="https://query.wikidata.org/sparql"
USER_AGENT="SAT Identity Auditor/1.0 (https://github.com/salgo60/Stockholm_Archipelago_Trail)"
