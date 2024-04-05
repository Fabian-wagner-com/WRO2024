#!/usr/bin/env python3

from drive import *
import time
from ev3dev2.motor import OUTPUT_A, OUTPUT_D, LargeMotor, MediumMotor
from ev3dev2.sound import Sound
from ev3dev2.sensor import INPUT_3, INPUT_2
from ev3dev2.sensor.lego import ColorSensor

spkr = Sound()
#color_sensor = ColorSensor(INPUT_3)
line_sensor = ColorSensor(INPUT_2)
move_motors = MoveSteering(OUTPUT_B, OUTPUT_C)


#functions
#-------------------------------

def ausparken():
    #ausparken
    turn_for_degrees.turn(-15, 40, "left")
    turn_for_degrees.turn(15, 20, "right")
    drive_for_cm.drive(10, 3.1)
    turn_for_degrees.turn(15, 44, "right")
    drive_for_cm.drive(-10, 9.1)
    turn_for_degrees.turn(-15, 10.5, "right")


def ausparken2():
    #ausparken
    turn_for_degrees.turn(-15, 40, "left")
    turn_for_degrees.turn(15, 20, "right")
    drive_for_cm.drive(10, 3.1)
    turn_for_degrees.turn(15, 44, "right")
    drive_for_cm.drive(-10, 8.5)
    turn_for_degrees.turn(-15, 11.98, "right")


def absetzen():
    #absetzen
    motor_ele.on_for_rotations(50, 0.35)
    motor_zang.on_for_rotations(-50, 1)
    motor_ele.on_for_rotations(-50, 0.63)
    drive_for_cm.drive(3, 8.4)



#variabeln
#-------------------------------

#Abstand zu den Banden. Fareben bedeuten da, wo die Startbereiche den Farben am nächstens sind.
wall_distance_green = 0 # in cm
wall_distance_red = 1 #in cm

fahrstulbewegung = 0.3 + 0.02

#steinfarben
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
start_time = time.time()

motor_ele.on_for_rotations(-50, fahrstulbewegung)

#programm
#-------------------------------

#an der Wand ausrichten
drive_for_cm.drive(20, 10)
drive_for_cm.drive(-10, wall_distance_green)

#ausparken
ausparken()

beschleunigt.drive_for_cm_back(30, 5, 16)

#aufsammeln
motor_ele.on_for_rotations(50, fahrstulbewegung)
motor_zang.on_for_rotations(50, 1.2)
motor_ele.on_for_rotations(-50, fahrstulbewegung)

beschleunigt.drive_for_cm_back(30, 5, 9.8)
motor_zang.on_for_rotations(-50, 1.2)

motor_ele.on_for_rotations(50, fahrstulbewegung)
motor_zang.on_for_rotations(50, 1.2)
motor_ele.on_for_rotations(-50, fahrstulbewegung)


#rüber fahren
turn_for_degrees.turn(35, 127, "right")
drive_for_cm.drive(65, 83)
turn_for_degrees.turn(35, 36, "left")
drive_for_cm.drive(35, 25.4)
time.sleep(0.2)
drive_for_cm.drive(-10, wall_distance_red)

ausparken2()

#nach hinten fahren bis zu braun
reflection = line_sensor.reflected_light_intensity
if reflection <= 55:
    move_motors.on(0, 10)
    while reflection <= 50:
        reflection = line_sensor.reflected_light_intensity

else:
    move_motors.on(0, -10)
    while reflection >= 50:
        reflection = line_sensor.reflected_light_intensity  
move_motors.off()

#drive_for_cm.drive(-30, 13)

#einsammeln
motor_zang.on_for_rotations(-50, 1.2)
motor_ele.on_for_rotations(50, fahrstulbewegung)
motor_zang.on_for_rotations(50, 1.2)
motor_ele.on_for_rotations(-50, fahrstulbewegung)

drive_for_cm.drive(-20, 9.8)
motor_zang.on_for_rotations(-50, 1.2)

motor_ele.on_for_rotations(50, fahrstulbewegung)
motor_zang.on_for_rotations(50, 1.2)
motor_ele.on_for_rotations(-50, fahrstulbewegung)

#zum abstellen
turn_for_degrees.turn(35, 88, "right")
drive_for_cm.drive(30, 43.2)
turn_on_spot_for_degrees.turn(20, 90)
drive_for_cm.drive(30, 16.6)
absetzen()

#Schrott in d'Ecke bringen
turn_for_degrees.turn(40, 46, "left")
drive_for_cm.drive(55, 50)

#zur Wasserleitung rasen
turn_for_degrees.turn(-40, 44, "right")
drive_for_cm.drive(-45, 17)
turn_for_degrees.turn(-40, 90, "right")
motor_ele.on_for_rotations(60, 0.47)
drive_for_cm.drive(-45, 17.3)

#Klempner spielen  --> Wasserleitung reparerien
motor_ele.on_for_rotations(-60, 0.47)
turn_on_spot_for_degrees.turn(-35,90)
















spkr.speak('Yeah')

#Zeit ausgeben
#-------------------------------
end_time = time.time()
duration = round(end_time - start_time, 2)
print( duration, "Sekunden")