from tkinter import *
import tkinter as tk
import tkinter.messagebox as tm
import mysql.connector

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
        self.logbtn = Button(self, text="Deactivate Ticket", command=self._deactivate_ticket)
        self.logbtn.grid(columnspan=2)
        self.pack()

    def _deactivate_ticket(self):
        userid = self.entry_userid.get()
        sql3 = "SELECT * FROM customer WHERE id=%s"
        uid = (userid,)
        mycursor.execute(sql3, uid)
        myresult = mycursor.fetchall()
        validate=len(myresult)
        if validate==1:
            cancel = (userid,)
            sql4 = "SELECT status FROM customer WHERE id=%s"
            mycursor.execute(sql4, cancel)
            myresult = mycursor.fetchall()
            for x in myresult:
                curr_status=x[0]
            if (curr_status==0):
                sql5 = "UPDATE customer SET status=2 WHERE id=%s"
                mycursor.execute(sql5, cancel)
                mydb.commit()
                tm.showinfo("Information","Ticket Deactivation Successfull")
               # r = Tk() # Opens new window
                #r.title(':D')
                #r.geometry('350x350') # Makes the window a certain size
                #rlbl = Label(r, text='\nTicket Deactivation Successfull') # "logged in" label
                #rlbl.pack() # Pack is like .grid(), just different
                #r.mainloop()
            else:
                tm.showwarning("Warning","Ticket is used!!! Cannot be deactivated")
        else:
            tm.showerror("Error","Please enter valid user id")
    

root = Tk()
lf = LoginFrame(root)
root.mainloop()
root.wm_geometry("1000x1000")
page1btn.pack()
page2btn.pack()

