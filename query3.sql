/* Find the number of auctions belonging to exactly four categories
    Expected Answer: 8365
*/
SELECT COUNT(ItemID) 
FROM Item, Categories 
WHERE Item.ItemID = Categories.ItemID AND 