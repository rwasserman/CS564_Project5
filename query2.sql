/* Find the number of users from New York (i.e., users whose location is the string "New York") 
    Expected Answer: 80
*/
SELECT COUNT(DISTINCT UserID) 
FROM Sellers, Bidders 
WHERE Sellers.UserID = Bidders.UserID AND Sellers.Location = "New York";