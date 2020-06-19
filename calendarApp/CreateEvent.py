'''
Author: Robert Watts
Project: Computer Science Controlled Assessment 2019
File Name: CreateEvent.py
Description: Creates a form to create and edit
             event details.
'''

from tkinter import *
from calendarApp.DateTimePopup import *
import datetime
from tkinter import messagebox
import time

class createEvent(Frame):
    def  __init__ (self, parent, controller, database):
        #Initalise Frame
        Frame.__init__(self,parent)
        self.DB = database
        self.controller = controller

        #Create and Pack labels
        labelsText = ["Name","Start Time & Date","End Time & Date","All Day?","Description","Location","Colour"]
        labels = []
        row = 1
        for text in labelsText:
            labels.append(Label(self, text=text))
            labels[-1].grid(column=0, row=row)
            row += 1

        #Create Text Boxes
        self.name = Entry(self)
        self.name.grid(column=1, row=1, padx=10,sticky="ew", columnspan=5)
        self.location = Entry(self)
        self.location.grid(column=1, row=6, padx=10,sticky="ew", columnspan=5)

        #Create Check Box
        self.allDayValue = IntVar()
        self.allDay = Checkbutton(self, text="All Day",variable=self.allDayValue)
        self.allDay.grid(column=1, row=4, padx=10,sticky="w", columnspan=5)

        #Create Text Area
        self.description = Text(self,height=3)
        self.description.grid(column=1, row=5, padx=10, sticky="ew", columnspan=5)

        #Create Dropdown
        colours = ["Red","Orange","Pink","Green", "Yellow", "Light Blue", "Lavender",
                   "Wheat", "Indian Red", "Pale Green", "Deep Pink", "Slate Blue"]
        self.colourValue = StringVar(self)
        self.colourValue.set(self.controller.USER_DETAILS[3][0][2]) # initial value
        self.colour = OptionMenu(self, self.colourValue, *colours)
        self.colour.grid(column=1, row=7, padx=10, sticky="ew", columnspan=5)

        #Create Start Time Button / Popup
        self.startTime = None
        startTimeButton = Button(self, text="Choose Date", width=12, command=lambda: DateTimePopup(self.changeStartTime))
        startTimeButton.grid(column=1, row=2, padx=10, pady=10, sticky="w")

        #Start Time to de displayed once chosen
        self.startTimeText = Label(self, text="")
        self.startTimeText.grid(column=2, row=2, sticky="w")

        #Create End Time Button / Popup
        self.endTime = None
        endTimeButton = Button(self, text="Choose Date", width=12, command=lambda: DateTimePopup(self.changeEndTime))
        endTimeButton.grid(column=1, row=3, padx=10, pady=10, sticky="w")

        #End Time to de displayed once chosen
        self.endTimeText = Label(self, text="")
        self.endTimeText.grid(column=2, row=3, sticky="w")

        self.createEventButton = Button(self, text="Create Event", width=12, command=self.CreateEventButtonPress)
        self.createEventButton.grid(column=1, row=8, padx=10, pady=10, sticky="w")

        clearFormButton = Button(self, text="Clear Form", width=12, command=self.clearForm)
        clearFormButton.grid(column=2, row=8, padx=10, pady=10, sticky="w")

        self.IsEditEvent = False
        self.EditID = None

    def changeStartTime (self, newTime):
        self.startTime = newTime
        dateObject = datetime.datetime(newTime[0], newTime[1], newTime[2], newTime[3], newTime[4])
        text = dateObject.strftime("%A %d %B %Y @ %X")
        self.startTimeText.config(text=text)

    def changeEndTime (self, newTime):
        self.endTime = newTime
        dateObject = datetime.datetime(newTime[0], newTime[1], newTime[2], newTime[3], newTime[4])
        text = dateObject.strftime("%A %d %B %Y @ %X")
        self.endTimeText.config(text=text)

    def editEvent(self,eventID):
        #Display Frame + Reset Form + Get event Details
        self.controller.show_frame("createEvent")
        self.clearForm()
        eventDetails = self.DB.getEventDetails(eventID)

        #Populate Form
        self.name.insert(END, eventDetails[1])
        startTime = datetime.datetime.fromtimestamp(eventDetails[2])
        self.changeStartTime((int(startTime.strftime("%Y")), int(startTime.strftime("%m")), int(startTime.strftime("%d")), int(startTime.strftime("%H")), int(startTime.strftime("%M"))))
        if eventDetails[3] != None:
            endTime = datetime.datetime.fromtimestamp(eventDetails[3])
            self.changeEndTime((int(endTime.strftime("%Y")), int(endTime.strftime("%m")), int(endTime.strftime("%d")), int(endTime.strftime("%H")), int(endTime.strftime("%M"))))
        if eventDetails[5] == 1:
            self.allDay.select()
        self.description.insert(END,eventDetails[7])
        self.location.insert(END, eventDetails[4])
        self.colourValue.set(eventDetails[8])

        self.createEventButton["text"] ="Edit Event"

        self.IsEditEvent = True
        self.EditID = eventID


    def CreateEventButtonPress(self):
        #Get Form Info
        name = self.name.get()
        start = self.startTime
        end = self.endTime
        allDay = self.allDayValue.get()
        description = self.description.get("1.0",END)
        location = self.location.get()
        colour = self.colourValue.get()

        #Validate Form
        if name == "" or start == None:
            messagebox.showinfo("", "At a minimum an event needs a name and a start date.")
            return
        StartUnixTime = time.mktime(datetime.datetime(start[0], start[1], start[2], start[3], start[4]).timetuple())
        try:
            EndUnixTime = time.mktime(datetime.datetime(end[0], end[1], end[2], end[3], end[4]).timetuple())
        except:
            EndUnixTime = None
        if allDay == 0:
            if end == None:
                messagebox.showinfo("", "No End Time Selected")
                return

            if EndUnixTime <= StartUnixTime:
                messagebox.showinfo("", "This event finishes before it starts! Please change either the start or end time.")
                return

        #Get Default Calendar ID
        calendarID = self.controller.USER_DETAILS[3][0][0]

        if self.IsEditEvent == False:
            #Create Event
            self.DB.createEvent(name,StartUnixTime,EndUnixTime,allDay, description, location, colour, calendarID)
        else:
            #Edit Event
            self.DB.editEvent(self.EditID, name,StartUnixTime,EndUnixTime,allDay, description, location, colour)

        #Refresh Calendar View
        self.controller.frames["mainPage"].eventViewerHolder.displayEvent(self.controller.frames["mainPage"].eventViewerHolder.currentDate[0],
                                                                          self.controller.frames["mainPage"].eventViewerHolder.currentDate[1],
                                                                          self.controller.frames["mainPage"].eventViewerHolder.currentDate[2])

        #Clear Form and change frame
        self.clearForm()
        self.controller.show_frame("mainPage")

    def clearForm(self):
        #Reset the form
        self.name.delete(0,END)
        self.name.focus_set()
        self.startTime = None
        self.endTime = None
        self.startTimeText.config(text="")
        self.endTimeText.config(text="")
        self.allDay.deselect()
        self.description.delete("1.0",END)
        self.location.delete(0,END)
        self.colourValue.set(self.controller.USER_DETAILS[3][0][2])
        self.IsEditEvent = False
        self.EditID = None
        self.createEventButton["text"] ="Create Event"
