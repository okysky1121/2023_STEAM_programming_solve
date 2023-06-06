#!/usr/bin/env python

import sys
from pandas import read_excel

data = read_excel(sys.argv[1],
                  sheet_name=2,
                  usecols=[6, 8, 9, 12, 13, 23 ,25],
                  header=None,
                  skiprows=10,
                  names=["name", "type", "public", "group", "location", "contact", "homepage"])

data.to_csv("fetch_data.csv", index=False)