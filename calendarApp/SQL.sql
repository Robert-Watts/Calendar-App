/*
Author: Robert Watts
Project: Computer Science Controlled Assessment 2019
File Name: SQL.sql
Description: The SQL for the database 
*/

/*Create Users Table - Holds User Data*/
CREATE TABLE Users (
	ID int,
	Name varchar(255) NOT NULL,
	Email varchar(255) NOT NULL,
	Username varchar(255) NOT NULL,
	Password varchar(255) NOT NULL,

	PRIMARY KEY (ID)
);

/*Create Calendars Table - Holds data about all the calendars that exist */
CREATE TABLE Calendars (
	ID int,
	Name varchar(255) NOT NULL,
	Colour int,
	UserID int NOT NULL,

	PRIMARY KEY (ID),
	FOREIGN KEY (UserID) REFERENCES Users(ID)
);

/*Create Calendars Table - Holds data about all the events that exist */
CREATE TABLE Events(
	ID int,
	Name varchar(255),
	StartTimestamp int NOT NULL,
	EndTimestamp int NOT NULL,
	Location varchar(255),
	AllDay bollean,
	CalendarID int NOT NULL,

	PRIMARY KEY (ID),
	FOREIGN KEY (CalendarID) REFERENCES Calendars(ID)
);
