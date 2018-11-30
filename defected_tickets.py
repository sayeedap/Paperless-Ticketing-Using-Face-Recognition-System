from tkinter import *
import tkinter as tk
import tkinter.messagebox as tm
import mysql.connector
import datetime as datetime1
from time import gmtime, strftime
from datetime import datetime
import time as time1
import math


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

        self.label_userid = Label(self, text="Enter user id")
        self.entry_userid = Entry(self)
        self.label_userid.grid(row=0, sticky=E)
        self.entry_userid.grid(row=0, column=1)
        self.logbtn = Button(self, text="Calculate Fine", command=self._calc_fine)
        self.logbtn.grid(columnspan=2)
        self.pack()

    def _calc_fine(self):
        userid = self.entry_userid.get()
        sql3 = "SELECT * FROM customer WHERE id=%s"
        uid = (userid,)
        mycursor.execute(sql3, uid)
        myresult = mycursor.fetchall()
        validate=len(myresult)
        if validate==1:
            uid = (userid,)
            sql4 = "SELECT date FROM customer WHERE id=%s"
            mycursor.execute(sql4, uid)
            myresult = mycursor.fetchall()
            for x in myresult:
                ticket_time=x[0]
            #current_time = datetime.datetime.now()
            #diff=current_time-ticket_time
            amt=50
            

            FMT = '%Y-%m-%d %H:%M:%S'
            timenow=datetime1.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            #print(timenow)
            elapsed = datetime.strptime(str(timenow), FMT) - datetime.strptime(str(ticket_time), FMT)
            MMT = '%H:%M:%S'
            atime=datetime.strptime(str(elapsed), MMT)
            diff=(atime.hour*3600)+(atime.minute*60)+atime.second
            if (diff>=3600):
                amt = amt + (diff-3600)*0.013889
                #sql5 = "UPDATE customer SET fine=amt WHERE id=%s"
                #mycursor.execute(sql5, uid)
                #mydb.commit()
            tm.showinfo("Fine Amount",math.floor(amt))
        else:
            tm.showerror("Error","Please enter valid user id")
    

root = Tk()
lf = LoginFrame(root)
root.mainloop()
root.wm_geometry("1000x1000")
page1btn.pack()
page2btn.pack()

