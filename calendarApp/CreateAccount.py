'''
Author: Robert Watts
Project: Computer Science Controlled Assessment 2019
File Name: CreateAccount.py
Description: Creates a form to create and edit
             account details.
'''

from tkinter import *
from calendarApp.mainPage import *

class createAccount(Frame):
    def  __init__ (self, parent, controller, database):
        #Initalise program
        Frame.__init__(self,parent)
        self.DB = database
        self.controller = controller

        self.userID = None

        #Create Labels
        nameText = Label(self, text="Full Name")
        emailText = Label(self, text="Email")
        usernameText = Label(self, text="Username")
        passwordText = Label(self, text="Password")

        #Put labels on Grid
        nameText.grid(column=0, row=0)
        emailText.grid(column=0, row=1)
        usernameText.grid(column=0, row=2)
        passwordText.grid(column=0, row=3)

        #Create entry
        self.name = Entry(self,width=30)
        self.name.grid(column=1, row=0, padx=10)

        self.email = Entry(self,width=30)
        self.email.grid(column=1, row=1, padx=10)

        self.username = Entry(self,width=30)
        self.username.grid(column=1, row=2, padx=10)

        #Create password entry
        self.password = Entry(self,width=30)
        self.password.grid(column=1, row=3)
        self.password.config(show="*")

        #Create error message label
        self.errorLabel = Label(self, text="")
        self.errorLabel.grid(column=0, row=4, sticky=W, columnspan=2)
        self.errorLabel.config(fg='red')

        #Create Login Button + Create account button
        self.createAccountButton = Button(self, text="Create Account", width=12, command=self.createAccount)
        self.createAccountButton.grid(column=1, row=5, columnspan=2, sticky=W, padx=10, pady=10)
        self.LoginButton = Button(self, text="Back to Login", width=12, command=lambda: controller.show_frame("login"))
        self.LoginButton.grid(column=0, row=5, padx=10, pady=10, sticky=E)

    def createAccount(self):
        #Get Data from form
        usernameHolder = self.username.get()
        passwordHolder = self.password.get()
        nameHolder = self.name.get()
        emailHolder = self.email.get()

        #Check if user Exists and run
        if self.userID == None:
            accountCheck = self.DB.createAccount(nameHolder,emailHolder,usernameHolder,passwordHolder)
        else:
            if passwordHolder == "":
                passwordHolder = None
            accountCheck = self.DB.editUser(nameHolder,emailHolder,usernameHolder,self.userID,password = passwordHolder)

        if accountCheck == True:
            if self.userID == None:
                #log user in
                loginCheck = self.DB.checkLogin(usernameHolder,passwordHolder)
                self.controller.USERID = loginCheck[1]
                #Add Frame and Open
                self.controller.createFrame(mainPage)


            #Clear Form and change frame
            self.resetForm()
            self.controller.show_frame("mainPage")

        else:
            #Display Error Message
            self.errorLabel.config(text=accountCheck)

    def resetForm(self):
        #Clears the form
        self.name.delete(0, 'end')
        self.username.delete(0, 'end')
        self.password.delete(0, 'end')
        self.email.delete(0, 'end')
        self.createAccountButton["text"] ="Create Account"
        self.errorLabel.config(text="")

    def editUser(self):
        #Get User Details + resets form
        self.userID = self.controller.USERID
        details = self.DB.getUserData(self.controller.USERID)
        self.resetForm()

        #Put user details info form
        self.username.insert(END, details[2])
        self.name.insert(END, details[0])
        self.email.insert(END, details[1])
        self.createAccountButton["text"] ="Edit Account"
        self.LoginButton.grid_forget()

        #Add Instructions Text
        instructionsText = Label(self, text="To edit your password enter a new one \notherwise leave this box blank.")
        instructionsText.grid(column=2, row=3)
