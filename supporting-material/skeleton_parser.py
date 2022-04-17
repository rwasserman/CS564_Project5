
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

from asyncio.windows_events import NULL
import sys
from json import loads
from re import sub

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file):
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
        for item in items:
            """
            TODO: traverse the items dictionary to extract information from the
            given `json_file' and generate the necessary .dat files to generate
            the SQL tables based on your relation design
            """
            # make item as a dictionary so it can use the key value pair 
            # to connect attributes and entities ex) Name: "John"
            # open with mode as append("a") will generate .dat file
            # need NULL coverter() and escapingQuotes()
            parseSeller(item)
            parseBids(item)
            parseItem(item)
            f.write("|".join(map(lambda x:x, item))) #lamba on map as func?
            f.write("\n")
            pass
"""
Seller table is (Location, Country, Rating, UserID(PK))
"""
def parseSeller(table):
    with open("sellers.dat", "a") as f:
        seller = []
        seller.append(escapeQuotations(table.get("Location", "NULL")))
        seller.append(escapeQuotations(table.get("Country", "NULL")))
        seller.append(table["Rating"])
        seller.append(escapeQuotations(table["Seller"]["UserID"])) #not sure if they is right
        f.write("|".join(map(lambda x:x, seller)))
        f.write("\n")

"""
Item table is (Currently, First_Bid, Started, Name, Category, ItemID(PK), 
Description, Ends, Buy_Price (Optional), Number_of_bids(Optional))
"""
def parseItem(table):
    with open("sellers.dat", "a") as f:
        item = []
        item.append(parseCategories(item))
        item.append(transformDollar(table.get("Currently", "NULL")))
        item.append(transformDollar(table["First_Bid"]))
        item.append(transformDttm(table["Started"]))
        item.append(transformDttm(table["Ends"]))
        item.append(escapeQuotations(table["Description"]))
        item.append(escapeQuotations(table["Name"]))
        item.append(table["ItemID"])
        item.append(transformDollar(table.get("Buy_Price", "NULL")))
        item.append(table["Number_of_Bids"])
        f.write("|".join(map(lambda x:x, item)))
        f.write("\n")

"""
Categories table is (Category(PK)) and is attached to the Item entity 
"""
def parseCategories(table):
    with open("categories.dat", "a") as f: 
        categories = table.get("Category")
        if categories != None:
            data_set = set()
            for category in categories:
                data = []
                data.append(escapeQuotations(category["Category"]))
            f.write("|".join(map(lambda x:x, data_set)))
            f.write("\n")

"""
Bids table is (Amount(PK), Time(PK)) and uses the Bidder entity 
attached to each bid through the relationship of Bids On
"""
def parseBids(table):
    with open("bids.dat", "a") as f:
        bids = table.get("Bids")
        if bids != None:
            data_set = set()
            for bid in bids:
                data = []
                data.append(transformDttm(bid["Bid"]["Time"]))
                data.append(transformDollar(bid["Bid"]["Amount"]))
                data.append(parseBidder(bid))
                data_set.add("|".join(data))
            f.write("|".join(map(lambda x:x, data_set)))
            f.write("\n")
"""
Bidder table is (Location(Optional), Country(Optional), UserID(PK), Rating)
"""
def parseBidder(table):
    with open("bidders.dat", "a") as f:
        bidder = []
        bidder.append(escapeQuotations(table["UserID"]))
        bidder.append(table["Rating"])
        bidder.append(escapeQuotations(table.get("Location", "NULL")))
        bidder.append(escapeQuotations(table.get("Country", "NULL")))
        f.write("|".join(map(lambda x:x, bidder)))
        f.write("\n")

"""
1. Escape every instance of a double quote with another double quote.
2. Surround all strings with double quotes.
"""
def escapeQuotations(element):
    if element == None:
        return element
    return '\"' +  element + '\"' #not sure if this is correct
    
"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print "Success parsing " + f

if __name__ == '__main__':
    main(sys.argv)
