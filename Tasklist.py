from tkinter import *
import sqlite3
import os
import random

global w1
global w2
global selectedCount
selectedCount = 0
global selectW
selectW = False
global editCount
editCount = 0
global editW
editW = False
global w2Count 
w2Count = 0
global w1Count
w1Count = 0

#Creates Accounts database and 2 tables in it if one does not exist yet
if os.path.exists("Accounts.db") == False:
    
    conn = sqlite3.connect("Accounts.db")
    c = conn.cursor()

    #this table holds all the users names and the their passwords
    accTable = '''CREATE TABLE Users (
        ID integer PRIMARY KEY,
        name varchar(100),
        password varchar(100)
    )'''

    #this table holds all the users tasks
    TaskTable= '''CREATE TABLE userTasks (
        userOfTasks integer NOT NULL,
        taskName varchar(20),
        task varchar(1000),
        FOREIGN KEY(userOfTasks) REFERENCES Users(ID)
    )'''

    c.execute(accTable)
    c.execute(TaskTable)
    conn.commit()
    conn.close()

#Function that creates window where you can make an account
def Register():
    global screen1
  
    
    screen1 = Toplevel(screen)
    screen1.title("Register")
    screen1.geometry("300x250")

    Label(screen1, text = "Create account").pack()
    Label(screen1, text = "").pack()
    Label(screen1, text = "Username").pack()
   

    global Username
    Username = Entry(screen1, width = 30)
    Username.pack()

    Label(screen1, text = "Password").pack()

    global Password 
    Password = Entry(screen1, width = 30, show='*')
    Password.pack()
   
    global existsLabel
    existsLabel = Label(screen1, fg='red', text="")

    global tooSmall
    tooSmall = Label(screen1, fg="red", text="")
    Button(screen1, text = "Register", width = 10, height = 1, command = createAcc, fg="green").pack()
    existsLabel.pack()

# Function checks if your account can be registered, it makes sure you dont make an account that has a password with less than 1 character or a name with less than 4 characters
# It also doesent let you create an account if an account with the same name and password already exists
def createAcc():
    global existsLabel
    global tooSmall
    
    conn = sqlite3.connect("Accounts.db")
    c = conn.cursor()
    findUser = ("SELECT * FROM Users WHERE name = ? AND password = ?")
    c.execute(findUser,[(Username.get()),(Password.get())])
    isUserTaken = c.fetchall()

    #if isUserTaken is TRUE it gives you a error message does not make a new account
    if isUserTaken:
        existsLabel['text'] = "User already exists"
    
    #if the the inputted is atleast 4 characters long and password atleast 1 character long it registers the account to the Users table
    else:
        if len(Username.get()) > 3 and len(Password.get()) >= 4:
            c.execute("INSERT INTO Users (name,password) VALUES (:name, :password)",
            {
            'name' : Username.get(),
            'password' : Password.get()
            })
            existsLabel['text'] = ""
            screen1.destroy()
           
        elif len(Password.get()) <4:
            existsLabel['text'] = "Password must be atleast 4 character long"
        elif len(Username.get()) <4:
            existsLabel['text'] = "Username must be atleast 4 characters long"

    conn.commit()
    conn.close

#This function creates a window where you can log in with you account
def Login():
    global screen2
    screen2 = Toplevel(screen)
    screen2.title("Log in")
    screen2.geometry("300x250")

    global spammerKick 
    spammerKick = 0

    global errorLabel
    errorLabel = Label(screen2, text="",fg="red")
    errorLabel.pack()

    Label(screen2, text = "Username").pack()

    global inputUsername
    inputUsername = Entry(screen2, width = 30)
    inputUsername.pack()

    Label(screen2, text = "Password").pack()

    global inputPassword 
    inputPassword = Entry(screen2, width = 30, show='*')
    inputPassword.pack()

    Button(screen2, text = "Log in", width = 10, height = 1, command = logginIn, fg="green").pack()

