'''
Author: Robert Watts
Project: Computer Science Controlled Assessment 2019
File Name: DateTimePopup.py
Description: Creates a popup that allows the user to select
             a day from any month and year, as well as a time.
             Outputs their selection to the outputFunction
             variable.
'''


from tkinter import *
from calendarApp.DatePicker import *
import datetime
from tkinter import messagebox


class DateTimePopup:

    def __init__(self, outputFunction):
        #Create Popup Window
        self.window = Toplevel()
        self.window.wm_title("Pick Date & Time")
        self.window.grab_set()

        #Define the variables
        self.outputVariable = outputFunction
        self.date = None

        #Create a list of all hours and mins avaliable
        hours = list(range(0, 24))
        mins = list(range(0, 60))

        #Create Time Label
        selectTimeLabel = Label(self.window, text="Select Time:", font='Helvetica 16 bold', fg="orange")
        selectTimeLabel.grid(column=0, row=0, columnspan=3,sticky="nsew")

        #Create Hours dropdown
        self.startHoursValue = StringVar(self.window)
        self.startHoursValue.set(hours[0]) # initial value
        self.startHours = OptionMenu(self.window, self.startHoursValue, *hours)
        self.startHours.grid(column=0, row=1,sticky="e")

        #Create a colon label
        colon = Label(self.window, text=":", font='Helvetica 18 bold')
        colon.grid(column=1, row=1)

        #Create a mins dropdown
        self.startMinsValue = StringVar(self.window)
        self.startMinsValue.set(mins[0]) # initial value
        self.startMins = OptionMenu(self.window, self.startMinsValue, *mins)
        self.startMins.grid(column=2, row=1,sticky="w")

        #Create a select date Label
        selectDateLabel = Label(self.window, text="Select Date:", font='Helvetica 16 bold', fg="orange")
        selectDateLabel.grid(column=0, row=2, columnspan=3,sticky="nsew")

        #Create a date picker
        self.selectedDate = Label(self.window, text="", font='Helvetica 8')
        self.selectedDate.grid(column=0, row=3, columnspan=3,sticky="nsew")
        self.startDatePicker = datePicker(self.window, command=self.datePickerReturn, borderwidth=2, relief="groove")
        self.startDatePicker.grid(column=0, row=4, columnspan=3)

        #Create save button.
        SaveButton = Button(self.window, text="Save", bg="lightblue", command=self.saveButtonPress)
        SaveButton.grid(column=0, row=5, padx=10, pady=10, sticky="nsew", columnspan=3)

    def datePickerReturn(self, dateClicked):
        #Save date from date picker output
        self.date = dateClicked
        dateObject = datetime.datetime(self.date[0], self.date[1], self.date[2])
        text = dateObject.strftime("%A %d %B %Y")
        self.selectedDate.config(text=text)

    def saveButtonPress(self):
        #Handels save button press
        #Get values from form + Validate
        hour = int(self.startHoursValue.get())
        min = int(self.startMinsValue.get())
        if self.date == None:
            messagebox.showerror("Error", "Please Select a Date!")
        else:
            #Output data to output variable.
            output = self.date + (hour, min)
            try:
                self.outputVariable(output)
            except:
                pass
            self.window.destroy()
