/*Find the number of categories that include at least one item with a bid of more than $100
    Expected Answer: 150
*/


SELECT COUNT(DISTINCT Category_Var)
FROM Categories, Bids
WHERE Categories.ItemID_Var = Bids.ItemID_Var
AND Bids.Amount_Var > 100;
