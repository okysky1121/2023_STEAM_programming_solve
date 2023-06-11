import os
from fastapi import APIRouter
from elasticsearch import Elasticsearch

INDEX_NAME = "location"
ELASTICSEARCH = os.environ["ELASTICSEARCH"]

router = APIRouter(prefix="/api")
es = Elasticsearch(ELASTICSEARCH)

@router.get("/search")
def search(q: str):
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
    return es.search(index=INDEX_NAME, query=query)["hits"]["hits"]