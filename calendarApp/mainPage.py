'''
Author: Robert Watts
Project: Computer Science Controlled Assessment 2019
File Name: Login.py
Description: Handles the main window that the user
             comes to. Creates menus and the event
             viwer.
'''

from tkinter import *
from calendarApp.CreateEvent import *
from calendarApp.EventViewer import *
from calendarApp.DatePicker import datePicker


class mainPage(Frame):
    def  __init__ (self, parent, controller, database):
        Frame.__init__(self,parent)
        self.DB = database
        self.controller = controller
        self.parent = parent

        #Resize Window
        self.controller.geometry("1000x730")

        #Get User Details
        self.controller.USER_DETAILS = self.DB.getUserData(self.controller.USERID)
        self.USER_DETAILS = self.controller.USER_DETAILS

        self.createMenu()

        self.createSideBar()
        self.addFrames()

        self.eventViewerHolder = EventViewer(self,self.controller, self.DB, self.controller.USERID)
        self.eventViewerHolder.grid(row=0,column=1)

        #Display the events on Current Date
        now = datetime.datetime.now()
        self.calendarClick((now.year, now.month, now.day))

    def createMenu(self):
        #Create Menu
        self.menubar = Menu(self)

        #Create Menu Buttons
        self.menubar.add_command(label="Calendar!", command=lambda: [self.controller.show_frame("mainPage"),self.controller.frames["createEvent"].clearForm()])
        self.menubar.add_command(label="Create New Event", command=lambda: self.controller.show_frame("createEvent"))
        self.menubar.add_command(label=self.USER_DETAILS[0],command=lambda: [self.controller.show_frame("createAccount"),self.controller.frames["createAccount"].editUser()])

        #Pack Menu
        self.controller.config(menu=self.menubar)

    def createSideBar(self):
        datePickerSide = datePicker(self, command=self.calendarClick)
        datePickerSide.grid(row=0,column=0, sticky="n")

    def addFrames(self):
        self.controller.createFrame(createEvent)

    def calendarClick(self, input):
        self.eventViewerHolder.displayEvent(input[0], input[1], input[2])
