#!/bin/bash
rm *.dat
python3 skeleton_parser.py ebay_data/items-*.json
#bulk load the .dat files
#sort *.dat
#uniq *.dat
sqlite3 ebay < create.sql
#for each query
sqlite3 ebay < load.txt
#DONE 1, 2, 3?, 5, 6

for statement in 1 2 3 4 5 6 7
    do 
        sqlite3 ebay < query$statement.sql
    done

