'''
Author: Robert Watts
Project: Computer Science Controlled Assessment 2019
File Name: EventViewer.py
Description: Displays the events on a canvas in a grid.
             Handles all user clicking on an event and
             user changing date.
'''
from tkinter import *
import time
import datetime
from calendarApp.EventDetails import EventDetails

class EventViewer (Canvas):

    def __init__(self, master, controller, database, userID, width =98, height=23, ** kw):
        #Initalise Class
        self.DB = database
        self.USERID = userID
        self.CALENDARS = self.DB.getUserData(self.USERID)[3]
        self.controller = controller

        #Define height and width of each cell
        self.WIDTH = width
        self.HEIGHT = height


        Canvas.__init__(self,master, height=(self.HEIGHT * 31), width=(self.WIDTH * 8), **kw)

        self.BACKGROUND = self.master.cget('bg')
        self.EventDetails = EventDetails(self, self.DB, self.BACKGROUND, self.controller)


    def createGrid(self):
        verticalLength = (self.HEIGHT * 24 )
        horizontalLength = (self.WIDTH * 7)

        #Create Vertical Grid Lines
        y = self.GRID_START_CORDINATE_Y
        x = self.GRID_START_CORDINATE_X
        for line in range(0, 8):
            self.create_line(x,y,x,y+verticalLength, tag="grid")
            x += self.WIDTH

        #Add Horizontal Grid Lines
        y = self.GRID_START_CORDINATE_Y
        x = self.GRID_START_CORDINATE_X
        for line in range(0, 25):
            self.create_line(x, y, x+horizontalLength, y, tag="grid")
            y +=  self.HEIGHT

    def createLabels(self, initalX, initalY):
        #Add Day Labels
        x =  initalX
        y = (initalY)/1.3 #OFfset From Top

        DateObject = datetime.datetime(self.currentDate[0], self.currentDate[1], self.currentDate[2], 0,0)
        for q in range(0,7):
            text = DateObject.strftime("%A\n%d %b")
            self.create_text(x+(self.WIDTH/2),y, text=text, tag="daysLabel")
            x += self.WIDTH
            DateObject += datetime.timedelta(days=1)

        #Add Time Labels
        x = (self.GRID_START_CORDINATE_X)/1.5    # Offset from Side
        y = self.GRID_START_CORDINATE_Y

        for time in range(0,24):
            text=str(time).zfill(2) + ":00"
            self.create_text(x,y, text=text, tag="timeLabels")
            y +=self.HEIGHT

    def displayEvent(self, year, month, day):
        self.currentDate = (year, month, day)

        self.configure(background=self.BACKGROUND)

        self.GRID_START_CORDINATE_Y = (self.HEIGHT * 25) - (self.HEIGHT * 24 ) + 35
        self.GRID_START_CORDINATE_X = (self.WIDTH * 8) - (self.WIDTH * 7.1 )
        #Work Out Start TImestamp
        startTime = datetime.datetime(year, month, day, 0,0)
        startTimestamp = time.mktime(startTime.timetuple())


        #Work End Start TImestamp 6 Days Later
        endTime = startTime + datetime.timedelta(days=6,hours=23,minutes=59, seconds=59)
        endTimestamp = time.mktime(endTime.timetuple())



        #Get Events from all user calendars
        events = []
        for calendar in self.CALENDARS:
            events += self.DB.getEvents(startTimestamp, endTimestamp, calendar[0])


        eventsToGrid = []
        allDayEvents = []
        #For every Event
        for event in events:

            #Work Out Start Day
            startDay = int((event[2] - startTimestamp) / 86400 ) + 1
            #If Event is only on one day
            if event[3] == None:
                endDay = startDay
            else:
                endDay = int((event[3] - startTimestamp) / 86400) + 1

            #Length of event in days
            eventLength = (endDay - startDay) +1

            #If Event is Allday
            if event[5] == True:


                #Split event into days
                for x in range(startDay,startDay + eventLength):
                    if 1 <= x <= 7 :
                        allDayEvents.append({
                            "ID":event[0],
                            "name":event[1],
                            "day": x,
                            "location":event[4],
                            "calendarID":event[6],
                            "description":event[7],
                            "colour":event[8]
                        })

            else:
                #Get start and end Times
                if event[2] < startTimestamp:
                    startTime = int(datetime.datetime.fromtimestamp(startTimestamp).strftime("%H%M"))
                else:
                    startTime = int(datetime.datetime.fromtimestamp(event[2]).strftime("%H%M"))

                endTime = int(datetime.datetime.fromtimestamp(event[3]).strftime("%H%M"))

                #Event split into the individual day (if multi day)
                splitEvent = []

                if startDay == endDay:
                    #Add a single day event
                    splitEvent.append([startDay,startTime, endTime])
                else:
                    splitEvent.append([startDay,startTime, 2400])
                    if endDay <= 7:
                        splitEvent.append([endDay,0000, endTime])

                    for y in range(startDay+1,(startDay + eventLength)-1):
                        if y <= 7:
                            splitEvent.append([y,0000, 2400])

                #For every part of an event add it to the eventsToGrid list
                for part in splitEvent:
                    eventsToGrid.append({
                        "ID":event[0],
                        "name":event[1],
                        "day": part[0],
                        "startTime": part[1],
                        "endTime": part[2],
                        "location":event[4],
                        "calendarID":event[6],
                        "description":event[7],
                        "colour":event[8],
                        "startTimestamp": event[2],
                        "endTimestamp": event[3]
                    })



        self.clearCanvas()
        self.drawAllDayEvents(allDayEvents)
        #self.createGrid()

        self.drawEvents(eventsToGrid)
        self.createNavButtons()

    def drawEvents(self,events):
        #For every day
        for day in range(1,8):
            eventsToday = []
            eventDepth = [0] * 1440

            #Run through events
            for x in range(len(events) - 1, -1, -1):
                #If the event is on the current day
                if events[x]["day"] == day:
                    holder = events[x]
                    position = 0

                    #for every min in hour
                    for hour in range(holder["startTime"],holder["endTime"]-1):
                        #Work out hours and mins
                        hour = str(hour).zfill(4)
                        hoursNum,minsNum = hour[:2], hour[2:]

                        #Stops you having 12:76 (mins above 59)
                        if int(minsNum) > 59:
                            continue
                        #Calculate the number of mins since midnight and incroment that min by 1
                        mins = (int(hoursNum) * 60) + int(minsNum)
                        eventDepth[mins-1] += 1

                        if position < eventDepth[mins-1]:
                            position = eventDepth[mins-1]

                        eventsToday.append([x, position])


            for x in eventsToday:
                ID = x[0]
                start = events[ID]["startTime"]
                end = events[ID]["endTime"]
                y = eventDepth[start:end]
                widthDivider = max(y)

                if widthDivider == 0:
                    widthDivider=1

                #Calculate Cordinates
                x1 = self.GRID_START_CORDINATE_X + ((events[ID]["day"] - 1)*self.WIDTH) + ((x[1] -1)*(self.WIDTH/widthDivider))
                y1 = self.GRID_START_CORDINATE_Y + ((events[ID]["startTime"]/100)*self.HEIGHT)
                x2 = x1 + (self.WIDTH/widthDivider)
                y2 = self.GRID_START_CORDINATE_Y + ((events[ID]["endTime"]/100)*self.HEIGHT)


                tag = "eventClick " + str(events[ID]["ID"]) + " event"
                self.create_rectangle(x1, y1, x2, y2, fill=events[ID]["colour"], tags=tag)

                #Calculate event name width + shorten it
                eventName = events[ID]["name"]
                eventNameLength = int(len(events[ID]["name"]) * (0.2*widthDivider))

                #Find the first space and cut it there, and add a ...
                for x in range(eventNameLength, -1, -1):
                    if eventName[x] == " ":
                        eventName = eventName[0:x] + "..."
                        break
                #Draw Text
                self.create_text((x1 + ((x2-x1)*0.1), 0.5*(y2-y1) + y1), text=eventName, anchor="w", width=(x2-x1)*0.8, tags=tag)

        self.tag_bind("eventClick","<Button-1>", self.EventDetails.eventClick)

    def drawAllDayEvents(self, events):
        maxEvents = [0,0,0,0,0,0,0]
        for event in events:
            event["eventDepth"] = maxEvents[event["day"] - 1]
            maxEvents[event["day"] - 1] += 1

        maxEventsNum = max(maxEvents)

        for event in events:
            x1 = self.GRID_START_CORDINATE_X + ((event["day"] - 1)*self.WIDTH)
            y1 = self.GRID_START_CORDINATE_Y + (event["eventDepth"] * self.HEIGHT)
            x2 = x1 + self.WIDTH
            y2 = y1 + self.HEIGHT
            tag = "eventClick " + str(event["ID"]) + " event"
            self.create_rectangle(x1, y1, x2, y2, fill=event["colour"], tags="test", dash=(4, 4), tag=tag)
            self.create_text((0.5*(x2-x1) + x1, 0.5*(y2-y1) + y1), text=event["name"], anchor="center", width=(x2-x1-15), tag=tag )

        self.createAllDayGrid(maxEventsNum)
        y = self.GRID_START_CORDINATE_Y
        x = self.GRID_START_CORDINATE_X
        self.GRID_START_CORDINATE_Y += (maxEventsNum * self.HEIGHT) + (self.HEIGHT / 10)
        self.createLabels(x, y)
        self.createGrid()

    def createAllDayGrid (self, NumOfEvents):
        # verticalLength = (self.HEIGHT * 24 )
        horizontalLength = (self.WIDTH * 7)
        GridHeight = (NumOfEvents )*self.HEIGHT
        #Create Vertical Grid Lines
        y = self.GRID_START_CORDINATE_Y
        x = self.GRID_START_CORDINATE_X

        for line in range(0, 8):
            self.create_line(x,y,x,y+ GridHeight, tag="grid")
            x += self.WIDTH

        y = self.GRID_START_CORDINATE_Y
        x = self.GRID_START_CORDINATE_X
        self.create_line(x, y, x+horizontalLength, y, tag="grid")
        self.create_line(x, y+GridHeight, x+horizontalLength, y+GridHeight, tag="grid")


    def createNavButtons(self):
        leftButton =Button(self, text="<--",  command=self.leftButtonClick)
        self.create_window(40, 0, anchor=NW, window=leftButton, tag="grid")

        todayButton = Button(self, text="Today", command=self.todayButtonClick)
        self.create_window(80, 0, anchor=NW, window=todayButton, tag="grid")

        rightButton = Button(self, text="-->", command=self.rightButtonClick)
        self.create_window(150, 0, anchor=NW, window=rightButton, tag="grid")

    def todayButtonClick(self):
        now = datetime.datetime.now()
        self.displayEvent(now.year,now.month,now.day)

    def leftButtonClick(self):
        currentDateObject = datetime.datetime(self.currentDate[0], self.currentDate[1], self.currentDate[2], 0,0)
        newDateObject = currentDateObject - datetime.timedelta(days=7)
        self.displayEvent(newDateObject.year,newDateObject.month,newDateObject.day)

    def rightButtonClick(self):
        currentDateObject = datetime.datetime(self.currentDate[0], self.currentDate[1], self.currentDate[2], 0,0)
        newDateObject = currentDateObject + datetime.timedelta(days=7)
        self.displayEvent(newDateObject.year,newDateObject.month,newDateObject.day)

    def clearCanvas(self):
        self.delete("all")
