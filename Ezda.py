import os
import time
import pigpio

os.system("sudo pigpiod")

time.sleep(1)

ESC = 17
STEER = 18

pi = pigpio.pi()
pi.set_servo_pulsewidth(ESC, 0)
pi.set_servo_pulsewidth(STEER, 0)

pi.set_servo_pulsewidth(ESC, 1500)
time.sleep(1.5)

angle = 110
width_impulse = int(angle * 11.1 + 500)
pi.set_servo_pulsewidth(STEER, width_impulse)

pi.set_servo_pulsewidth(ESC, 1560)
time.sleep(5)


pi.set_servo_pulsewidth(ESC, 1500)
angle = 90
width_impulse = int(angle * 11.1 + 500)
pi.set_servo_pulsewidth(STEER, width_impulse)