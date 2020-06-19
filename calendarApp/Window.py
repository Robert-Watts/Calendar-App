'''
Author: Robert Watts
Project: Computer Science Controlled Assessment 2019
File Name: Login.py
Description: Hanndles all of the frames within the program.
             Allows switching between frames and storing
             them for use later.
'''

from tkinter import *
from calendarApp.Login import *
from calendarApp.CreateAccount import createAccount
from calendarApp.Database import *

class Window(Tk):
    def __init__(self, *args, **kwargs):
        #Define Tkinter Window
        Tk.__init__(self, *args, **kwargs)

        #Define Database Connection
        self.DB = Database()

        #Create Container in window
        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand = True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        #Change window text
        self.title("Calendar!")

        #User Id when logged in
        self.USERID = None

        self.frames = {}

        #Create long and create account frames
        for F in [login, createAccount]:
            self.createFrame(F)

        #Display login page
        self.show_frame("login")


    def createFrame(self,newFrame):
        #create a new frame
        frame = newFrame(self.container, self, self.DB)
        self.frames[newFrame.__name__] = frame
        frame.grid(row=0, column=0, sticky="nsew")


    def show_frame(self, FrametoShow):
        #Display a frame
        frame = self.frames[FrametoShow]
        frame.tkraise()