#This function checks what account you logged in with
def logginIn():
    global errorLabel
    global spammerKick

    conn = sqlite3.connect("Accounts.db")
    c = conn.cursor()

    findUser = ("SELECT * FROM Users WHERE name = ? AND password = ?")
    c.execute(findUser,[(inputUsername.get()),(inputPassword.get())])
    accountInput= c.fetchall()

    #opens taskList if you logged in with an registered account and saves the accounts id in a variable
    if accountInput:

        #finds the logged accounts id
        global findID
        findID = ("SELECT ID FROM Users WHERE name = ? AND password = ?")
        c.execute(findID,[inputUsername.get(),inputPassword.get()])

        #saves the found id to a variable
        global user_ID
        user_ID = c.fetchone()
        user_ID = int(user_ID[0])

        global w1
        w1 = False
        global w2
        w2 = False

        openTaskList()
        screen.destroy()
        
    else:
        #kicks you out of log in window if you get the acc name or password wrong 20 times
        randomErrorMessage = random.randint(0,5)
        spammerKick += 1
        if spammerKick == 20:
            screen2.destroy()
            spammerKick=0
        else:

            #Gives a random error message if you dont try to log in with a non existing account
            if randomErrorMessage == 0:
                errorLabel['text'] = "Something went wrong"
            elif randomErrorMessage == 1:
                errorLabel['text'] = "Try again"
            elif randomErrorMessage == 2:
                errorLabel['text'] = "bruh"
            elif randomErrorMessage == 3:
                errorLabel['text'] = "hmmm something is wrong"
            elif randomErrorMessage == 4:
                errorLabel['text'] = "Check for spelling mistakes"
            elif randomErrorMessage == 5:
                errorLabel['text'] = "nope"

#Creates the TaskList screen 
def openTaskList():
    global taskscreen
    taskscreen = Tk()
    taskscreen.geometry("1182x600")
    taskscreen.title("TaskList")

    Button(taskscreen, text="Log out", bg="lightGray", fg="blue",command= logOut, width=45).grid(row=0 ,column=0, columnspan=2)
    
    Button(taskscreen, text="Create new task", bg="lightGray", fg="green", width=55, command= createTask).grid(row=0 ,column=2, columnspan=2)

    Button(taskscreen, text="My tasks", bg="lightGrey", fg="green", width=30, command= showTasks).grid(row=0, column=4, columnspan=2)


def createTask():

    global w1
    w1 = True

    global w1Count
    w1Count += 1

    deleteselectW()
    deleteeditW()
    deletew2()
   
  
    #checks if you have already pressed the Create new task button if you have it deletes the existing labels and entrys... and makes new ones othervice it just creates new ones
    if w1Count == 1:

        global EmptyLabel
        EmptyLabel = Label(taskscreen, text="", width=22)
        EmptyLabel.grid(row=1, column=0, columnspan=1)

        global TaskNameLabel
        TaskNameLabel = Label(taskscreen, text="Task Name:", width=22)
        TaskNameLabel.grid(row=2, column=0, columnspan=1)

        global taskName
        taskName = Entry(taskscreen, bg="lightgrey", borderwidth=2,relief="flat")
        taskName.grid(row=2,column=2,columnspan=1)

        global EmptyLabel2
        EmptyLabel2 = Label(taskscreen, text="", width=22)
        EmptyLabel2.grid(row=3, column=0, columnspan=1)

        global TaskInfoLabel
        TaskInfoLabel = Label(taskscreen, text="Task description:", width=22)
        TaskInfoLabel.grid(row=4, column=0, columnspan=1)

        global taskInfo
        taskInfo = Text(taskscreen, width=40, height=10,bg="lightgrey", borderwidth=2, relief="flat")
        taskInfo.grid(row=4,column=2,columnspan=1)

        global creatingTaskButton
        creatingTaskButton = Button(taskscreen, text="Create task", fg="green", command=isTaskComplete)
        creatingTaskButton.grid(row=4, column=3,columnspan=4)

        global EmptyLabel3
        EmptyLabel3 = Label(taskscreen, text="", width=22)
        EmptyLabel3.grid(row=6, column=0, columnspan=1)

        global TaskAdviceLabel
        TaskAdviceLabel = Label(taskscreen, text="The task doesen't get saved if it doesen't have atleast 1 character and it can not have any spaces", width=80)
        TaskAdviceLabel.grid(row=7, column=1, columnspan=4)

        global TaskAdviceLabel3
        TaskAdviceLabel3 = Label(taskscreen, text="You can't make 2 same named tasks", width=40)
        TaskAdviceLabel3.grid(row=8, column=1, columnspan=4)

        global TaskAdviceLabel2
        TaskAdviceLabel2 = Label(taskscreen, text="The task description is optional", width=40)
        TaskAdviceLabel2.grid(row=9, column=1, columnspan=4)

    else:
        EmptyLabel3.destroy()
        EmptyLabel2.destroy()
        EmptyLabel.destroy()
        TaskAdviceLabel3.destroy()
        TaskAdviceLabel2.destroy()
        TaskAdviceLabel.destroy()
        TaskNameLabel.destroy()
        TaskInfoLabel.destroy()
        taskName.destroy()
        taskInfo.destroy()
        creatingTaskButton.destroy()
        w1Count = 0
        createTask()

