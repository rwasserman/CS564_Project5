#!/bin/bash
rm *.dat && rm ebay
python3 skeleton_parser.py ebay_data/items-*.json
sqlite3 ebay < create.sql
#for each query
sqlite3 ebay < load.txt
for statement in 1 2 3 4 5 6 7
    do 
        sqlite3 ebay < query$statement.sql
    done

