# import GPIO and time
import RPi.GPIO as GPIO
import time

interval = .4
turninterval = .2

rightforward = 24
rightback = 23
leftforward = 22
leftback = 17

def init():
    #set GPIO numbering mode and define output pins
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(rightforward,GPIO.OUT)
    GPIO.setup(rightback,GPIO.OUT)
    GPIO.setup(leftforward,GPIO.OUT)
    GPIO.setup(leftback,GPIO.OUT)

def move(direction):
    if direction == '^':
        print("Forward")
        GPIO.output(rightforward,True)
        GPIO.output(leftforward,True)
        GPIO.output(rightback,False)
        GPIO.output(leftback,False)
        time.sleep(interval)
        GPIO.output(rightforward,False)
        GPIO.output(leftforward,False)
        GPIO.output(rightback,False)
        GPIO.output(leftback,False)
    elif direction == 'v':
        print("Back")
        GPIO.output(rightforward,False)
        GPIO.output(leftforward,False)
        GPIO.output(rightback,True)
        GPIO.output(leftback,True)
        time.sleep(interval)
        GPIO.output(rightforward,False)
        GPIO.output(leftforward,False)
        GPIO.output(rightback,False)
        GPIO.output(leftback,False)
    elif direction == '<':
        GPIO.output(rightforward,True)
        GPIO.output(leftforward,False)
        GPIO.output(rightback,False)
        GPIO.output(leftback,True)
        time.sleep(turninterval)
        GPIO.output(rightforward,False)
        GPIO.output(leftforward,False)
        GPIO.output(rightback,False)
        GPIO.output(leftback,False)
    elif direction == '>':
        GPIO.output(rightforward,False)
        GPIO.output(leftforward,True)
        GPIO.output(rightback,True)
        GPIO.output(leftback,False)
        time.sleep(turninterval)
        GPIO.output(rightforward,False)
        GPIO.output(leftforward,False)
        GPIO.output(rightback,False)
        GPIO.output(leftback,False)

def cleanup():
    GPIO.cleanup()