#checks if your created task is viable

def isTaskComplete():

    global isTaskComplete
    conn = sqlite3.connect("Accounts.db")
    c = conn.cursor()

    global doesTaskAlreadyExist
    #saves a boolean value to doesTaskAlreadyExist, if its true it means that there is already a task with the same name
    doesTaskAlreadyExist = c.execute("SELECT taskName FROM userTasks WHERE taskName= ?",(taskName.get(),))
    doesTaskAlreadyExist = c.fetchall()
    if len(doesTaskAlreadyExist) == 0:
        doesTaskAlreadyExist = False
    else:
        doesTaskAlreadyExist = True
    #gives a -1 value to areSpacesInName if it finds spaces in the task name Entry 
    areSpacesInName = (taskName.get()).find(' ')

    #doesent create a new task if given task name is less than 1 character or if it has spaces or if a task with the same name already exists
    if len(taskName.get()) >= 1 and ((areSpacesInName != -1) == False) and (doesTaskAlreadyExist == False):

        c.execute("INSERT INTO userTasks(taskName,task, userOfTasks) VALUES (:taskName, :task, :userOfTasks)",
        {

        'taskName' : taskName.get(),
        'task' : taskInfo.get("1.0",END),
        'userOfTasks' : user_ID

        })
        conn.commit()
        conn.close
        createTask()

#shows all your tasks in a list and creates buttons "delete selected task", "edit seleced task" and "show selected task"
def showTasks():
    
    conn = sqlite3.connect("Accounts.db")
    c = conn.cursor()

    global w2
    w2 = True

    global w2Count
    w2Count += 1

    deleteselectW()
    deleteeditW()
    deletew1()

    #checks if you have already pressed the Show tasks button if you have it deletes the existing labels and entrys... and makes new ones othervice it just creates new ones
    if w2Count == 1:
        global myTasksLabel
        myTasksLabel = Label(taskscreen, text="Your tasks")
        myTasksLabel.grid(row=2)

        global UsersListBox
        UsersListBox = Listbox(taskscreen, width=40, height=20)
        UsersListBox.grid(row=3)

        c.execute("SELECT taskName FROM userTasks WHERE userOfTasks= ?",(user_ID,))
        printUsersTaskNames = c.fetchall()

        #when opening "my tasks" it inserts every task that haves the same id as the logged in account in the Listbox
        for index in printUsersTaskNames:
            UsersListBox.insert(END, index)

        global deleteButton
        deleteButton = Button(taskscreen, text="DELETE SELECTED TASK",  fg="red", width=33, command=deleteTask)
        deleteButton.grid(row=4, column=0)

        global editButton
        editButton = Button(taskscreen, text="EDIT SELECTED TASK", fg="orange", width=33, command=editTask)
        editButton.grid(row=5, column=0)

        global selectButton
        selectButton = Button(taskscreen, text="SHOW SELECTED TASK",fg="green", width=33, command=selectTask)
        selectButton.grid(row=6, column=0)
    else:
       
        editButton.destroy()
        selectButton.destroy()
        deleteButton.destroy()

        myTasksLabel.destroy()
        UsersListBox.destroy()
        w2Count = 0
        showTasks()
