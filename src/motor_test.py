from gpiozero import Motor
from time import sleep

boat_motor = Motor('GPIO26', 'GPIO19', pwm=True)

boat_motor.forward()
sleep(60)
