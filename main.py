##!/usr/bin/env python
import config
import utility
import socket
import time
import re
import robot
import cv2

CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
objectives = {
"PUT BULL SPREAD": False,
"CRAPPY MERCY": False,
"JUST A DONUT": False,
"CHEETOH": False,
"NECK BRO": False,
"FREEDOM SEAGULL": False,
}

cap=cv2.VideoCapture(2)
detector=cv2.QRCodeDetector()

print("Started QR Scanner")

try:
    s = socket.socket()
    s.connect((config.HOST, config.PORT))
    s.send("PASS {}\r\n".format(config.PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(config.NICK).encode("utf-8"))
    s.send("JOIN {}\r\n".format(config.CHAN).encode("utf-8"))
    connected = True #Socket succefully connected
except Exception as e:
    print(str(e))
    connected = False #Socket failed to connect

def bot_loop():
    try:
        robot.init()
        while connected:
            response = s.recv(1024).decode("utf-8")
            if response == "PING :tmi.twitch.tv\r\n":
                s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
                print("Pong")
            else:
                username = re.search(r"\w+", response).group(0)
                message = CHAT_MSG.sub("", response)
                if re.match(r'^\!robot pepeD', message):
                    newMessage = '>><<>><<^v'
                    for char in newMessage:
                        robot.move(char)
                        time.sleep(.1)
                    qrRead()
                elif re.match(r'^\!robot catDance', message):
                    newMessage = '^<>v<>^<>'
                    for char in newMessage:
                        robot.move(char)
                        time.sleep(.1)
                    qrRead()
                elif re.match(r'\!robot scan', message):
                    qrRead()
                elif username == 'ayejay18' and re.match(r'\!robot reset', message):
                    resetObj()
                elif re.match(r'\!robot status', message):
                    statusMessage = status()
                    utility.chat(s,statusMessage)
                elif re.match(r'\!robot ', message):
                    newMessage = message.strip('!robot ')[0:5]
                    for char in newMessage:
                        if char in ['^','v','<','>']:
                            robot.move(char)
                            time.sleep(.1)
                    qrRead()
                            #time.sleep(.1)
                #time.sleep(1 / config.RATE)
    finally:
        robot.cleanup()
        print("GPIO Cleanup")

def resetObj():
    global objectives
    for x in objectives:
        objectives[x] = False

def status():
    global objectives
    message = ""
    foundNum = 0
    for x in objectives.values():
        if x == True:
           foundNum += 1
    message += "Found " + str(foundNum) + " of 6 items: ("
    for x,y in objectives.items():
        if y and foundNum > 1:
            message += x + ", "
            foundNum -= 1
        elif y and foundNum == 1:
            message += x
    message += ")"
    return message

def qrRead():
    global objectives
    print("scanning")
    _, img = cap.read()
    for x in range(25):
        _, img = cap.read()
        data, bbox, _ = detector.detectAndDecode(img)
        if(bbox is not None):
            if data:
                for x in objectives:
                    if data == x and not objectives[x]:
                        objectives[x] = True
                        print("Found ", data)
                        message = "You Found " + data
                        utility.chat(s,message)

if __name__ == "__main__":
    bot_loop()

