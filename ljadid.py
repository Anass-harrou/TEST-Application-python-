import time
import cv2
import numpy as np
import face_recognition
from gtts import gTTS
from playsound import playsound
import os
import pymysql
import datetime
from pydub import AudioSegment
from pydub.playback import play
#conn = pymysql.connect(host="localhost", user="root", passwd="", db="python")
x = datetime.datetime.now()
n=x.strftime("%A")
m=x.strftime("%d")
o=x.strftime("%B")
p=n+m+o
#myCursor = conn.cursor()
#myCursor.execute("CREATE TABLE "+p+" (id  int(11) NOT NULL AUTO_INCREMENT primary key,nom varchar(40) NOT NULL,grp varchar(40) NOT NULL,Time time NOT NULL, Time1 time NOT NULL, Seance1 varchar(40) NOT NULL, Seance2 varchar(40) NOT NULL, Seance3 varchar(40) NOT NULL)")
#conn.commit()
path1 = 'ImagesBasic'
##path2 = 'IMAGES'
images = []
classNames = []
myList = os.listdir(path1)
#print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path1}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
    #print(len(classNames))
for x in classNames:
  #print(x)
  azz = x.split(", ")
  aa = azz[0]
  #ba = azz[1]
  #print(aa)
  #print(ba)
  #sql = "INSERT INTO " + p + " (nom, grp, Seance1, Seance2, Seance3) VALUES (%s, %s, 'A', 'A', 'A')"
  #val = [(aa, ba)]
  #myCursor.executemany(sql, val)
  #conn.commit()
  #print(myCursor.rowcount, "was inserted.")
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
encodeListKnown = findEncodings(images)
#print(len(encodeListKnown))
cap= cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,1024)
cap.set(15, 0.1)
while True:
    x = datetime.datetime.now()
    aw = x.strftime("%X")
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        #print(faceDis)
        matchIndex = np.argmin(faceDis)
        if faceDis[matchIndex] < 0.60:
            name = classNames[matchIndex].upper()
            #print(name)
            az = name.split(", ")
            a = az[0]
            #b = az[1]
            #print(a)
            #print(b)
            #sql = "SELECT Time FROM " + p + " WHERE nom = '" + a + "'"
            #myCursor.execute(sql)
            #myResult = myCursor.fetchone()
            #sql1 = "SELECT Time1 FROM " + p + " WHERE nom = '" + a + "'"
            #myCursor.execute(sql)
            #myResult1 = myCursor.fetchone()
            #print(myResult)
            '''if myResult == (datetime.timedelta(0),) and myResult1 == (datetime.timedelta(0),):
                sql = "UPDATE " + p + " SET Time = '" + aw + "' WHERE nom = '" + a + "'"
                myCursor.execute(sql)
                conn.commit()
            elif myResult1 == (datetime.timedelta(0),) and myResult != (datetime.timedelta(0),):
                sql = "UPDATE " + p + " SET Time1 = '" + aw + "' WHERE nom = '" + a + "'"
                myCursor.execute(sql)
                conn.commit()'''
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            res = gTTS(text ='merci'+a, lang='it')
            res.save("audio.mp3")
            song = AudioSegment.from_mp3("audio.mp3")
            play(song)
        else:
            name = 'Unknown'
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            res = gTTS(text='inconnue', lang='fr')
            res.save("audio.mp3")
            song = AudioSegment.from_mp3("audio.mp3")
            play(song)
    cv2.imshow('Result', img)
    cv2.waitKey(1)
