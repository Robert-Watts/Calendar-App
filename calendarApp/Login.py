'''
Author: Robert Watts
Project: Computer Science Controlled Assessment 2019
File Name: Login.py
Description: Handles the user logging into the program.
'''

from tkinter import *
from calendarApp.mainPage import *

class login(Frame):
    def  __init__ (self, parent, controller, database):
        Frame.__init__(self,parent)
        self.DB = database
        self.controller = controller
        #Create  labels
        usernameText = Label(self, text="Username")
        passwordText = Label(self, text="Password")
        usernameText.grid(column=0, row=1)
        passwordText.grid(column=0, row=2)

        #Create Username entry
        self.username = Entry(self,width=30)
        self.username.grid(column=1, row=1, padx=10)

        #Create password entry
        self.password = Entry(self,width=30)
        self.password.grid(column=1, row=2)
        self.password.config(show="*")

        #Create error message label
        self.errorLabel = Label(self, text="")
        self.errorLabel.grid(column=0, row=3, sticky=W, columnspan=2)
        self.errorLabel.config(fg='red')

        #Create Login Button + Create account button
        createAccountButton = Button(self, text="Create Account", width=12, command=lambda: controller.show_frame("createAccount"))
        createAccountButton.grid(column=0, row=4, columnspan=2, sticky=W, padx=10, pady=10)
        LoginButton = Button(self, text="Login", width=12, command=self.Login)
        LoginButton.grid(column=1, row=4, padx=10, pady=10, sticky=E)

    def Login(self):
        #Get Data from form
        usernameHolder = self.username.get()
        passwordHolder = self.password.get()

        #Check if user Exists and run
        loginCheck = self.DB.checkLogin(usernameHolder,passwordHolder)
        if loginCheck[0]:
            #Save the users ID
            self.controller.USERID = loginCheck[1]
            #Add Frame and Open
            self.controller.createFrame(mainPage)
            self.controller.show_frame("mainPage")

        else:
            #Display Error Message
            self.errorLabel.config(text="Username or Password Incorect")
