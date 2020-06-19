'''
Author: Robert Watts
Project: Computer Science Controlled Assessment 2019
File Name: DatePicker.py
Description: Creates a date picker that allows the user to select
             a day from any month and year. Outputs their selection
             to the command variable.
'''

from tkinter import *
from calendar import monthrange, month_name
import datetime


class datePicker(Frame):
    def __init__(self, master=None, command=None, ** kw):
        self.command = command
        Frame.__init__(self,master,**kw)

        self.populateForm()
        self.navButtonClick("t")

    def populateForm(self):
        #Create Title
        self.title = Label(self, font='comic-sans-ms 11 bold')
        self.title.grid(in_=self, column=0, row=0, columnspan=7)

        #Create Nav DayButtons
        self.navButtons = []

        self.navButtons.append(Button(self, text="<--", command=lambda: self.navButtonClick("l")))
        self.navButtons[-1].grid(in_=self, column=0, row=1, columnspan=2)

        self.navButtons.append(Button(self, text="-->", command=lambda: self.navButtonClick("r")))
        self.navButtons[-1].grid(in_=self, column=5, row=1, columnspan=2)

        self.navButtons.append(Button(self, text="Today", command=lambda: self.navButtonClick("t")))
        self.navButtons[-1].grid(in_=self, column=2, row=1, columnspan=3)

        #Create Labels
        days = ["Mon ", "Tues", "Weds", "Thur", "Fri ", "Sat ", "Sun "]
        self.DayLabels = []
        ColumnCount = 0
        for day in days:
            self.DayLabels.append(Label(self,text=day))
            self.DayLabels[-1].grid(in_=self, column=ColumnCount, row=2)
            ColumnCount += 1

    def navButtonClick(self, command):
        if command == "l":
            self.Year, self.Month = self.PreviousYearMonth(self.Year, self.Month)
        elif command == "r":
            self.Year, self.Month = self.NextYearMonth(self.Year, self.Month)
        elif command == "t":
            now = datetime.datetime.now()
            self.Year = now.year
            self.Month = now.month

        self.DisplayMonth(self.Year,self.Month)

    def DisplayMonth(self, year, month):
        #Delete Month
        try:
            for x in self.DayButtons:
                x.destroy()
        except:
            pass
        #Change Title Text
        text = month_name[month]  + " " + str(year)
        self.title['text'] = text

        #Create new buttons
        self.DayButtons = []

        #Get details about the month in question:
        monthDetails = monthrange(year, month)
        gridPosition = [monthDetails[0], 3]

        for x in range(0, monthDetails[1]):
            #Work out position in grid
            if gridPosition[0] % 7 == 0:
                gridPosition[0] = 0
                gridPosition[1] += 1
            gridPosition[0] += 1
            text = x+1
            if text <= 9:
                text = "0" + str(text)

            #Create and pack da button
            self.DayButtons.append(Button(self, text=text, command=lambda day=int(text):self.dayButtonPressed(self.Year,self.Month,day)))
            self.DayButtons[-1].grid(in_=self, column=gridPosition[0]-1, row=gridPosition[1])

    def dayButtonPressed(self,year,month,day):
        try:
            output = (year,month,day)
            self.command(output)
        except Exception as e:
            print("Date Picker Error: ",e)



    def NextYearMonth(self, year, month):
        if month == 12:
            return year + 1, 1
        else:
            return year, month+1

    def PreviousYearMonth(self, year, month):
        if month == 1:
            return year - 1, 12
        else:
            return year, month-1
