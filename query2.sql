/* Find the number of users from New York (i.e., users whose location is the string "New York") 
    (Hint: If your second query result is incorrect, it might be because you set the
    location of a seller incorrectly in your database. The location of a seller is the location of his or her item)
    Expected Answer: 80
*/
-- SELECT COUNT(DISTINCT Sellers.UserID_Var) 
-- FROM Sellers, Bidders 
-- WHERE Sellers.UserID_Var = Bidders.UserID_Var AND Sellers.Location_Var = "New York";

SELECT COUNT(*) total
FROM (
    SELECT UserID_Var, Location_Var FROM Bidders WHERE Location_Var = "New York"
    UNION
    SELECT UserID_Var, Location_Var FROM Sellers WHERE Location_Var = "New York"
) s
;
