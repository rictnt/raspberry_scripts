#!/usr/bin/env python2.7

from time import sleep
import subprocess
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD) # choose BCM or BOARD numbering schemes. I use BOARD 

button_A = 18 # button is on pin 18
# it will work on any GPIO channel
# Optional 50K Ohm pull up to 3.3v. A push button will ground the pin, creating a falling edge.

long_press = 1 #s
very_long_press = 4 #s

red = 16 # set pin 16 for red led
green = 11 # set pin 11 for green led 
blue = 15 # set pin 15 for blue led 

Freq = 60 #Hz
pause_time = 0.01 # you can change this to slow down/speed up

GPIO.setup(button_A, GPIO.IN, pull_up_down=GPIO.PUD_UP) # set button pin as input
GPIO.setup(red, GPIO.OUT) # set red led pin as output
GPIO.setup(green, GPIO.OUT) # set green led pin as output
GPIO.setup(blue, GPIO.OUT) # set blue led pin as output
RED = GPIO.PWM(red, Freq)
GREEN = GPIO.PWM(green, Freq)
BLUE = GPIO.PWM(blue, Freq)

RED.start(0)
GREEN.start(0)
BLUE.start(0)

state = 1

def system_button(button_A):
	global state
	
	button_press_timer = 0
	while True:
			if (GPIO.input(button_A) == False) : # while button is still pressed down
				button_press_timer += 0.1 # keep counting until button is released
			else: # button is released, count for how long
				if (button_press_timer > very_long_press) : # pressed for > 5 seconds
					# do what you want with a very long press
					print "very long press : ", button_press_timer
					state = 0
					subprocess.call(['shutdown -h now "System halted by GPIO action" &'], shell=True)
					
				elif (button_press_timer > long_press) : # press for > 1 < 5 seconds
					# do what you want with a long press
					print "long press : ", button_press_timer
					state = 2
					subprocess.call(['sudo reboot &'], shell=True)
					
				elif (button_press_timer > 0.1):
					# do what you want with a short press
					print "short press : ", button_press_timer

				button_press_timer = 0
			sleep(0.1)

GPIO.add_event_detect(button_A, GPIO.FALLING, callback=system_button, bouncetime=100)
# setup the thread, detect a falling edge on channel and debounce it with 100mSec
	
# assume this is the main code...
try:
	while True:
		
		# do whatever while "waiting" for falling edge on channel
		for i in range(0,101):      # 101 because it stops when it finishes 100 
			if state == 0:
				RED.ChangeDutyCycle(i)
				GREEN.ChangeDutyCycle(0)
				BLUE.ChangeDutyCycle(0)
			if state == 1:
				RED.ChangeDutyCycle(0)
				GREEN.ChangeDutyCycle(i)
				BLUE.ChangeDutyCycle(0)
			if state == 2:
				RED.ChangeDutyCycle(i)
				GREEN.ChangeDutyCycle(0)
				BLUE.ChangeDutyCycle(100 - i)
			sleep(pause_time) 
			
		for i in range(100,-1,-1):      # from 100 to zero in steps of -1 
			if state == 0:
				RED.ChangeDutyCycle(i)
				GREEN.ChangeDutyCycle(0)
				BLUE.ChangeDutyCycle(0)
			if state == 1:
				RED.ChangeDutyCycle(0)
				GREEN.ChangeDutyCycle(i)
				BLUE.ChangeDutyCycle(0)
			if state == 2:
				RED.ChangeDutyCycle(i)
				GREEN.ChangeDutyCycle(0)
				BLUE.ChangeDutyCycle(100 - i)
			sleep(pause_time) 
			
except KeyboardInterrupt:
	GPIO.cleanup()       # clean up GPIO on CTRL+C exit
GPIO.cleanup()           # clean up GPIO on normal exit
