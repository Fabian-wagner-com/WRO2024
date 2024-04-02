#!/usr/bin/env python3

from drive import *
import time
from ev3dev2.motor import OUTPUT_A, OUTPUT_D, LargeMotor, MediumMotor
from ev3dev2.sound import Sound
from ev3dev2.sensor import INPUT_3
from ev3dev2.sensor.lego import ColorSensor

spkr = Sound()
color_sensor = ColorSensor(INPUT_3)

#variabeln
#Abstand zu den Banden. Fareben bedeuten da, wo die Startbereiche den Farben am nächstens sin.
wall_distance_green = 0

stein1 = ""
stein2 = ""

drive_for_cm.set_cm(17.5929)
turn_on_spot_for_degrees.set_motor_rotations_for_full_turn(2.175)
turn_for_degrees.set_motor_rotations_for_full_turn(4.35)

motor_ele = LargeMotor(OUTPUT_D)
motor_zang = MediumMotor(OUTPUT_A)




spkr.speak('S')

wait_for_button.wait()
time.sleep(0.6)

motor_ele.on_for_rotations(-50, 0.3)

#an der Wand ausrichten
drive_for_cm.drive(20, 10 + wall_distance_green)

#ausparken
turn_for_degrees.turn(-15, 40, "left")
turn_for_degrees.turn(15, 20, "right")
drive_for_cm.drive(10, 3.1)
turn_for_degrees.turn(15, 44, "right")
drive_for_cm.drive(-10, 8.4)
turn_for_degrees.turn(-15, 12, "right")

beschleunigt.drive_for_cm_back(30, 5, 16)

#aufsammeln
motor_ele.on_for_rotations(50, 0.3)
motor_zang.on_for_rotations(50, 1.2)
motor_ele.on_for_rotations(-50, 0.3)

beschleunigt.drive_for_cm_back(30, 5, 9.8)
motor_zang.on_for_rotations(-50, 1.2)

motor_ele.on_for_rotations(50, 0.3)
motor_zang.on_for_rotations(50, 1.2)
motor_ele.on_for_rotations(-50, 0.3)

#zu blau/grün Steinen fahren
turn_for_degrees.turn(35, 90, "right")
drive_for_cm.drive(30, 5.1)
turn_on_spot_for_degrees.turn(30, 88)
drive_for_cm.drive(-25, 46)
#farbe erkennen
stein1 = color_sensor.color_name
spkr.speak(stein1)
print(stein1)

drive_for_cm.drive(-10, 9.8)
stein2 = color_sensor.color_name
spkr.speak(stein2)
print(stein2)

#rüber fahren
turn_on_spot_for_degrees.turn(-30, 88)
drive_for_cm.drive(60, 115)




def absetzen():
    #absetzen
    motor_ele.on_for_rotations(50, 0.35)
    motor_zang.on_for_rotations(-50, 0.8)
    motor_ele.on_for_rotations(-50, 0.54)
    drive_for_cm.drive(3, 10)