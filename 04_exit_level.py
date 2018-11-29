import cv2
import numpy as np
import os
import mysql.connector
import datetime as datetime1
from time import gmtime, strftime
from datetime import datetime
import time as time1

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
        img = cv2.flip(img, 1) # Flip vertically
        border_color=(0,0,255)
        disp_status='Please Contact Administrative'
        cv2.rectangle(img,(0,0),(640,60),(0,255,255),3)
        cv2.putText(img,'Welcome To '+station_name+' Station',(5,45), font, 1,(255,255,255),2,cv2.LINE_AA)
     


        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale( 
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
           )

        for(x,y,w,h) in faces:

            

            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
            ids="unknown"

            # Check if confidence is less them 100 ==> "0" is perfect match 
            if (confidence < 100):
                sql2 = "SELECT name, status,date,fromstation,tostation FROM customer WHERE id = %s and status=%s "
                adr = (id,'1', )
                mycursor.execute(sql2, adr)
                myresult = mycursor.fetchall()
                for xy in myresult:
                  ids = xy[0]
                  status=xy[1]
                  time=xy[2]
                  source=xy[3]
                  destination=xy[4]
                  FMT = '%Y-%m-%d %H:%M:%S'
                  timenow=datetime1.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                  #print(timenow)
                  elapsed = datetime.strptime(str(timenow), FMT) - datetime.strptime(str(time), FMT)
                  MMT = '%H:%M:%S'
                  atime=datetime.strptime(str(elapsed), MMT)
                  diff=(atime.hour*3600)+(atime.minute*60)+atime.second
                  if station_id!=source:
                          if station_id==destination:
                              if diff<3600:
                                #stat = "You have reached your destination"
                                disp_status="You reached destination"
                                border_color=(0,255,0)
                                k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
                                if k == 27:
                                    #code in entry point
                                    if status==1:
                                        sql3 = "UPDATE customer SET status = '2' WHERE id = %s"
                                        stat = (id, )
                                        mycursor.execute(sql3,stat)
                                        mydb.commit()
                              else:
                                  border_color=(0,0,255)
                                  disp_status="Your time period experied. Contact admin"
                              #print(stat)
                          elif source>destination:
                                r=range(destination,source)
                                stat=station_id in r
                                if stat==True:
                                    if diff<3600:
                                     disp_status="You are existing from middle station"
                                     border_color=(0,255,255)
                                     #print("success")
                                     k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
                                     if k == 27:
                                        #code in entry point
                                        if status==1:
                                            sql3 = "UPDATE customer SET status = '2' WHERE id = %s"
                                            stat = (id, )
                                            mycursor.execute(sql3,stat)
                                            mydb.commit()
                                    else:
                                        border_color=(0,0,255)
                                        disp_status="Your time period experied. Contact admin"
                                        #print("Your time period experied. Contact admin")
                                else:
                                    border_color=(0,0,255)
                                    disp_status="You are at worng station"
                                    #Print("You are at wrong destination")
                                    
                          else:
                                r=range(source,destination)
                                stat=station_id in r
                                if stat==True:
                                    if diff<3600:
                                     disp_status="You are existing from middle station"
                                     border_color=(0,255,255)
                                     #print("Success")
                                     k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
                                     if k == 27:
                                        #code in entry point
                                        if status==1:
                                            sql3 = "UPDATE customer SET status = '2' WHERE id = %s"
                                            stat = (id, )
                                            mycursor.execute(sql3,stat)
                                            mydb.commit()
                                    else:
                                        border_color=(0,0,255)
                                        disp_status="Your time period experied. Contact admin"
                                        #print("Your time period experied. Contact admin")
                                else:
                                    border_color=(0,0,255)
                                    disp_status="You are at wrong destination"
                                    #print("You are at wrong destination")
                                    
                     
                  else:
                      if diff<3600:
                        if diff<1800:
                            border_color=(0,255,255)
                            disp_status="Same station: enter within 10 minut"
                            #print("you existed")
                        else:
                            disp_status="Existing from same station"
                            border_color=(0,255,255)
                            k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
                            if k == 27:
                                            #code in entry point
                                        if status==1:
                                            sql3 = "UPDATE customer SET status = '2' WHERE id = %s"
                                            stat = (id, )
                                            mycursor.execute(sql3,stat)
                                            mydb.commit()
                      else:
                          border_color=(0,0,255)
                          disp_status="Your time period experied. Contact admin"
                        #print("you are at same station")
                        
                  
                  #print("difference"+str(diff))
                #print(elapsed)

                #timenow = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                #time='2018-10-25 11:43:26'
                    
                
                #print(time)
                    
                
                confidence = "  {0}%".format(round(100 - confidence))
            else:
                ids = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))
            cv2.rectangle(img, (x,y), (x+w,y+h), border_color, 2)
            cv2.putText(img, str(ids), (x+5,y-5), font, 1, (255,255,255), 2)
            cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)
            #font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.rectangle(img,(20,420),(620,639),border_color,3)
            cv2.putText(img,disp_status,(30,460), font, 1,border_color,2,cv2.LINE_AA)
        
        cv2.imshow('Exit Level',img) 

        k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            #code in entry point
            if status==1:
                sql3 = "UPDATE customer SET status = '2' WHERE id = %s"
                stat = (id, )
                mycursor.execute(sql3,stat)
                mydb.commit()

    # Do a bit of cleanup
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