#deletes selected task
def deleteTask():
    
    conn = sqlite3.connect("Accounts.db")
    c = conn.cursor()

    selectedTask = UsersListBox.get(ANCHOR)

    UsersListBox.delete(ANCHOR)
    c.execute("DELETE FROM userTasks WHERE taskName = ?",(selectedTask))
    conn.commit()

#opens task editor 
def editTask():

    conn = sqlite3.connect("Accounts.db")
    c = conn.cursor()

    global editW
    editW = True

    global editCount
    editCount += 1

    deleteselectW()
    #checks if you have already pressed the Edit selected task button if you have it deletes the existing labels and entrys... and makes new ones othervice it just creates new ones
    if editCount == 1:

        global editNameLabel
        editNameLabel = Label(taskscreen, text="EDIT NAME")
        editNameLabel.grid(row=2, column=2)

        global editNameEntry
        editNameEntry = Entry(taskscreen)
        editNameEntry.grid(row=2, column=3)

        global selectedTask2
        selectedTask2 = UsersListBox.get(ANCHOR)

        global editDiscriptionLabel
        editDiscriptionLabel = Label(taskscreen, text="Edit task discription")
        editDiscriptionLabel.grid(row=3, column=2)

        global editDiscriptionText
        editDiscriptionText = Text(taskscreen, width=40, height=20, bg="lightgrey")
        editDiscriptionText.grid(row=3, column=3)

        global blankCommitLabel
        blankCommitLabel = Label(taskscreen, text="")
        blankCommitLabel.grid(row=4,column=2)

        global commitButton
        commitButton = Button(taskscreen, text="Commit changes", bg="green", command= changeTask)
        commitButton.grid(row=4,column=3)

        c.execute("SELECT taskName FROM userTasks WHERE taskName = ?",(selectedTask2))
        editName = c.fetchall()

        editNameEntry.insert(0, editName)


        c.execute("SELECT Task FROM userTasks WHERE taskName = ?",(selectedTask2))
        editDiscription = c.fetchall()

        editDiscriptionText.insert(1.0,*tuple(*tuple(editDiscription)))
        
    else:
        blankCommitLabel.destroy()
        commitButton.destroy()
        editDiscriptionLabel.destroy()
        editDiscriptionText.destroy()
        editNameEntry.destroy()
        editNameLabel.destroy()
        editCount = 0
        editTask()
    
def changeTask():

    conn = sqlite3.connect("Accounts.db")
    c = conn.cursor()

    areSpacesInName2 = (editNameEntry.get()).find(' ')

    global doesTaskAlreadyExist
    #saves a boolean value to doesTaskAlreadyExist, if its true it means that there is already a task with the same name
    doesTaskAlreadyExist = c.execute("SELECT taskName FROM userTasks WHERE taskName= ?",(editNameEntry.get(),))
    doesTaskAlreadyExist = c.fetchall()
    if len(doesTaskAlreadyExist) == 0:
        doesTaskAlreadyExist = False
    else:
        doesTaskAlreadyExist = True
    #if you try to commit an edited task with a name that has spaces or less than 1 character it doesent let you commit it 
    if len(editNameEntry.get()) >= 1 and ((areSpacesInName2 != -1) == False) and (doesTaskAlreadyExist ==False):
        c.execute("DELETE FROM userTasks WHERE taskName = ?",(selectedTask2))

        c.execute("INSERT INTO userTasks(taskName,task, userOfTasks) VALUES (:taskName, :task, :userOfTasks)",
        {

        'taskName' : editNameEntry.get(),
        'task' : editDiscriptionText.get("1.0",END),
        'userOfTasks' : user_ID

        })
        conn.commit()
        showTasks()
    
