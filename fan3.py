#!/usr/bin/env python3
# Romeo St-Cyr 2023
import os
import time
from time import sleep
import signal
import sys
import RPi.GPIO as GPIO


fanPin = 14 

desiredTemp = 50 

fanSpeed=100
sum=0
pTemp=15
iTemp=0.4

def Shutdown():  
    fanOFF()
    sleep(100)

def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    temp =(res.replace("temp=","").replace("'C\n",""))
    #print("temp is {0}".format(temp)) #Decommenter pour tester
    return temp
def fanOFF():
    myPWM.ChangeDutyCycle(0)   # Arreter le ventilateur
    return()
def handleFan():
    global fanSpeed,sum
    actualTemp = float(getCPUtemperature())
    diff=actualTemp-desiredTemp
    sum=sum+diff
    pDiff=diff*pTemp
    iDiff=sum*iTemp
    fanSpeed=pDiff +iDiff
    if fanSpeed>100:
        fanSpeed=100
    if fanSpeed<15:
        fanSpeed=0
    if sum>100:
        sum=100
    if sum<-100:
        sum=-100
    #print("actualTemp %4.2f TempDiff %4.2f pDiff %4.2f iDiff %4.2f fanSpeed %5d" % (actualTemp,diff,pDiff,iDiff,fanSpeed))
    myPWM.ChangeDutyCycle(fanSpeed)
    return()
def setPin(mode): 
    GPIO.output(fanPin, mode)
    return()
try:
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(fanPin, GPIO.OUT)
    myPWM=GPIO.PWM(fanPin,50)
    myPWM.start(50)
    GPIO.setwarnings(False)
    fanOFF()
    while True:
        handleFan()
        sleep(1)  
except KeyboardInterrupt: 
    fanOFF()
    GPIO.cleanup() 
