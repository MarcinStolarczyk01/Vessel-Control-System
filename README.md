# Vessel-Control-System
## Introduction
This repo contains a software which was a small part of my first degree engineering studies thesis which I graduated from University of Science and Technology in Wrocław.
As the title of the thesis was "Development of the concept of a remotely controlled floating unit" this solution is a program desired to enable controlling the vessel and getting feedback like onboard camera view and current engines RPMs at the same time.
Communication system was based on 4G connection established by SIM card managed my WWAN USB adapter plugged into Raspberry Pi 4.

## Idea
HTTP server hosted on an onboard computer provides a simple web application.
The vessel's motion system is based on two, symmetrically placed engines with two independent shafts.
Current course can be adjusted by changing balance between engines RPMs (via PWM signal output on GPIO pins).
Operator can manipulate engines power and their balance ratio by slider interface.
## Technologies
Programming languages:
- Python3
- CSS
- HTML (arguably :))

Python frameworks & libraries:
- GPIO Zero
- Flask
- Picamera2
- numpy
## Problems
The main issue with the solution was low FPS value which caused significant lag and made it hard to navigate especially while traveling with great speeds.
The solution for that could be implementing WebSocket or RTC connection which would increase the connection's bit rate.
#### _Full thesis is available here: https://drive.google.com/file/d/1kKVPxddbqeV-F_Ym20ivEoKj_XBN5spo/view?usp=sharing_