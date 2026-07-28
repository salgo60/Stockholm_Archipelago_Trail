import time,requests
from config import USER_AGENT

session=requests.Session()
session.headers.update({"User-Agent":USER_AGENT})

def get_json(url,params=None,headers=None,retries=5):
    for i in range(retries):
        r=session.get(url,params=params,headers=headers,timeout=180)
        if r.status_code==429:
            time.sleep(int(r.headers.get("Retry-After","30")))
            continue
        if r.status_code>=500:
            time.sleep(2**i)
            continue
        r.raise_for_status()
        return r.json()
    raise RuntimeError("Failed")
