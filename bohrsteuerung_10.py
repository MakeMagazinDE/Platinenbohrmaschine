#!/usr/bin/python3
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk
import serial
import os
import RPi.GPIO as GPIO

name = "Bohrsteuerung V08"
filename = 'bohrconf.txt'
rpm = 0

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(18, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(27, GPIO.OUT)
GPIO.output(27, GPIO.HIGH)

mainWin=Tk()
mainWin.geometry('154x420+640+27')
mainWin.resizable(width=FALSE, height=FALSE)
mainWin.title(name)
mainFrame = Frame(master=mainWin)
mainFrame.place(x=0, y=0, width=154, height=420)
outFrame = Frame(master=mainFrame)
outFrame.place(x=0, y=280, width=154, height=140)

try:
    ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=0.1)
except ValueError:
    tkMessageBox.showinfo("Fehler", "ttyAMA0")
        
ser.flushInput()
ser.flushOutput()
sertextsend = StringVar()
sertextrec = StringVar()

bg = StringVar()
ba = StringVar()
wp = StringVar()
bt = StringVar()
wl = StringVar()
hp = StringVar()
su = StringVar()
ss = StringVar()
pw = StringVar()

def BHome():
    ser.write("\x00".encode())
    
def BRef():
    ser.write("\x01".encode())
    button2.config(bg='light green')
    
def BWkz():
    ser.write("\x02".encode())
    
def BStart():
    ser.write("\x03".encode())
    
def BWl():
    ser.write("\x04".encode())

def BRpm0():
    ser.write("\x05".encode())
    button6.config(bg='red')
    button7.config(bg='light grey')
    button8.config(bg='light grey')
    button9.config(bg='light grey')
    button10.config(bg='light grey')
    
def BRpm25():
    ser.write("\x06".encode())
    button7.config(bg='red')
    button6.config(bg='light grey')
    button8.config(bg='light grey')
    button9.config(bg='light grey')
    button10.config(bg='light grey')
    
def BRpm50():
    ser.write("\x07".encode())
    button8.config(bg='red')
    button6.config(bg='light grey')
    button7.config(bg='light grey')
    button9.config(bg='light grey')
    button10.config(bg='light grey')
    
def BRpm75():
    ser.write("\x08".encode())
    button9.config(bg='red')
    button6.config(bg='light grey')
    button7.config(bg='light grey')
    button8.config(bg='light grey')
    button10.config(bg='light grey')
    
def BRpm100():
    ser.write("\x09".encode())
    button10.config(bg='red')
    button6.config(bg='light grey')
    button7.config(bg='light grey')
    button8.config(bg='light grey')
    button9.config(bg='light grey')

def shutdown():
    GPIO.cleanup()
    print('os: shutdown -h now')
    os.system("sudo shutdown -h now")
    
def config():
    os.system("./bohrconfig.py")
    
def doReturn():
    print('Return gedrueckt')

def callback():
    ser.close()
    fenster.destroy()
    fenster.protocol("WM_DELETE_WINDOW", callback)

def send(*args):
   ser.write(sertextsend.get().encode())
   
def receive():
   if (ser.inWaiting() != 0):
       sertextrec = ser.read(10).decode()
       text=sertextrec
       ausgabetext1.insert('1.0', text)
       
   mainWin.after(10,receive)

def check_button():
    if(GPIO.input(17) == GPIO.LOW):
        BStart()
    if(GPIO.input(18) == GPIO.LOW):
        shutdown()
    mainWin.after(250,check_button)

try:
        f = open(filename)
except IOError:
    tkMessageBox.showinfo("Fehler", "config.txt fehlt")

for line in f:
#    line = line.rstrip('\n')
    ser.write(line.encode())
f.close 

image1=PhotoImage(file='ico/home.png')
button1 = Button(master=mainFrame,image=image1, command=BHome)
button1.place(x=1, y=5, width=50, height=50)

image2=PhotoImage(file='ico/ref.png')
button2 = Button(master=mainFrame,image=image2, command=BRef)
button2.place(x=1, y=60, width=50, height=50)

image3=PhotoImage(file='ico/wkz.png')
button3 = Button(master=mainFrame,image=image3, command=BWkz)
button3.place(x=1, y=115, width=50, height=50)

image4=PhotoImage(file='ico/start.png')
button4 = Button(master=mainFrame,image=image4, command=BStart)
button4.place(x=1, y=170, width=50, height=50)

image5=PhotoImage(file='ico/wl.png')
button5 = Button(master=mainFrame,image=image5, command=BWl)
button5.place(x=1, y=225, width=50, height=50)

image6=PhotoImage(file='ico/rpm0.png')
button6 = Button(master=mainFrame,image=image6, command=BRpm0)
button6.place(x=52, y=5, width=50, height=50)

image7=PhotoImage(file='ico/rpm25.png')
button7 = Button(master=mainFrame,image=image7, command=BRpm25)
button7.place(x=52, y=60, width=50, height=50)

image8=PhotoImage(file='ico/rpm50.png')
button8 = Button(master=mainFrame,image=image8, command=BRpm50)
button8.place(x=52, y=115, width=50, height=50)

image9=PhotoImage(file='ico/rpm75.png')
button9 = Button(master=mainFrame,image=image9, command=BRpm75)
button9.place(x=52, y=170, width=50, height=50)

image10=PhotoImage(file='ico/rpm100.png')
button10 = Button(master=mainFrame,image=image10, command=BRpm100)
button10.place(x=52, y=225, width=50, height=50)

image11=PhotoImage(file='ico/conf.png')
button11 = Button(master=mainFrame,image=image11, command=config)
button11.place(x=103, y=5, width=50, height=50)

image12=PhotoImage(file='ico/shut.png')
button12 = Button(master=mainFrame,image=image12, command=shutdown)
button12.place(x=103, y=60, width=50, height=50)

scrollbar1 = Scrollbar(outFrame)
ausgabetext1 = Text(outFrame, height=6, width=19)
scrollbar1.pack(side=RIGHT, fill=Y)
ausgabetext1.pack(side=LEFT, fill=Y)
scrollbar1.config(command=ausgabetext1.yview)
ausgabetext1.config(yscrollcommand=scrollbar1.set)

mainWin.after(500,check_button)
mainWin.after(10,receive)
mainWin.mainloop()

