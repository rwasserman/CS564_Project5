/* Find the number of users in the database 
    Expected Answer: 13422
*/
SELECT COUNT(DISTINCT UserID) FROM Sellers, Bidders WHERE Sellers.UserID = Bidders.UserID; 

