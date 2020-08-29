#!/usr/bin/env python
import config
import utility
import socket
import time
import re
import robot

CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

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
                                print(username + ": " + response)
                                if re.match(r'\!robot \^', message):
                                        #utility.chat(s,"Bot Forward")
                                        robot.move('^')
                                elif re.match(r'\!robot \<', message):
                                        #utility.chat(s,"Bot Left")
                                        robot.move('<')
                                elif re.match(r'\!robot \>', message):
                                        #utility.chat(s,"Bot Right")
                                        robot.move('>')
                                elif re.match(r'\!robot v', message):
                                        #utility.chat(s,"Bot Backward")
                                        robot.move('v')
                                elif re.match(r'\!robot 360', message):
                                        robot.move('>')
                                        robot.move('>')
                                        robot.move('>')
                                        robot.move('>')
                                        robot.move('>')
                                        robot.move('>')
                                        robot.move('>')
                                        robot.move('>')
                                elif re.match(r'\!robot 180', message):
                                        robot.move('<')
                                        robot.move('<')
                                        robot.move('<')
                                        robot.move('<')
                time.sleep(1 / config.RATE)
        finally:
                robot.cleanup()
                print("GPIO Cleanup")
if __name__ == "__main__":
        bot_loop()

