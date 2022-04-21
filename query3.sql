/* Find the number of auctions belonging to exactly four categories
    (If your third query result is wrong, it is probably because you did not eliminate duplicates correctly in your
database.))
    Expected Answer: 8365
*/
SELECT COUNT(ItemID_Var) 
FROM (
    SELECT *
    FROM Categories
    GROUP BY ItemID_Var
    HAVING COUNT(Category_Var) = 4
);
