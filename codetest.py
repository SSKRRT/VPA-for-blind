# -*- coding: utf-8 -*-
import speech_recognition as sr
import time
import pyttsx
import requests
import RPi.GPIO as GPIO
import os
import sys
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
                                       
GPIO.setup(22, GPIO.OUT)

engine = pyttsx.init()
engine.setProperty('rate', 150)
r = sr.Recognizer()

def weather_data(query):
	res=requests.get('http://api.openweathermap.org/data/2.5/weather?'+query+'&APPID=b35975e18dc93725acb092f7272cc6b8&units=metric');
	return res.json();
def print_weather(result,city):
        print("{}'s temperature: {}°C ".format(city,result['main']['temp']))
        temp="{}".format(result['main']['temp'])
        print("Wind speed: {} m/s".format(result['wind']['speed']))
        wind="{}".format(result['wind']['speed'])
        print("Description: {}".format(result['weather'][0]['description']))
        desc="{}".format(result['weather'][0]['description'])
        print("Weather: {}".format(result['weather'][0]['main']))
        weath="{}".format(result['weather'][0]['main'])
        #print temp,wind,desc,weath
        engine.say("temperature is %s celcius, wind speed is %s miles per second, sky is %s, overall weather is %s"%(temp,wind,desc,weath))
        engine.runAndWait()
        
while(1):
    with sr.Microphone() as source:                                            
        print("Speak:")
        time.sleep(1)
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        speechString =r.recognize_google(audio)
        print "",speechString
        
        if speechString=="light on":
            engine.say("Yess I am turning on light")
            engine.runAndWait()
            print "turning on light"
            GPIO.output(22,GPIO.HIGH)
        if speechString=="light off":
            engine.say("Yess I am turning off light")
            engine.runAndWait()
            print "turning off light"
            GPIO.output(22,GPIO.LOW)
        if speechString=="weather":
            engine.say("heres the weather report")
            engine.runAndWait()
            city="Pune"#raw_input('Enter the city:')
            print()
            try:
              query='q='+city;
              w_data=weather_data(query);
              print_weather(w_data, city)
              print()
            except:
              print('City name not found...')
              
        if speechString=="start security system":
            engine.say("Alright,Starting security system")
            engine.runAndWait()
            os.system("python secalert.py")
            
            
        if speechString=="thank you":
            print "Goodbye!"
            engine.say("Goodbye")
            engine.runAndWait()
            break
        
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    
