#!/usr/bin/python3
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk

name = "Bohrconfig V01"
filename = 'bohrconf.txt'

mainWin=Tk()
mainWin.geometry('310x330+50+30')
mainWin.resizable(width=FALSE, height=FALSE)
mainWin.title(name)
mainFrame = Frame(master=mainWin)
mainFrame.place(x=0, y=0, width=310, height=330)

bg = StringVar()
ba = StringVar()
wp = StringVar()
bt = StringVar()
wl = StringVar()
hp = StringVar()
su = StringVar()
ss = StringVar()
pw = StringVar()
fx = StringVar()
fy = StringVar()

try:
    f = open(filename)
except IOError:
    tkMessageBox.showinfo("Fehler", "config.txt fehlt")

for line in f:
        line = line.rstrip('\n')
        liste = line.split("=")
        if liste[0] == 'bg':
                bg.set(liste[1])
        elif liste[0] == 'ba':
                ba.set(liste[1])
        elif liste[0] == 'wp':
                wp.set(liste[1])
        elif liste[0] == 'bt':
                bt.set(liste[1])
        elif liste[0] == 'wl':
                wl.set(liste[1])
        elif liste[0] == 'hp':
                hp.set(liste[1])
        elif liste[0] == 'su':
                su.set(liste[1])
        elif liste[0] == 'ss':
                ss.set(liste[1])
        elif liste[0] == 'pw':
                pw.set(liste[1])
        elif liste[0] == 'fx':
                fx.set(liste[1])
        elif liste[0] == 'fy':
                fy.set(liste[1])                
f.close 

def Bsave():
        try:
            f = open(filename, 'w')
        except IOError:
            tkMessageBox.showinfo("Fehler", "config.txt fehlt")
        f.write("bg=" + str(bg.get()) + "\n")
        f.write("ba=" + str(ba.get()) + "\n")
        f.write("wp=" + str(wp.get()) + "\n")
        f.write("bt=" + str(bt.get()) + "\n")
        f.write("wl=" + str(wl.get()) + "\n")
        f.write("hp=" + str(hp.get()) + "\n")
        f.write("su=" + str(su.get()) + "\n")
        f.write("ss=" + str(ss.get()) + "\n")
        f.write("pw=" + str(pw.get()) + "\n")
        f.write("fx=" + str(fx.get()) + "\n")
        f.write("fy=" + str(fy.get()) + "\n")
        f.close

def Bback():
    mainWin.destroy()

ausgabelabel1 = ttk.Label(mainFrame, text='Bohrgeschwindigkeit [m/s]')
ausgabelabel1.place(x=5, y=50, width=200, height=20)

eingabelabel1 = ttk.Entry(mainFrame, textvariable=bg)
eingabelabel1.place(x=200, y=50, width=100, height=20)

ausgabelabel2 = ttk.Label(mainFrame, text='Bohrbeschleunigung [mm/ss]')
ausgabelabel2.place(x=5, y=70, width=200, height=20)
amax = StringVar()
eingabelabel2 = ttk.Entry(mainFrame, textvariable=ba)
eingabelabel2.place(x=200, y=70, width=100, height=20)

ausgabelabel3 = ttk.Label(mainFrame, text='Werkzeuwechselposition [mm]')
ausgabelabel3.place(x=5, y=90, width=200, height=20)
wwpos = StringVar()
eingabelabel3 = ttk.Entry(mainFrame, textvariable=wp)
eingabelabel3.place(x=200, y=90, width=100, height=20)

ausgabelabel4 = ttk.Label(mainFrame, text='Bohrtiefe [mm]')
ausgabelabel4.place(x=5, y=110, width=200, height=20)
btief = StringVar()
eingabelabel4 = ttk.Entry(mainFrame, textvariable=bt)
eingabelabel4.place(x=200, y=110, width=100, height=20)

ausgabelabel5 = ttk.Label(mainFrame, text='Werkzeuglänge [mm]')
ausgabelabel5.place(x=5, y=130, width=200, height=20)
wlang = StringVar()
eingabelabel5 = ttk.Entry(mainFrame, textvariable=wl)
eingabelabel5.place(x=200, y=130, width=100, height=20)

ausgabelabel6 = ttk.Label(mainFrame, text='Home-Position [mm]')
ausgabelabel6.place(x=5, y=150, width=200, height=20)
homepos = StringVar()
eingabelabel6 = ttk.Entry(mainFrame, textvariable=hp)
eingabelabel6.place(x=200, y=150, width=100, height=20)

ausgabelabel7 = ttk.Label(mainFrame, text='Schrittmotor [S/U]')
ausgabelabel7.place(x=5, y=170, width=200, height=20)
spu = StringVar()
eingabelabel7 = ttk.Entry(mainFrame, textvariable=su)
eingabelabel7.place(x=200, y=170, width=100, height=20)

ausgabelabel8 = ttk.Label(mainFrame, text='Spindelsteigung [mm/U]')
ausgabelabel8.place(x=5, y=190, width=200, height=20)
pitch = StringVar()
eingabelabel8 = ttk.Entry(mainFrame, textvariable=ss)
eingabelabel8.place(x=200, y=190, width=100, height=20)

ausgabelabel9 = ttk.Label(mainFrame, text='Spindeldrehzahl max. [%]')
ausgabelabel9.place(x=5, y=210, width=200, height=20)
pwm = StringVar()
eingabelabel9 = ttk.Entry(mainFrame, textvariable=pw)
eingabelabel9.place(x=200, y=210, width=100, height=20)

ausgabelabel10 = ttk.Label(mainFrame, text='Fadenkreuz x.Pos')
ausgabelabel10.place(x=5, y=5, width=200, height=20)
fkx = StringVar()
eingabelabel10 = ttk.Entry(mainFrame, textvariable=fx)
eingabelabel10.place(x=200, y=5, width=100, height=20)

ausgabelabel11 = ttk.Label(mainFrame, text='Fadenkreuz y-Pos.')
ausgabelabel11.place(x=5, y=25, width=200, height=20)
fky = StringVar()
eingabelabel11 = ttk.Entry(mainFrame, textvariable=fy)
eingabelabel11.place(x=200, y=25, width=100, height=20)

image2=PhotoImage(file='ico/save.png')
button2 = Button(master=mainFrame,image=image2, command=Bsave)
button2.place(x=25, y=245, width=50, height=50)

image4=PhotoImage(file='ico/back.png')
button4 = Button(master=mainFrame,image=image4, command=Bback)
button4.place(x=80, y=245, width=50, height=50)

mainWin.mainloop()

