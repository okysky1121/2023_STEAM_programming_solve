#!/usr/bin/env python

import sys
import unicodedata
import pandas
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from pandas import Series
from geopy import Nominatim

BASE_URL = "https://www.juso.go.kr/support/AddressMainSearch.do?searchKeyword="

def get_address(addr: str) -> Series | None:
    try:
        res = requests.get(BASE_URL + addr, timeout=None)
        html = BeautifulSoup(res.content, "html.parser")

        return Series([unicodedata.normalize("NFKC", html.select_one(".roadNameText").text),
                       unicodedata.normalize("NFKC", html.select_one(".info_eng > span").text)])
    except:
        return Series([None, None])
    
def geocode(addr: str) -> str:
    try:
        location = geolocator.geocode(addr)
        return f"{location.latitude},{location.longitude}"
    except:
        pass

tqdm.pandas()

# load file
data = pandas.read_excel(sys.argv[1],
                         sheet_name=2,
                         usecols=[6, 8, 9, 12, 13, 23, 25],
                         header=None,
                         skiprows=10,
                         names=["name", "type", "public", "group", "address", "contact", "hompage"])\
                .apply(lambda x: x.str.strip())\
                .fillna("EMPTY")

geolocator = Nominatim(user_agent="sleepy")

# request location
data[["_address", "_address_eng"]] = data["address"].progress_apply(get_address)

# request latitude/longitude
data["_point"] = data["_address"].progress_apply(geocode)
data["_point_eng"] = data["_address_eng"].progress_apply(geocode)

# filter empty values
data = data[data["_point"].notnull() | data["_point_eng"].notnull()]
data["point"] = data["_point"].combine_first(data["_point_eng"])

# export csv
data.drop(columns=["_address", "_address_eng", "_point", "_point_eng"])\
    .to_csv("data.csv", index=None)
