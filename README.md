# Stockholm Archipelago Trail
* [SAT Dashboard](https://raw.githack.com/salgo60/Stockholm_Archipelago_Trail/main/notebook/output/SAT_ALL_IN_ONE_142_3_dashboard_latest.html)
A try to add value to Stockholm Archipelago Trail see [issues](https://github.com/salgo60/Stockholm_Archipelago_Trail/issues?q=is%3Aissue)
* see futher [Stockholm Archipelago Trail issues](https://github.com/salgo60/Stockholm_Archipelago_Trail/issues?q=is%3Aissue) and [Roslagsleden issues Roslagsleden](https://github.com/salgo60/Roslagsleden/issues?q=is%3Aissue)

# System Architecture see [issue 149](https://github.com/salgo60/Stockholm_Archipelago_Trail/issues/149)

```mermaid
flowchart LR
  subgraph Sources[Data Sources]
    OSM["OSM <br/>(trails, POIs, toilets, water)"]
    WD["Wikidata <br/>(600 SAT items,<br/>labels >30 languages,<br/>links: OSM/GMaps/Instagram)"]
    GM["Google Maps / Business Sites <br/>(opening hours, URLs)"]
    SK["Skärgårdsstiftelsen <br/>(2019 open-data sets?)"]
    HF["Ferry/Transport Feeds <br/>(GTFS/CSV/API)"]
    UGC["User Feedback <br/>(Facebook, blogs, GitHub Issues)"]
  end

  subgraph Ingest[Ingestion & ETL]
    IN_OSM["Overpass/OSM Sync <br/>scheduled ETL"]
    IN_WD["SPARQL Sync <br/>labels & links"]
    IN_GM["Scraper/API for hours <br/>(legal/robots aware)"]
    IN_SK["Once-off import + <br/>quality scoring"]
    IN_HF["GTFS parser"]
    IN_UGC["NLP extraction <br/>(closed tap, hours, notes)"]
    QAC["Validation & QA <br/>(schema, tag checks)"]
  end

  Sources --> IN_OSM
  Sources --> IN_WD
  Sources --> IN_GM
  Sources --> IN_SK
  Sources --> IN_HF
  Sources --> IN_UGC
  IN_OSM --> QAC
  IN_WD --> QAC
  IN_GM --> QAC
  IN_SK --> QAC
  IN_HF --> QAC
  IN_UGC --> QAC

  subgraph Storage[Storage & Catalog]
    PG[("PostGIS")]
    KB[("Doc Store / Vector DB <br/>(WD descriptions, pages)")]
    MQ[["Message Queue / Scheduler"]]
    MET[("Data Catalog & Provenance")]
  end

  QAC --> PG
  QAC --> MET
  IN_WD --> KB
  IN_UGC --> KB
  MQ --- IN_OSM
  MQ --- IN_WD
  MQ --- IN_GM
  MQ --- IN_HF

  subgraph AI[AI Services]
    NLP["NLP Router <br/>(user text -> queries)"]
    QG["Query Generator <br/>(NL -> SPARQL/Overpass/SQL)"]
    SUM["Summarizer & Translator <br/>(>30 languages via WD labels)"]
    AVP["Availability Predictor <br/>(hrs/seasonality model)"]
    DQ["Data Quality Heuristics <br/>(OSM<->WD<->Google consistency)"]
    PLAN["Itinerary & Routing <br/>(multi-island + ferries)"]
  end

  PG --> AVP
  PG --> PLAN
  KB --> SUM
  PG --> DQ
  MET --> DQ
  NLP --> QG
  QG --> PG
  QG --> KB
  AVP --> SUM
  DQ --> SUM
  PLAN --> SUM

  subgraph API[Public API Layer]
    GEO["GeoJSON/REST <br/>/sections, /islands, /pois"]
    TRIP[/"trip-plan <br/>inputs: start, nights,<br/>mode, tent/hotel, bike/foot/boat/"/]
    STATUS[/"status <br/>(open/closed, water/toilets)"/]
    SEARCH[/"search <br/>text -> facilities"/]
  end

  PG --> GEO
  AVP --> STATUS
  PLAN --> TRIP
  SUM --> SEARCH

  subgraph UI[User Interfaces]
    Web["Web Map (mobile-first) <br/>filters: water, toilets, food,<br/>open now, bike-friendly"]
    Chat["Conversational Assistant <br/>(multilingual)"]
    Embed["Static exports <br/>(GeoJSON for uMap/Folium,<br/>printable PDFs)"]
  end

  API --> UI
  GEO --> Web
  STATUS --> Web
  TRIP --> Web
  SEARCH --> Chat
  TRIP --> Chat
  GEO --> Embed

  subgraph Gov[Governance & Ops]
    Admin["Admin Portal <br/>(verify reports,<br/>flag outdated POIs)"]
    Auth["Auth & Roles <br/>(operators, volunteers)"]
    Obs["Monitoring & Logs"]
    Lic["Licensing & Attributions <br/>(OSM/ODbL, WD/CC0)"]
  end

  UI --> Admin
  API --> Obs
  MET --> Admin
  Admin --> PG
  Auth --- API
  Lic --- Web

```

## Binder with POC [video](https://youtu.be/bepljHYFqp4)

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/salgo60/Stockholm_Archipelago_Trail/HEAD?filepath=notebook/stockholm_archipelago_trail_map_poc.ipynb)

Click the badge to launch an interactive map in Binder 🚀

## Variant med snippets hur data kan hämtas från Wikidata OpenStreet Map
* [video](https://youtu.be/D02QFoozRvI)

TBA

## Variant med köra python kod och skapa översättningar mha Google Translate
* video TBD
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/salgo60/Stockholm_Archipelago_Trail/main?filepath=Notebook/Show%20case%20Stockholm%20Archipelago%20Trail%20showcase%202.ipynb)

## Tältplatser Naturreservat version 1 
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/salgo60/Stockholm_Archipelago_Trail/HEAD?filepath=notebook%2FCampingplatser%20och%20Naturreservat%20v1.ipynb)
## Resources
1) [Naturkartan](https://www.naturkartan.se/sv/) / [app](https://apps.apple.com/se/app/naturkartan/id1223011883)
2) [Grillplatser.nu](https://grillplatser.nu/Karta/Kommun/Stockholm)
2) Wikiproject
3) 
## Thoughts
