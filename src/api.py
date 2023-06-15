import os
from fastapi import APIRouter
from elasticsearch import Elasticsearch
from urllib.parse import unquote

INDEX_NAME = "location"
ELASTICSEARCH = os.environ["ELASTICSEARCH"]

def get_location(query):
    return { "result": list(map(lambda x: x["_source"], es.search(index=INDEX_NAME, query=query)["hits"]["hits"])) }

router = APIRouter(prefix="/api")
es = Elasticsearch(ELASTICSEARCH)

@router.get("/search")
def search(q: str):
    q = unquote(q)
    query = {
        "bool": {
            "must": [
                {
                    "match": {
                        "name": q
                    }
                },
                {
                    "match": {
                        "address": q
                    }
                }
            ]
        }
    }
    
    return get_location(query)

@router.get("/nearby")
def nearby(lat: float, lon: float):
    query = {
        "geo_distance": {
            "distance": "5km",
            "point": f"{lat},{lon}"
        }
    }

    return get_location(query)