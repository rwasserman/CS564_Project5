/* Find the number of users in the database 
    Expected Answer: 13422
*/
-- SELECT COUNT(DISTINCT Sellers.UserID_Var)
-- FROM Bidders 
--     JOIN Sellers on Bidders.UserID_Var != Sellers.UserID_Var; 
-- WHERE Sellers.UserID_Var != Bidders.UserID_Var;



SELECT COUNT(*) total
FROM (
    SELECT UserID_Var FROM Bidders
    UNION
    SELECT UserID_Var FROM Sellers
) s
;

/* 
Bidders 7010
Sellers 13129
*/



-- Buyer ID
-- 1
-- 2
-- 3
-- 4
-- 5
-- 6

-- Seller ID
-- 5
-- 6
-- 7
-- 8
-- 9
-- 10 


-- SELECT COUNT(DISTINCT Bidders.UserID_Var)
-- FROM Sellers, Bidders
-- WHERE Sellers.UserID_Var = Bidders.UserID_Var;



