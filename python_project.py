import cv2
from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
import random
from gtts import gTTS   
import time
import vlc
import eyed3
import datetime
import calendar
from datetime import date

def findDay(date):
   born = datetime.datetime.strptime(date, '%d %m %Y').weekday()
   return (calendar.day_name[born])


face_cascade=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap=cv2.VideoCapture(0)

flag = 0
head =0
while True:
    ret,img=cap.read()
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,1.3,5)
    for(x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray=gray[y:y+h,x:x+w]
        roi_color=img[y:y+h,x:x+w]
        if((w*h>0) and (flag == 0)):
            flag = 1
            print("Face detected!")
    
    cv2.imshow('img',img)
    if cv2.waitKey(30) & 0xFF==ord('q'):
        break
        
    if ((flag == 1) and (head == 0)):
        source = requests.get('https://indianexpress.com/latest-news/').text
        soup = BeautifulSoup(source, 'lxml')
        csv_file = open('temp.csv', 'w')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['headline', 'summary', 'Bookmark'])
        
        for article in soup.find_all('div', class_='m-article-landing__inner'):
            headline = article.h3.a.text
            summary = article.p.text
            bookmark = 0 
            csv_writer.writerow([headline, summary, bookmark])
        
        csv_file.close()
        head = 1
        


newsText = 'Good morning! Welcome to Group 14\'s Blind Aid Prototype, Professors' 
myobj = gTTS(text=newsText, lang='en', slow=False)
myobj.save("welcome.mp3")
player = vlc.MediaPlayer("welcome.mp3")
player.play()
duration = eyed3.load('welcome.mp3').info.time_secs
time.sleep(duration)

news = pd.read_csv('temp.csv')
print(news)

Index = news.index
for i in list(Index):
    text = str(news.iloc[i,0])
    print(text)
    
    myobj = gTTS(text=text, lang='en', slow=False)
    f = "news"+str(i)+".mp3"
    myobj.save(f)
    player = vlc.MediaPlayer(f)
    player.play()
    duration = eyed3.load(f).info.time_secs
    time.sleep(duration)
    news.iloc[i,2] = random.randint(0, 1)
    
    
today = date.today()

# dd/mm/YY
d1 = today.strftime("%d %m %Y")
date = d1
print(findDay(date))
if(findDay(date)=='Sunday'):
   news.to_csv("Sunday.csv")
elif findDay(date)=='Monday' :
   news.to_csv("Monday.csv")
elif findDay(date)=='Tuesday' :
   news.to_csv("Tuesday.csv")
elif findDay(date)=='Wednesday' :
   news.to_csv("Wednesday.csv")
elif findDay(date)=='Thursday' :
   news.to_csv("Thursday.csv")
elif findDay(date)=='Friday' :
   news.to_csv("Friday.csv")
elif findDay(date)=='Saturday' :
   news.to_csv("Saturday.csv")

news.to_csv('temp.csv')  # override

dataset = pd.read_csv("temp.csv")
bookmark = dataset.iloc[:, -1]
csv_file = open('bookmark_temp.csv', 'w')
csv_writer = csv.writer(csv_file)
for index in range(0, len(bookmark)):   
    if dataset.iloc[index, 3] == 1:
        csv_writer.writerow([dataset.iloc[index, 1], dataset.iloc[index, 2], dataset.iloc[index, 3]])        
csv_file.close() 


        
        
        
cap.release()
cv2.destroyAllWindows()


     