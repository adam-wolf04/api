# Autor: Adam Wolf | REST API pro kurzovní lístky

import os
import math
from fastapi import FastAPI, Query, HTTPException
from sqlmodel import Field, SQLModel, Session, create_engine, select
from sqlalchemy import text
from dotenv import load_dotenv
import httpx

load_dotenv()

class Rate(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    shortName: str
    validFrom: str
    name: str
    country: str
    move: float
    amount: int
    valBuy: float
    valSell: float
    valMid: float
    currBuy: float
    currSell: float
    currMid: float
    version: int
    cnbMid: float
    ecbMid: float

app = FastAPI()
engine = create_engine("sqlite:///rates.db")
SQLModel.metadata.create_all(engine)

ERSTE_API_KEY = os.environ.get("ERSTE_API_KEY")
if not ERSTE_API_KEY:
    raise Exception("Chybí ERSTE_API_KEY env variable!")

ERSTE_URL = f"https://webapi.developers.erstegroup.com/api/csas/public/sandbox/v2/rates/exchangerates?web-api-key={ERSTE_API_KEY}"

# Porovnání dvou float čísel s nějakou nadsázkou +-, protože mi to furt vypisovalo, že něco bylo updatnutý i když se nic neměnilo
def are_floats_equal(a, b):
    return math.isclose(a, b, abs_tol=1e-6)

def compare_rates(a, b):
    for key in a:
        if isinstance(a[key], float):
            if not are_floats_equal(a[key], b.get(key, None)):
                return False
        else:
            if a[key] != b.get(key, None):
                return False
    return True

def is_same_dataset(list1, list2):
    if len(list1) != len(list2):
        return False
    l1 = sorted(list1, key=lambda x: x['shortName'])
    l2 = sorted(list2, key=lambda x: x['shortName'])
    return all(compare_rates(x, y) for x, y in zip(l1, l2))


@app.get("/status") # endpoint který ovšřuje, že backend běží, link: http://localhost:3000/status
def status():
    return {"status": "running"}


# link: http://localhost:3000/api/rates?usedb=false stáhne z API, porovná, a pokud něco tak aktualizuje DB
# link: http://localhost:3000/api/rates?usedb=true načte z databáze
@app.get("/api/rates")
def get_rates(usedb: bool = Query(...)):
    print("Kontrola API kurzu spuštěna – usedb =", usedb)

    with Session(engine) as session:
        if usedb:
            db_data = session.exec(select(Rate)).all()
            return [r.dict() for r in db_data]

        try:
            response = httpx.get(ERSTE_URL, timeout=10)
            response.raise_for_status()
            fresh_data = response.json()
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Chyba při stahování z API: {str(e)}")

        db_data = session.exec(select(Rate)).all()
        existing = [r.dict() for r in db_data]

        if is_same_dataset(fresh_data, existing):
            return {"message": "No change", "rates": existing}

        session.exec(text("DELETE FROM rate"))
        session.commit()

        keys = Rate.__fields__.keys()
        for item in fresh_data:
            filtered = {k: item[k] for k in keys if k in item}
            session.add(Rate(**filtered))
        session.commit()

        updated = session.exec(select(Rate)).all()
        return {"message": "Updated", "rates": [r.dict() for r in updated]}