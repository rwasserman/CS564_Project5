
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

import sys
from json import loads
from re import sub
import os

columnSeparator = "|"
SELLER_USER_ID_DICTIONARY = {}
BUYER_USER_ID_DICTIONARY = {}

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}


def isJson(f):
    """
    Returns true if a file ends in .json
    """
    return len(f) > 5 and f[-5:] == '.json'

def checkSellerIDIsUnique(sellerID):
    '''
    For a given userID assigned to a seller, make sure that the seller is not
    a duplicate.
    In summary, filters out duplicate sellers.

    @param sellerID, which represents the userID of a seller.
    '''
    try:
        if SELLER_USER_ID_DICTIONARY[sellerID] == "SELLER":
            #already inserted
            return False
        else:
            #not already inserted 
            SELLER_USER_ID_DICTIONARY[sellerID] = "SELLER"
            return True
    except:
        #another case where it is not already inserted
        SELLER_USER_ID_DICTIONARY[sellerID] = "SELLER"
        return True

def checkBuyerIDIsUnique(buyerID):
    '''
    For a given userID assigned to a buyer, make sure the buyer is not a duplicate.
    In summary, filters out duplicate buyers.

    @param buyerID, representing the userID of a buyer
    '''
    try:
        if BUYER_USER_ID_DICTIONARY[buyerID] == "BUYER":
            #already inserted
            return False
        else:
            #not already inserted 
            BUYER_USER_ID_DICTIONARY[buyerID] = "BUYER"
            return True
    except:
        #another case where it is not already inserted
        BUYER_USER_ID_DICTIONARY[buyerID] = "BUYER"
        return True


def transformMonth(mon):
    """
    Converts month to a number, e.g. 'Dec' to '12'
    """
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon


def transformDttm(dttm):
    """
    Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
    """
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]



def transformDollar(money):
    """
    Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
    """
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)


def parseJson(json_file):
    """
    Parses a single json file. Currently, there's a loop that iterates over each
    item in the data set. Your job is to extend this functionality to create all
    of the necessary SQL tables for your database.
    """
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
            parseBidder(item)
            parseItem(item)
            parseCategories(item)
            parseSoldBy(item)
            pass

def parseSeller(table):
    """
    Seller table is (Location, Country, Rating, UserID(PK))
    """
    with open("sellers.dat", "a") as f:
        seller = []
        seller.append(escapeQuotations(table.get("Location", "NULL")))
        seller.append(escapeQuotations(table.get("Country", "NULL")))
        rating = table["Seller"]["Rating"]
        seller.append(escapeQuotations(rating)) #TODO: Rating key does not exist
        seller.append(escapeQuotations(table["Seller"]["UserID"])) #not sure if this is right

        # Only write the seller info if it is a unique userid
        if (checkSellerIDIsUnique(table["Seller"]["UserID"])):
            f.write(columnSeparator.join(map(lambda x:x, seller)))
            f.write("\n")
            
        


def parseItem(table):
    """
    Item table is (Currently, First_Bid, Started, Name, Category, ItemID(PK), 
    Description, Ends, Buy_Price (Optional), Number_of_bids(Optional))
    """
    with open("items.dat", "a") as f:
        item = []
        item.append(transformDollar(table["Currently"]))
        item.append(transformDollar(table["First_Bid"]))
        item.append(transformDttm(table["Started"]))
        item.append(transformDttm(table["Ends"]))
        item.append(escapeQuotations(table["Description"]))
        item.append(escapeQuotations(table["Name"]))
        item.append(table["ItemID"])
        item.append(transformDollar(table.get("Buy_Price", "NULL")))
        item.append(table["Number_of_Bids"])
        f.write(columnSeparator.join(map(lambda x:x, item)))
        f.write("\n")


def parseCategories(table):
    """
    Categories table is (Category(PK)) and is attached to the Item entity 
    """
    with open("categories.dat", "a") as f:
        categories = table.get("Category")
        for category in categories:
            if categories != None:
                item = []
                try:
                    item.append(table["ItemID"])
                    item.append(escapeQuotations(category))
                    f.write(columnSeparator.join(map(lambda x:x, item)))
                    f.write("\n")
                except:
                    pass
                



def parseBids(table):
    """
    Bids table is (Amount(PK), Time(PK)) and uses the Bidder entity 
    attached to each bid through the relationship of Bids On
    """
    with open("bids.dat", "a") as f:
        bids = table.get("Bids")
        
        if bids != None:
            for bid in bids:
                item = []
                item.append(table["ItemID"])    #Foreign key, references Item 
                userID = bid["Bid"]["Bidder"]["UserID"]
                time = bid["Bid"]["Time"]
                amount = bid["Bid"]["Amount"]              
                item.append(escapeQuotations(userID))
                item.append(transformDttm(time))
                item.append(transformDollar(amount))
                f.write(columnSeparator.join(map(lambda x:x, item)))
                f.write("\n")
                

def parseBidder(table):
    """
    Bidder table is (Location(Optional), Country(Optional), UserID(PK), Rating)
    """
    with open("bidders.dat", "a") as f:
        bids = table.get("Bids")
        if bids != None:
            for bid in bids:
                bidder = []
                bidder.append(escapeQuotations(bid["Bid"]["Bidder"]["UserID"]))
                bidder.append(bid["Bid"]["Bidder"]["Rating"])
                
                try:
                    location = bid["Bid"]["Bidder"]["Location"]

                except:
                    location = "NULL"
                bidder.append(escapeQuotations(location))

                try:
                    country = bid["Bid"]["Bidder"]["Country"]
                except:
                    country = "NULL"
                bidder.append(escapeQuotations(country))

                # Only write the bidder info if the UserId is not already in the file
                if(checkBuyerIDIsUnique(bid["Bid"]["Bidder"]["UserID"])):
                    f.write(columnSeparator.join(map(lambda x:x, bidder)))
                    f.write("\n")

def parseSoldBy(table):
    '''
    Parse the @param table 
    '''
    with open("soldby.dat", "a") as f:
        item = []
        item.append(escapeQuotations(table["Seller"]["UserID"]))
        item.append(escapeQuotations(table["ItemID"]))
        f.write(columnSeparator.join(map(lambda x:x, item)))
        f.write("\n")


def escapeQuotations(element):
    """
    1. Escape every instance of a double quote with another double quote.
    2. Surround all strings with double quotes.
    """
    if element != None:
        BASE_QUOTES = '\"'
        stringBuilder = BASE_QUOTES + element.replace('\"', '\"\"') + BASE_QUOTES
        return stringBuilder
    else:
        return "NULL"
    

def main(argv):
    """
    Loops through each json files provided on the command line and passes each file
    to the parser
    """
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print( "Success parsing " + f)

if __name__ == '__main__':
    main(sys.argv)
