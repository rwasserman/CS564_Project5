/* Find number of Sellers with Rating > 1000 
    Expected Answer: 3130
*/
SELECT COUNT( DISTINCT UserID_Var)
FROM Sellers
WHERE Rating_Var > 1000;
