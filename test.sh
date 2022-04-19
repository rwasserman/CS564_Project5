#!/bin/bash
rm *.dat
python3 skeleton_parser.py ebay_data/items-0.json
#bulk load the .dat files
sqlite3 ebay < create.sql
#for each query
sqlite3 ebay < load.txt
for statement in 1 2 3 4 5 6 7
    do 
        sqlite3 ebay < query$statement.sql
    done