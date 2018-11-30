from tkinter import *
import tkinter as tk
import tkinter.messagebox as tm
import mysql.connector
import os

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="python"
)
mycursor = mydb.cursor()


class LoginFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.label_username = Label(self, text="Username")
        self.label_password = Label(self, text="Password")

        self.entry_username = Entry(self)
        self.entry_password = Entry(self, show="*")

        self.label_username.grid(row=0, sticky=E)
        self.label_password.grid(row=1, sticky=E)
        self.entry_username.grid(row=0, column=1)
        self.entry_password.grid(row=1, column=1)

        self.checkbox = Checkbutton(self, text="Keep me logged in")
        self.checkbox.grid(columnspan=2)

        self.logbtn = Button(self, text="Login", command=self._login_btn_clicked)
        self.logbtn.grid(columnspan=2)
        

        self.pack()
    def page1(self):
        #page2text.pack_forget()
        #page1text.pack()
        
        #page1 = Tk() # Opens new window
        #page1.title('Ticket Cancel')
        #.geometry('1050x650')
        os.system("ticket_cancel.py")

    def page2(self):
        '''page2 = Tk() # Opens new window
        page2.title('Ticket VIew')
        page2.geometry('950x650')

        label_head = Label(page2, text="Welcome")
        label_userid = Label(page2, text="Enter the User id")   
        entry_userid = Entry(page2)
        
        label_userid.grid(row=1, sticky=E)
        entry_userid.grid(row=1, column=1)
        label_head.grid(row=0,column=5)
        logbtn = Button(page2, text="Submit", command=self.ticketview)
        logbtn.grid(columnspan=2)
        #label_userid.pack()
        #entry_userid.pack()
        #logbtn.pack(side="left")'''
        os.system("ticketsview.py")

    def ticketview(self):
        #ticketview = Tk()
        userid = self.entry_userid.get()
        print(userid)
        query = "SELECT * FROM customer WHERE ID = %s"
        uid = (userid,)
        mycursor.execute(query, uid)
        myresult = mycursor.fetchall()
        print(myresult)
        #ticketview.mainloop()
                
    def page3(self):
        os.system("ticket_cancel.py")


    def _login_btn_clicked(self):
        # print("Clicked")
        username = self.entry_username.get()
        password = self.entry_password.get()
        # print(username, password)
        sql3 = "SELECT * FROM station WHERE user_name = %s and password=%s"
        #p1 = Page1(self)
        login = (username,password,)
        mycursor.execute(sql3, login)
        myresult = mycursor.fetchall()
        validate=len(myresult)
        if validate==1:
            for x in myresult:
                station_id=x[0]
                station_name=x[1]
            r = Tk() # Opens new window
            r.title(station_name+ 'Station')
            r.geometry('1050x650') # Makes the window a certain size
            rlbl = Label(r, text='\n Welcome '+station_name+' Station') # "logged in" label
            page1btn = Button(r, text="Ticket Cancellation", command=self.page1)
            page2btn = Button(r, text="Ticket View", command=self.page2)
            page3btn = Button(r, text="Fine Calculation", command=self.page3)
            #page4btn = Button(r, text="Ticket View", command=self.page4)
            page1btn.pack(side="left")
            page2btn.pack(side="left")
            page3btn.pack(side="left")
            #page4btn.pack(side="left")
            rlbl.pack() # Pack is like .grid(), just different
            r.mainloop()
        else:
            tm.showerror("Login error", "Incorrect username")


root = Tk()
lf = LoginFrame(root)
root.mainloop()
