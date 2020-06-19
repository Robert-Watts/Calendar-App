'''
Author: Robert Watts
Project: Computer Science Controlled Assessment 2019
File Name: EventDetails.py
Description: Display the details for an event within
             a canvas. Provides the users options to
             edit and delete an event.
'''

from tkinter import *
from datetime import datetime
from tkinter import messagebox

class EventDetails:
    def __init__(self,canvas, database, defualtBackgroundColour, controller):
        #Inialise Class
        self.CANVAS = canvas
        self.DB = database
        self.defaultBackground = defualtBackgroundColour
        self.controller = controller

    def eventClick(self, event, *args):
        #Find Item + Get ID
        CanvasItem = event.widget.find_closest(event.x, event.y)
        eventID = event.widget.gettags(CanvasItem[0])[1]

        #Hide everything on items on the canvas
        thingsOnCanvas = self.CANVAS.find_withtag("event") + self.CANVAS.find_withtag("timeLabels") + self.CANVAS.find_withtag("daysLabel") + self.CANVAS.find_withtag("grid")
        for id in thingsOnCanvas:
            self.CANVAS.itemconfigure(id, state='hidden')

        self.drawEventDetails(eventID)
        self.drawButtons(eventID)

    def drawEventDetails (self, eventID):
        #Get Events
        event = self.DB.getEventDetails(eventID)

        #Change Background Colour
        self.CANVAS.configure(background=event[8])
        x = datetime.fromtimestamp(event[2])

        #Work out which Items the user filled in and added them to the list
        items = [
            ["Name:", event[1]],
            ["Start Date:", x.strftime("%A %d %B %Y @ %X")]
        ]
        if event[3] != None:
            items.append(["End Date:", datetime.fromtimestamp(event[3]).strftime("%A %d %B %Y @ %X")])
        if event[4] != "":
            items.append(["Location:", event[4]])
        if event[5] == 1:
            items.append(["All Day?", "Yes"])
        else:
            items.append(["All Day?", "No"])
        items.append(["Description:", event[7].strip("\n")])

        #Define the inital position for the grid
        y = 80
        for item in items:
            #Display the infomation about the event
            self.CANVAS.create_text(40,y, text=item[0], anchor="w", tag="eventDetails", font = ('Calibri', 15, 'bold'))
            self.CANVAS.create_text(160,y, text=item[1], anchor="w", tag="eventDetails", font = ('Calibri', 15, ''))
            y += 30

    def drawButtons (self, eventID):
        #Draw Buttons
        BackButton = Button(self.CANVAS, text = "Back", anchor = W, command=self.backButtonPress)
        BackButton_window = self.CANVAS.create_window(40, 20, anchor=NW, window=BackButton, tag="eventDetails")

        EditEventButton = Button(self.CANVAS, text = "Edit Event", anchor = W, command=lambda id=eventID: self.controller.frames["createEvent"].editEvent(id))
        EditEventButton_window = self.CANVAS.create_window(80, 20, anchor=NW, window=EditEventButton, tag="eventDetails")

        DeleteEventButton = Button(self.CANVAS, text = "Delete Event", anchor = W, command=lambda id=eventID: self.deleteButtonPress(id))
        DeleteEventButton_window = self.CANVAS.create_window(150, 20, anchor=NW, window=DeleteEventButton, tag="eventDetails")

    def backButtonPress(self):
        #Delete all of the event detial items
        eventDetailsOnCanvas = self.CANVAS.find_withtag("eventDetails")
        for id in eventDetailsOnCanvas:
            self.CANVAS.delete(id)

        #Display all of the hidden items
        hiddenOnCanvas = self.CANVAS.find_withtag("event") + self.CANVAS.find_withtag("timeLabels") + self.CANVAS.find_withtag("daysLabel") + self.CANVAS.find_withtag("grid")
        for id in hiddenOnCanvas:
            self.CANVAS.itemconfigure(id, state='normal')

        self.CANVAS.configure(background=self.defaultBackground)

    def deleteButtonPress(self, id):
        #Delete Button press
        comfirm = messagebox.askyesno("Delete Event","Are you sure you want to delete this event?")
        if comfirm == True:
            self.DB.deleteEvent(id)
            self.CANVAS.displayEvent(self.CANVAS.currentDate[0],self.CANVAS.currentDate[1],self.CANVAS.currentDate[2])
