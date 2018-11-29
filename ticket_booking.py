import cv2
import os
import numpy as np
import mysql.connector
from tabulate import tabulate
from texttable import Texttable
import datetime
from PIL import Image

# Path for face image database
path = 'dataset'

recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml");


#####
# function to get the images and label data
def getImagesAndLabels(path):

    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
    faceSamples=[]
    ids = []

    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
        img_numpy = np.array(PIL_img,'uint8')

        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_numpy)

        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)

    return faceSamples,ids


########


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="python"
)
mycursor = mydb.cursor()
#def logged(station_id,station_name):
 # print ("welcome",station_name)


def logged(station_id,station_name):
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # set video width
    cam.set(4, 480) # set video height
    while(True):
        

        face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        # For each person, enter one numeric face id
        while True:
            face_name = input('\n Enter Name : ')
            if face_name.isalpha():
                break
            print ("\n[INFO] Please enter valid name")
        print("\n")
        if station_id!=12:
          print("To North :\n")
          mycursor = mydb.cursor()
          sql3 = "SELECT * FROM station where id>=%s"
          station=(station_id,)
          mycursor.execute(sql3,station)
          myresult = mycursor.fetchall()
          #for i in range(a,12):
          for x in myresult:
            #list.append("->")
            print("("+str(x[0])+")" +x[1], end=" -> ")
              #break
          print("**Finished**", end=" ")
          print("\n")
        if station_id!=1:
          print("To South :\n")
          mycursor = mydb.cursor()
          sql3 = "SELECT * FROM station where id<=%s"
          station=(station_id,)
          mycursor.execute(sql3,station)
          myresult = mycursor.fetchall()
          #for i in range(a,12):
          for x in reversed(myresult):
            #list.append("->")
            print("("+str(x[0])+")" +x[1], end=" -> ")
              #break
          print("**Finished**", end=" ")
        while(True):
            to_station = input('\n\nEnter To Station : ')
            if to_station.isdigit()and int(to_station)<=12:
                if int(to_station)==int(station_id):
                    print("\n[INFO] Both Source And Destination Cannot Be Same")
                else:
                    break
            else:
                print("\n[INFO] Please enter valid station id")
                
        mycursor = mydb.cursor()
        dest="SELECT name from station where id=%s"
        de=(to_station,)
        mycursor.execute(dest, de)
        myresult = mycursor.fetchall()
        for xy in myresult:
            to_station_name = xy[0]
        mycursor = mydb.cursor()
        sql = "INSERT INTO customer(name, fromstation,tostation) VALUES (%s, %s, %s)"
        val = (face_name, station_id, to_station)
        mycursor.execute(sql, val)
        mydb.commit()
        #print(mycursor.rowcount, "record inserted.")
        face_id=mycursor.lastrowid
        #a=int(station_id)
        #b=int(to_station)
        no=abs(int(station_id)-int(to_station))
        fare=str(no*10)
        date1=str(datetime.date.today())
        t = Texttable()
        t.add_rows([['WELCOME TO KOCHI METRO \n\n '+station_name+' Station \t'], ['Id: Metro00'+str(face_id)+'\t\tDate : '+date1], ['\nName : '+face_name.capitalize()+'  \n\nTo Station : '+str(to_station_name)+'\n'], ['Total Fare   \t:  '+fare+' Rs' ]])
        print (t.draw())



        print("\n [INFO] Initializing face capture. Look the camera and wait ...")
        # Initialize individual sampling face count
        count = 0

        while(True):

            ret, img = cam.read()
            img = cv2.flip(img, 1) # flip video image vertically
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5)
            
            #while faces:
                #print ("hai")
            #else:
              #  print ("not")

            for (x,y,w,h) in faces:

                cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
                count += 1

                # Save the captured image into the datasets folder
                cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])

                cv2.imshow('image', img)

            k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
            #print(k)
            if k == 27:
                break
            elif count >= 30: # Take 30 face sample and stop video
                 break

        # Do a bit of cleanup
        print("\n [INFO] Image Captured Successfully")
        #cam.release()
        print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
        faces,ids = getImagesAndLabels(path)
        recognizer.train(faces, np.array(ids))

        # Save the model into trainer/trainer.yml
        recognizer.write('trainer/trainer.yml')
        # Print the numer of faces trained and end program
        print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))
        
        exit_key=input("Press Enter to continue or q to loggout...")
        if exit_key=='q':
            print("You have been successfully logged out successfully!")
            cam.release()
            cv2.destroyAllWindows()
            break
        

    
  


print("***********************WELCOME TO KOCHI METRO***********************")
while(True):
    user_name = input('\n Enter user name :  ')
    password = input('\n Enter password :  ')
    sql3 = "SELECT * FROM station WHERE user_name = %s and password=%s"
    login = (user_name,password,)
    mycursor.execute(sql3, login)
    myresult = mycursor.fetchall()
    validate=len(myresult)
    if validate==1:
      for x in myresult:
        station_id=x[0]
        station_name=x[1]
        print ("\n***********************Welcome",station_name,"***********************")
        logged(station_id,station_name)
      break
    else:
      print("\n[INFO] Please enter valid username or password")










