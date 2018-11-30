#!C:\Users\THOMAS\AppData\Local\Programs\Python\Python36-32\python.exe

from tkinter import *
import tkinter as tk
import tkinter.messagebox as tm
import pymysql

page2 = Tk() # Opens new window
page2.title('Ticket VIew')
page2.geometry('950x650')
page2.configure(background="light blue")
page2.grid_rowconfigure(0, weight=1)
page2.grid_columnconfigure(0, weight=1)

lbl= tk.Label(page2, text="UserId",width=10  ,height=1  ,fg="white"  ,bg="grey" ,font=('times', 15, ' bold ') )
lbl.place(x=50, y=100)

textbox = tk.Entry(page2,width=20  ,bg="white" ,fg="green",font=('times', 15))
textbox.place(x=180, y=100)
lb2= tk.Label(page2, text="",width=50  ,height=3  ,fg="white"  ,bg="light blue" ,font=('times', 15, ' bold ') )
lb2.place(x=50, y=250)


def ticketview():
    mydb = pymysql.connect("localhost","root","","python")
    mycursor = mydb.cursor()

    userid = int(textbox.get())
    print(userid)
    mycursor.execute("SELECT * FROM customer WHERE ID = %d" %(userid))
    myresult = mycursor.fetchall()
    print(myresult)
    lb2.configure(text= myresult)
    mydb.close()

takedata = tk.Button(page2, text="Submit", command=ticketview ,fg="white"  ,bg="grey"  ,width=10  ,height=1, activebackground = "yellow" ,font=('times', 15, ' bold '))
takedata.place(x=50, y=150)
page2.mainloop()
