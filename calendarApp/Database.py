'''
Author: Robert Watts
Project: Computer Science Controlled Assessment 2019
File Name: Database.py
Description: Interfaces with the database file, holding all the
             SQL that is needed throught the program.
'''

import sqlite3 as lite
import os
import re
import hashlib

class Database:
    def __init__(self):
        #Find location of database
        dir_path = os.path.dirname(os.path.realpath(__file__))
        databaseLocation =  dir_path + "/Calendar.db"

        #Create Database connection
        self.con = lite.connect(databaseLocation)
        self.cur = self.con.cursor()


    def createAccount(self, name, email, username, password):
        email=email.lower()

        #Make sure email is valid
        if self.validateEmail(email) == False:
            return "Email Not Valid"

        #Makes sure all othe feilds are valid
        if name == "" or username == "" or password == "":
            return "Fill In Missing Values"

        #See if a user already exists
        check = self.checkIfUserExist(email, username)
        if  check != False:
            return check


        #Create Values list, and SQL statement
        values = (name, email, username, self.hashPassword(password))
        sql = "INSERT INTO Users ('Name','Email', 'Username', 'Password') VALUES (?,?,?,?);"

        #Execute SQL
        self.cur.execute(sql,values)
        self.con.commit()

        userID = self.checkLogin(username,password)[1]
        self.createCalendar(userID, "Default", "Orange")

        return True

    def checkIfUserExist(self,email,username, id=None):
        #See if a user already exists
        if id == None:
            sql = "SELECT Email,Username FROM users WHERE Email=? OR Username=?"
            self.cur.execute(sql, (email,username))
        else:
            sql = "SELECT Email,Username FROM users WHERE (Email=? OR Username=?) AND (ID <>  ?)"
            self.cur.execute(sql, (email,username,id))

        rows = self.cur.fetchall()
        for user in rows:
            if user[0] == email:
                return "That email aready exists!"
            else:
                return "That username already Exists! Try Another one."
        return False

    def checkLogin(self, username, password):
        #See if a username and password is valid
        sql = "SELECT ID,Password FROM users WHERE Username=?"
        self.cur.execute(sql, (username,))
        rows = self.cur.fetchall()
        for user in rows:
            if self.hashPassword(password) == user[1]:
                return True, user[0]
        return False, None


    def validateEmail(self, email):
        #Makes sure an email is valid
        regx = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        p = re.compile(regx)

        if p.match(email):
            return True
        else:
            return False

    def hashPassword(self,password):
        #Hash the string.
        return hashlib.sha224(password.encode()).hexdigest()

    def createCalendar(self, userID, name, colour):
        #Create Values list, and SQL statement
        values = (name,userID, colour)
        sql = "INSERT INTO Calendars ('Name','UserID', 'Colour') VALUES (?,?,?);"

        #Execute SQL
        self.cur.execute(sql,values)
        self.con.commit()


    def getUserData(self,userID):
        #Get the calendars from a particular user
        sql = "SELECT ID ,Name,Colour FROM Calendars WHERE UserID=?"
        self.cur.execute(sql, (userID,))
        CalendarRows = self.cur.fetchall()

        #Get the details from a particular user
        sql = "SELECT Name,Email,Username FROM users WHERE ID=?"
        self.cur.execute(sql, (userID,))
        rows = self.cur.fetchall()
        for user in rows:
                return list(user) + list([CalendarRows])


    def createEvent(self, name, startTime, endTime, allDay, description, location, colour, calendarID):
        #Create Values list, and SQL statement
        values = (name, startTime, endTime,location,allDay, description, colour, calendarID)
        sql = "INSERT INTO Events ('Name','StartTimestamp', 'EndTimestamp', 'Location', 'AllDay', 'Description', 'Colour', 'CalendarID') VALUES (?,?,?,?,?,?,?,?);"

        #Execute SQL
        self.cur.execute(sql,values)
        self.con.commit()


    def getEvents(self, startTimestamp, endTimestamp, calendarID):
        #Get the calendars from a particular user
        sql = "SELECT * FROM Events WHERE ((StartTimestamp BETWEEN ? AND ?) AND CalendarID=?) OR ((EndTimestamp BETWEEN ? AND ?) AND CalendarID=?)"
        self.cur.execute(sql, (startTimestamp,endTimestamp,calendarID, startTimestamp,endTimestamp,calendarID))
        Rows = self.cur.fetchall()
        return Rows

    def getEventDetails(self,eventID):
        #Get the details about a particular event
        sql = "SELECT * FROM Events WHERE ID=?"
        self.cur.execute(sql,(eventID,))
        for row in self.cur.fetchall():
            return row

    def deleteEvent(self,eventID):
        #Delete an event by ID
        sql = "DELETE FROM Events WHERE ID=?"
        #Execute SQL
        self.cur.execute(sql,(eventID,))
        self.con.commit()

    def editEvent(self, eventID, name, startTime, endTime, allDay, description, location, colour):
        #Edits an event
        sql = "UPDATE Events SET Name = ?, StartTimestamp = ?, EndTimestamp = ?, Location = ?, AllDay=?, Description=?, Colour=? WHERE ID = ?"
        values = (name,startTime,endTime,location,allDay,description,colour, eventID)
        #Execute SQL
        self.cur.execute(sql,values)
        self.con.commit()

    def editUser(self, name, email, username, id, password=None):
        #EDITS USER
        email=email.lower()

        #Make sure email is valid
        if self.validateEmail(email) == False:
            return "Email Not Valid"

        #Makes sure all othe feilds are valid
        if name == "" or username == "":
            return "Fill In Missing Values"

        #See if a user already exists
        check = self.checkIfUserExist(email, username, id=id)
        if  check != False:
            return check

        #Create SQL Statement and Values to pass
        if password == None:
            sql = "UPDATE Users SET Name = ?,Email = ?,Username = ?  WHERE ID = ?"
            values = (name,email, username,id)
        else:
            sql = "UPDATE Users SET Name = ?,Email = ?,Username = ?,Password = ?  WHERE ID = ?"
            values = (name,email, username,self.hashPassword(password),id)


        #Execute SQL
        self.cur.execute(sql,values)
        self.con.commit()

        return True
