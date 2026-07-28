import pandas as pd
from client import get_json
from config import CONCORDANCE_URL

def load():
    data=get_json(CONCORDANCE_URL)
    rows=[]
    for ext,sat in data["satIdOf"].items():
        p=ext.split(":")
        row={"source":p[0],"external_id":ext,"sat_id":sat,
             "osm_type":None,"osm_id":None,"qid":None}
        if p[0]=="osm":
            row["osm_type"]=p[1]
            row["osm_id"]=int(p[2])
        elif p[0]=="wikidata":
            row["qid"]=p[1]
        rows.append(row)
    return pd.DataFrame(rows)
