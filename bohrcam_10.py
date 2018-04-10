#!/usr/bin/python2
# -*- coding: utf-8 -*-

import numpy as np  
import cv2

filename = 'bohrconf.txt'

cam = cv2.VideoCapture(0)  
cam.open(0)  
cam.set(3,640)  
cam.set(4,480)  

def nothing(x):
    pass

img = np.zeros((1,400,3), np.uint8)
cv2.namedWindow('Fadenkreuz')
cv2.moveWindow('Fadenkreuz',0,0)
cv2.createTrackbar('x','Fadenkreuz',0,100,nothing)
cv2.createTrackbar('y','Fadenkreuz',0,100,nothing)

try:
    f = open(filename)
except IOError:
    tkMessageBox.showinfo("Fehler", "config.txt fehlt")

for line in f:
    line = line.rstrip('\n')
    liste = line.split("=")
    if liste[0] == 'fx':
        x = int(liste[1])
    elif liste[0] == 'fy':
        y = int(liste[1])
f.close 

cv2.setTrackbarPos('x','Fadenkreuz',x)
cv2.setTrackbarPos('y','Fadenkreuz',y)

while(True):  
  ret, frame = cam.read()  
  cv2.imshow('Fadenkreuz',img)

  X = cv2.getTrackbarPos('x','Fadenkreuz') + 320 - 25
  Y = cv2.getTrackbarPos('y','Fadenkreuz') + 240 -25

  cv2.line(frame,(0,Y),(800,Y),(255,0,0),2)  
  cv2.line(frame,(X,0),(X,600),(255,0,0),2)  
  cv2.circle(frame,(X,Y), 20, (0,0,255), 1)  
  cv2.circle(frame,(X,Y), 50, (0,0,255), 2)  

  cv2.moveWindow('Platinenbohranlage',0,0)  
  cv2.imshow('Platinenbohranlage',frame)
  
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break  

cam.release()  
cv2.destroyAllWindows()
