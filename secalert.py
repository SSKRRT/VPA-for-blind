import urllib2
import cookielib
from getpass import getpass
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from smtplib import SMTP
import smtplib
import sys
from stat import *
import os
import time
import RPi.GPIO as GPIO       ## Import GPIO library
GPIO.setmode(GPIO.BOARD)      ## Use board pin numbering
GPIO.setup(13, GPIO.IN)
i=0
import Adafruit_DHT


def tempr():
        sensor = 11
        pin = 4
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        if humidity is not None and temperature is not None:
            print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
        else:
            print('Failed to get reading. Try again!')
        return temperature

def mail():
        recipients = ['kiranrodge21@gmail.com']
        emaillist = [elem.strip().split(',') for elem in recipients]
        msg = MIMEMultipart()
        msg['Subject'] = "ALERT MESSAGE"
        msg['From'] = 'sskrrt21@gmail.com'
        msg['Reply-to'] = 'sskrrt21@gmail.com'
        msg.preamble = 'Multipart massage.\n'
        part = MIMEText("Hi, please find the attached file")
        msg.attach(part)
        fp=open("img.jpg","rb")
        img=MIMEImage(fp.read())
        #part = MIMEApplication(img,"rb")
        #part.add_header('Content-Disposition', 'attachment', filename="test.jpg")
        msg.attach(img)
        server = smtplib.SMTP("smtp.gmail.com:587")
        server.ehlo()
        server.starttls()
        server.login("sskrrt21@gmail.com", "ruchi12!")
        server.sendmail(msg['From'], emaillist , msg.as_string())
        print "mail sent"
        return


def smoke(sk):
        if sk==1:
                temperature=tempr()
                if temperature>20:
                        print "fire"
                        os.system("fswebcam img.jpg")
                        mail()
                time.sleep(1)
                print " smoke detected"
                #return "image captured"
        else:
                print " no smoke detected"
                #return "no image"

while True:
        i=i+1
        time.sleep(1)
        sm=GPIO.input(13)
        smoke(sm)
        time.sleep(1)
        
        

