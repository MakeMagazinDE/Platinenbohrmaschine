![GitHub Logo](http://www.heise.de/make/icons/make_logo.png)

Maker Media GmbH und c't, Heise Zeitschriften Verlag

***

# Platinenbohrmaschine
Halbautomatische Platinenbohrmaschine mit kamerabasierter Zentrierung. Bitte beachten Sie den Artikel in Make 2/2018.


Raspberry für PCB-Bohrmaschine installieren

1. Raspbian auf SD Karte flashen
2. ersten Start durchführen
3. sudo raspi-config
4. Expand Filesystem (unter advanced options)
5. Laendereinstellungen
6. Hostname aendern
7. Passwort aendern
8. sudo apt-get update && sudo apt-get upgrade
9. swap auf 1024 erweitern
  sudo su -c 'echo "CONF_SWAPSIZE=1024" > /etc/dphys-swapfile'
  sudo dphys-swapfile setup
  sudo dphys-swapfile swapon
10. Mount einrichten
  sudo mkdir /mnt/joerg
  in /etc/fstab: //192.168.9.101/joerg /mnt/joerg cifs username=joerg,password=*** 0 0
  sudo mount -av
11. unnoetige Softare entfernen
  Geany, Mathematica, Node Red, Scratch, Sonic Pi, Libreoffce
12. serielle Schnittstelle aktivieren
  /boot/cmdline.txt: console= ttyAMA0 oder ttyS0 oder serial0 entfernen
  /boot/config.txt: am Ende eintragen
     enable_uart=1 
     dtoverlay=pi3-disable-bt
  Rechte aendern: sudo usermod -a -G dialout pi
13. sudo apt-get install python-opencv
14. ./update ausfuehren
	#!/bin/bash
	sudo mount -av
	cp -rf /mnt/Joerg/Arduino/EigeneAnwendungen/PCB_Bohrer/Raspberry/upload/* /home/pi/
15. autostart ueber den main-menu-editor unter Einstellungen default aplications fuer lxde einfuegen
    dort unter autostart : @python3 /home/pi/bohrsteuerung.py
                           @python /home/pi/bohrcam.py eintragen
