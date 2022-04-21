/*Find the number of users who are both sellers and bidders.
    Expected Answer: 6717
    Works don't change
*/
SELECT COUNT(Sellers.UserID_Var)
FROM Bidders, Sellers
WHERE Bidders.UserID_Var = Sellers.UserID_Var;