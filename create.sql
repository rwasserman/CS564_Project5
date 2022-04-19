drop table if exists Item;
drop table if exists Sellers;
drop table if exists SoldBy;
drop table if exists Categories;
drop table if exists Bids;
drop table if exists Bidders;

create table Item (ItemID INT NOT NULL, Name VARCHAR(256) NOT NULL, Currently
    VARCHAR(256) NOT NULL, First_Bid VARCHAR(256) NOT NULL, Started VARCHAR(256) NOT NULL, Description VARCHAR(256) NOT NULL,
    Ends VARCHAR(256) NOT NULL, Buy_Price VARCHAR(256), Number_Of_Bids INT NOT NULL, PRIMARY KEY(ItemID) );

create table Sellers (UserID INT NOT NULL, Rating VARCHAR(256) NOT NULL, Location VARCHAR(256) NOT NULL, Country CHAR(256) NOT NULL, primary key (UserID) );

create table SoldBy (UserID VARCHAR(256) NOT NULL, ItemID INT NOT NULL, primary key(UserID, ItemID) );

create table Categories (ItemID INT NOT NULL, Category VARCHAR(256) NOT NULL, primary key(Category), foreign key(ItemID) references Item(ItemID) );

create table Bids (ItemID INT NOT NULL, UserID VARCHAR(256) NOT NULL, Time_Var VARCHAR(256) NOT NULL, Amount VARCHAR(256) NOT NULL, primary key(Time_Var, Amount), 
    foreign key(ItemID) references Item(ItemID), foreign key(UserID) references Bidder(UserID) );

create table Bidders (UserID VARCHAR(256) NOT NULL, Rating INT NOT NULL, Country VARCHAR(256), Location_Var VARCHAR(256), primary key(UserID) );


