/*Find the ID(s) of auction(s) with the highest current price.
    Expected Answer: 1046871451
*/

WITH maxTable (maxNum) AS
(
    SELECT MAX(Currently_Var)
    FROM Items
)
SELECT ItemID_Var
FROM Items, maxTable
WHERE Items.Currently_Var = maxTable.maxNum;                