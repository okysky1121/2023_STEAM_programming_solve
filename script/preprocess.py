#!/usr/bin/env python

import sys, os, json, requests, unicodedata
from pandas import read_excel
from tqdm import tqdm
from geopy import Nominatim
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch
from elasticsearch.helpers import parallel_bulk

INDEX_NAME = "location"
ELASTICSEARCH = os.environ["ELASTICSEARCH"]
BASE_URL = "https://www.juso.go.kr/support/AddressMainSearch.do?searchKeyword="

def geocode(addr):
    try:
        point = geolocator.geocode(addr, timeout=None)
        return f"{point.latitude},{point.longitude}"
    except:
        pass

def get_address(addr):
    try:
        res = requests.get(BASE_URL + addr)
        html = BeautifulSoup(res.content, "html.parser")

        return unicodedata.normalize("NFKD", html.select_one(".roadNameText").text)
    except:
        pass

def generate_data(data):
    for value in data.values:
        yield {
            "_index": INDEX_NAME,
            "name": value[0],
            "type": value[1],
            "public": value[2],
            "group": value[3],
            "address": value[4],
            "contact": value[5],
            "homepage": value[6]
        }

data = read_excel(sys.argv[1],
                  sheet_name=2,
                  usecols=[6, 8, 9, 12, 13, 23 ,25],
                  header=None,
                  skiprows=10,
                  names=["name", "type", "public", "group", "address", "contact", "homepage"])\
        .apply(lambda x: x.str.strip())\
        .fillna("null")
geolocator = Nominatim(user_agent="sleepy")

tqdm.pandas()
data["address"] = data["address"].progress_apply(get_address)
# .progress_apply(geocode)

data.to_csv("fetch_data.csv", index=False)

es = Elasticsearch(ELASTICSEARCH)

with open("es_mapping.json", encoding="utf8") as f:
    mapping = json.load(f)

es.options(ignore_status=[400, 404]).indices.delete(index=INDEX_NAME)
es.indices.create(index=INDEX_NAME, mappings=mapping["mappings"])

for s, info in parallel_bulk(es, generate_data(data)):
    if not s:
        print(info)