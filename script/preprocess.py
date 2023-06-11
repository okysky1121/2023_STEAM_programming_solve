#!/usr/bin/env python

import sys, os, json
from pandas import read_excel
from elasticsearch import Elasticsearch
from elasticsearch.helpers import parallel_bulk

INDEX_NAME = "location"
ELASTICSEARCH = os.environ["ELASTICSEARCH"]

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

data.to_csv("fetch_data.csv", index=False)

es = Elasticsearch(ELASTICSEARCH)

with open("es_mapping.json", encoding="utf8") as f:
    mapping = json.load(f)

es.options(ignore_status=[400, 404]).indices.delete(index=INDEX_NAME)
es.indices.create(index=INDEX_NAME, mappings=mapping["mappings"])

for s, info in parallel_bulk(es, generate_data(data)):
    if not s:
        print(info)