#!/usr/bin/env python

import os
import json
import pandas
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

INDEX_NAME = "location"
ELASTICSEARCH = os.environ["ELASTICSEARCH"]

def generate_data(df):
    for value in df.values:
        yield {
            "_index": INDEX_NAME,
            "name": value[0],
            "type": value[1],
            "public": value[2],
            "group": value[3],
            "address": value[4],
            "contact": value[5],
            "homepage": value[6],
            "point": value[7]
        }

es = Elasticsearch(ELASTICSEARCH)

data = pandas.read_csv("data.csv")

with open("es_mapping.json", encoding="utf8") as f:
    mapping = json.load(f)

es.options(ignore_status=[400, 404]).indices.delete(index=INDEX_NAME)
es.indices.create(index=INDEX_NAME, mappings=mapping["mappings"])

bulk(es, generate_data(data))
