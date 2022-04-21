drop table if exists Items;
drop table if exists Sellers;
drop table if exists SoldBy;
drop table if exists Categories;
drop table if exists Bids;
drop table if exists Bidders;

create table Items (Currently_Var INT NOT NULL, First_Bid_Var VARCHAR(256) NOT NULL, Started_Var VARCHAR(256) NOT NULL, 
    Ends_Var VARCHAR(256) NOT NULL, Description_Var VARCHAR(256) NOT NULL, Name_Var VARCHAR(256) NOT NULL, ItemID_Var INT NOT NULL,     
    Buy_Price_Var VARCHAR(256), Number_Of_Bids_Var INT NOT NULL, PRIMARY KEY(ItemID_Var) );

create table Sellers (Location_Var VARCHAR(256) NOT NULL, Country_Var CHAR(256) NOT NULL, Rating_Var INT NOT NULL, UserID_Var VARCHAR(256) NOT NULL, 
    primary key (UserID_Var) );


create table SoldBy (UserID_Var VARCHAR(256) NOT NULL, ItemID_Var INT NOT NULL, primary key(UserID_Var, ItemID_Var) );

create table Categories (ItemID_Var INT NOT NULL, Category_Var VARCHAR(256) NOT NULL, primary key(Category_Var, ItemID_Var), foreign key(ItemID_Var) references Items(ItemID_Var) );

create table Bids (ItemID_Var INT NOT NULL, UserID_Var VARCHAR(256) NOT NULL, Time_Var VARCHAR(256) NOT NULL, Amount_Var INT NOT NULL, primary key(ItemID_Var, Time_Var, Amount_Var), 
    foreign key(ItemID_Var) references Items(ItemID_Var), foreign key(UserID_Var) references Bidder(UserID_Var) );

create table Bidders (UserID_Var VARCHAR(256) NOT NULL, Rating_Var INT NOT NULL, Location_Var VARCHAR(256), Country_Var VARCHAR(256), primary key(UserID_Var) );


