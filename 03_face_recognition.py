import cv2
import numpy as np
import os
import mysql.connector
import datetime
import time

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="python"
)

mycursor = mydb.cursor()


def logged(station_id,station_name):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml')
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath);

    font = cv2.FONT_HERSHEY_SIMPLEX

    #iniciate id counter
    id = 0
    #mycursor.execute("SELECT id, name FROM test")
    #names = ['x']
    #myresult = mycursor.fetchall()

    #for x in myresult:
      #print(x)
     # names.append(x)

    # names related to ids: example ==> Marcelo: id=1,  etc
    #names = ['None', 'Sayeed', 'suthi', 'amru', 'anil', 'manisha','tree'] 

    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # set video widht
    cam.set(4, 480) # set video height

    # Define min window size to be recognized as a face
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)
       

    while True:

        ret, img =cam.read()
        border_color=(0,0,255)#bgr
        disp_status='Please Contact Administrative'
        img = cv2.flip(img, 1) # Flip vertically
        cv2.rectangle(img,(0,0),(640,60),(0,255,255),3)
        cv2.putText(img,'Welcome To '+station_name+' Station',(5,45), font, 1,(255,255,255),2,cv2.LINE_AA)
     

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale( 
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
           )
        #print(len(faces))
        #if len(faces)!=0:
         #       disp_status='###########################'
        #else:
         #       disp_status='@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'

        for(x,y,w,h) in faces:
            #cv2.putText(img,'Welcome To '+station_name+' Station',(5,45), font, 1,(255,255,255),2,cv2.LINE_AA)

            #cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
            ids="unknown"

            # Check if confidence is less them 100 ==> "0" is perfect match 
            if (confidence > 30):
                sql2 = "SELECT name, status FROM customer WHERE id = %s and fromstation=%s and (status=%s or status=%s )"
                adr = (id,station_id,0,1 )
                mycursor.execute(sql2, adr)
                myresult = mycursor.fetchall()
                for xy in myresult:
                  ids = xy[0]
                  status=xy[1]
                  if status==0:
                    disp_status="Success:Ticket activated"
                    border_color=(0,255,0)
                  else:
                    disp_status="Your time stamp already started"
                    border_color=(0,255,255)
                cv2.rectangle(img,(20,420),(620,639),border_color,3)
                cv2.putText(img,disp_status,(30,460), font, 1,border_color,2,cv2.LINE_AA)
     
                #time.sleep( 5 )
                #if status==0:
                 #   t = Timer(30.0, hello)
                  #  t.start()
                  
                confidence = "  {0}%".format(round(100 - confidence))
            else:
                ids = "unknown"
                border_color=(0,0,255)
                disp_status='Please Contact Administrative'
                confidence = "  {0}%".format(round(100 - confidence))
                cv2.rectangle(img,(20,420),(620,639),border_color,3)
                cv2.putText(img,disp_status,(30,460), font, 1,border_color,2,cv2.LINE_AA)
     
            cv2.rectangle(img, (x,y), (x+w,y+h), border_color, 2)
            cv2.putText(img, str(ids), (x+5,y-5), font, 1, (255,255,255), 2)
            cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
        #cv2.namedWindow('Entry Level', cv2.WND_PROP_FULLSCREEN)
        #cv2.setWindowProperty('Entry Level', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        #else:
            #cv2.putText(img,'Welcome To '+station_name+' Station',(5,45), font, 1,(255,255,255),2,cv2.LINE_AA)
        cv2.imshow('camera',img) 

        k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            #code in entry point
            if status==0:
                date3=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            #print (date3)
                sql3 = "UPDATE customer SET status = '1', date=%s WHERE id = %s"
                stat = (date3,id, )
                mycursor.execute(sql3,stat)
                mydb.commit()
        
        
    print("\n [INFO] Exiting Program and cleanup stuff")    
    cam.release()
    cv2.destroyAllWindows()
        




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