#shows you what your selected task has inside
def selectTask():

    conn = sqlite3.connect("Accounts.db")
    c = conn.cursor()

    global selectW
    selectW = True

    global selectedCount
    selectedCount += 1

    deleteeditW()

    #checks if you have already pressed the Show selected task button if you have it deletes the existing labels and entrys... and makes new ones othervice it just creates new ones
    if selectedCount == 1:
        global showDiscription
        showDiscription = Text(taskscreen, width=40, height=20, bg="lightgrey", font=("Helvetica", 18))
        showDiscription.grid(row=3, column=2)

       
        selectedTask1 = UsersListBox.get(ANCHOR)

        c.execute("SELECT taskName FROM userTasks WHERE taskName = ?",(selectedTask1))
        header = c.fetchall()

        c.execute("SELECT Task FROM userTasks WHERE taskName = ?",(selectedTask1))
        discription = c.fetchall()


        showDiscription.insert(1.0,header)
        showDiscription.insert(2.0,"\n")
        showDiscription.insert(3.0,"\n")
        showDiscription.insert(4.0,"Description:\n")
        showDiscription.insert(5.0,"\n")
        showDiscription.insert(6.0,*tuple(*tuple(discription)))
        showDiscription.config(state="disabled")

    else:
        showDiscription.destroy()
        selectedCount = 0
        selectTask()
#checks if you have pressed show selected task button before, and if you have it deletes the labels created from it
def deleteselectW():
    if selectW:
        showDiscription.destroy()
#checks if you have pressed edit selected task button before, and if you have it deletes the labels created from it
def deleteeditW():
    if editW:
        blankCommitLabel.destroy()
        commitButton.destroy()
        editDiscriptionLabel.destroy()
        editDiscriptionText.destroy()
        editNameLabel.destroy()
        editNameEntry.destroy()
#checks if you have pressed show tasks button before, and if you have it deletes the labels created from it
def deletew2():
    if w2:
        editButton.destroy()
        selectButton.destroy()
        deleteButton.destroy()
        myTasksLabel.destroy()
        UsersListBox.destroy()
#checks if you have pressed create new task button before, and if you have it deletes the labels created from it
def deletew1():
    if w1:
        TaskAdviceLabel3.destroy()
        EmptyLabel3.destroy()
        EmptyLabel.destroy()
        EmptyLabel2.destroy()
        TaskAdviceLabel2.destroy()
        TaskAdviceLabel.destroy()
        TaskNameLabel.destroy()
        TaskInfoLabel.destroy()
        taskName.destroy()
        taskInfo.destroy()
        creatingTaskButton.destroy()
#logs closes the TaskList screen and opens main menu        
def logOut():

    global editCount
    editCount = 0
    global selectedCount
    selectedCount = 0
    global w1Count
    w1Count = 0
    global w2Count
    w2Count = 0

    global selectW
    selectW = False
    global editW
    editW = False
    global w1
    w1 = False
    global w2
    w2 = False

    taskscreen.destroy()
    main_screen()
#Main menu
def main_screen():
    global screen
    screen = Tk()
    screen.geometry("300x250")
    screen.title("Projekti")
    Label(text = "Log in", bg= "grey", width = "300", height = "2", font = ("Calibri", 13)).pack()
    Label(text = "").pack()
    Button(text = "Log in", height = "2", width = "30", command = Login).pack()
    Label(text ="").pack()
    Button(text = "Create a new account", height = "2", width = "30", command = Register).pack()
    screen.mainloop()

main_screen()





