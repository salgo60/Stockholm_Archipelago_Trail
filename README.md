# Stockholm Archipelago Trail
A try to add value to Stockholm Archipelago Trail see [issues](https://github.com/salgo60/Stockholm_Archipelago_Trail/issues?q=is%3Aissue)
* see futher [Stockholm Archipelago Trail issues](https://github.com/salgo60/Stockholm_Archipelago_Trail/issues?q=is%3Aissue) and [Roslagsleden issues Roslagsleden](https://github.com/salgo60/Roslagsleden/issues?q=is%3Aissue)

# System Architecture see [issue 149](https://github.com/salgo60/Stockholm_Archipelago_Trail/issues/149)

flowchart LR
  subgraph Sources[Data Sources]
    OSM[OSM\n(trails, POIs, toilets, water)]
    WD[Wikidata\n(600 SAT items,\nlabels >30 languages,\nlinks: OSM/GMaps/Instagram)]
    GM[Google Maps / Business Sites\n(opening hours, URLs)]
    SK[Skärgårdsstiftelsen\n(2019 open-data sets?)]
    HF[Ferry/Transport Feeds\n(GTFS/CSV/API)]
    UGC[User Feedback\n(Facebook, blogs, GitHub Issues)]
  end

  subgraph Ingest[Ingestion & ETL]
    IN_OSM[Overpass/OSM Sync\nscheduled ETL]
    IN_WD[SPARQL Sync\nlabels & links]
    IN_GM[Scraper/API for hours\n(legal/robots aware)]
    IN_SK[Once-off import +\nquality scoring]
    IN_HF[GTFS parser]
    IN_UGC[NLP extraction\n(closed tap, hours, notes)]
    QAC[Validation & QA\n(schema, tag checks)]
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
    PG[(PostGIS)]
    KB[(Doc Store / Vector DB\n(WD descriptions, pages))]
    MQ[[Message Queue / Scheduler]]
    MET[(Data Catalog & Provenance)]
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
    NLP[NLP Router\n(user text → queries)]
    QG[Query Generator\n(NL → SPARQL/Overpass/SQL)]
    SUM[Summarizer & Translator\n(>30 languages via WD labels)]
    AVP[Availability Predictor\n(hrs/seasonality model)]
    DQ[Data Quality Heuristics\n(OSM↔WD↔Google consistency)]
    PLAN[Itinerary & Routing\n(multi-island + ferries)]
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
    GEO[GeoJSON/REST\n/sections, /islands, /pois]
    TRIP[/trip-plan\ninputs: start, nights,\nmode, tent/hotel, bike/foot/boat/]
    STATUS[/status\n(open/closed, water/toilets)]
    SEARCH[/search\ntext → facilities]
  end

  PG --> GEO
  AVP --> STATUS
  PLAN --> TRIP
  SUM --> SEARCH

  subgraph UI[User Interfaces]
    Web[Web Map (mobile-first)\nfilters: water, toilets, food,\nopen now, bike-friendly]
    Chat[Conversational Assistant\n(multilingual)]
    Embed[Static exports\n(GeoJSON for uMap/Folium,\nprintable PDFs)]
  end

  API --> UI
  GEO --> Web
  STATUS --> Web
  TRIP --> Web
  SEARCH --> Chat
  TRIP --> Chat
  GEO --> Embed

  subgraph Gov[Governance & Ops]
    Admin[Admin Portal\n(verify reports,\nflag outdated POIs)]
    Auth[Auth & Roles\n(operators, volunteers)]
    Obs[Monitoring & Logs]
    Lic[Licensing & Attributions\n(OSM/ODbL, WD/CC0)]
  end

  UI --> Admin
  API --> Obs
  MET --> Admin
  Admin --> PG
  Auth --- API
  Lic --- Web


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
