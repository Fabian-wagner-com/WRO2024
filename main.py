#!/usr/bin/env python3

from drive import *
import time
from ev3dev2.motor import OUTPUT_A, OUTPUT_D, LargeMotor, MediumMotor
from ev3dev2.sound import Sound
from ev3dev2.sensor import INPUT_3, INPUT_2
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.led import Leds


spkr = Sound()
#color_sensor = ColorSensor(INPUT_3)
line_sensor = ColorSensor(INPUT_2)
move_motors = MoveSteering(OUTPUT_B, OUTPUT_C)

leds = Leds()


#functions
#-------------------------------

def ausparken():
    #ausparken
    turn_for_degrees.turn(-15, 40, "left")
    turn_for_degrees.turn(15, 20, "right")
    drive_for_cm.drive(10, 3.1)
    turn_for_degrees.turn(15, 44, "right")
    drive_for_cm.drive(-10, 9.2)
    turn_for_degrees.turn(-15, 10.5, "right")


def ausparken2():
    #ausparken
    turn_for_degrees.turn(-15, 40, "left")
    turn_for_degrees.turn(15, 20, "right")
    drive_for_cm.drive(10, 2.9)
    turn_for_degrees.turn(15, 44, "right")
    drive_for_cm.drive(-10, 7.5)
    turn_for_degrees.turn(-15, 13.6, "right")

def ausparken3():
    #ausparken
    turn_for_degrees.turn(-15, 40, "left")
    turn_for_degrees.turn(15, 20, "right")
    drive_for_cm.drive(10, 3.1)
    turn_for_degrees.turn(15, 44, "right")
    drive_for_cm.drive(-10, 7.7)
    turn_for_degrees.turn(-15, 12.2, "right")

def ausparken4():
    #ausparken
    turn_for_degrees.turn(-15, 40, "left")
    turn_for_degrees.turn(15, 20, "right")
    drive_for_cm.drive(10, 3.1)
    turn_for_degrees.turn(15, 44, "right")
    drive_for_cm.drive(-10, 7.3)
    turn_for_degrees.turn(-15, 11.2, "right")



def absetzen():
    #absetzen
    motor_ele.on_for_rotations(50, 0.35)
    motor_zang.on_for_rotations(-50, 1)
    motor_ele.on_for_rotations(-50, 0.9)
    drive_for_cm.drive(5, 8.4)

def drifeToBrown():
    reflection = line_sensor.reflected_light_intensity
    if reflection <= 60:
        move_motors.on(0, 10)
        while reflection <= 50:
            reflection = line_sensor.reflected_light_intensity

    else:
        move_motors.on(0, -10)
        while reflection >= 60:
            reflection = line_sensor.reflected_light_intensity  
    move_motors.off()



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



spkr.speak('s')
leds.set_color("LEFT", "RED")
leds.set_color("RIGHT", "RED")

wait_for_button.wait()
leds.set_color("LEFT", "GREEN")
leds.set_color("RIGHT", "GREEN")
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
turn_for_degrees.turn(35, 128, "right")
drive_for_cm.drive(65, 83)
turn_for_degrees.turn(35, 37, "left")
drive_for_cm.drive(35, 27.5)
time.sleep(0.2)
drive_for_cm.drive(-10, wall_distance_red)

ausparken2() #erstes mal

#nach hinten fahren bis zu braun
drifeToBrown()

#drive_for_cm.drive(-30, 13)

#einsammeln
motor_zang.on_for_rotations(-50, 1.4)
motor_ele.on_for_rotations(50, fahrstulbewegung)
motor_zang.on_for_rotations(50, 1.4)
motor_ele.on_for_rotations(-50, fahrstulbewegung)

drive_for_cm.drive(-20, 9.8)
motor_zang.on_for_rotations(-50, 1.4)

motor_ele.on_for_rotations(50, fahrstulbewegung)
motor_zang.on_for_rotations(50, 1.4)
motor_ele.on_for_rotations(-50, fahrstulbewegung)

#zum abstellen
turn_for_degrees.turn(35, 88, "right")
drive_for_cm.drive(30, 43.2)
turn_on_spot_for_degrees.turn(20, 90)
drive_for_cm.drive(30, 15.5)
absetzen()

#Schrott in d'Eck bringen
turn_for_degrees.turn(35, 46, "left")
drive_for_cm.drive(52, 50)

#zur Wasserleitung rasen
turn_for_degrees.turn(-35, 44, "right")
drive_for_cm.drive(-45, 17.9)
turn_for_degrees.turn(-35, 90, "right")
motor_ele.on_for_rotations(60, 0.7)
drive_for_cm.drive(-45, 9.7)

#Klempner spielen  --> Wasserleitung reparerien
motor_ele.on_for_rotations(-60, 0.5)
turn_on_spot_for_degrees.turn(-35, 55)
turn_on_spot_for_degrees.turn(35, 26)

#zu den gelben Steinen fahren
#--------------------------

drive_for_cm.drive(70, 54)
turn_for_degrees.turn(30, 70, "right")
drive_for_cm.drive(40, 22.2)

time.sleep(0.2)
drive_for_cm.drive(-10, wall_distance_red)

ausparken3()

drive_for_cm.drive(-15, 6)

#nach hinten fahren bis zu braun
drifeToBrown()


drive_for_cm.drive(-30, 19.6)

#einsammeln
#motor_zang.on_for_rotations(-50, 1.2)
motor_ele.on_for_rotations(50, fahrstulbewegung + 0.4)
motor_zang.on_for_rotations(50, 1)
motor_ele.on_for_rotations(-50, fahrstulbewegung)

drive_for_cm.drive(-20, 9.8)
motor_zang.on_for_rotations(-50, 1.2)

motor_ele.on_for_rotations(50, fahrstulbewegung)
motor_zang.on_for_rotations(50, 1.2)
motor_ele.on_for_rotations(-50, fahrstulbewegung)


#rüber fahren
turn_for_degrees.turn(35, 120, "right")
drive_for_cm.drive(70, 90)
turn_for_degrees.turn(70, 30, "left")
drive_for_cm.drive(50, 12)
drive_for_cm.drive(-10, wall_distance_green)

ausparken4()
drifeToBrown()

drive_for_cm.drive(-30, 20)

#einsammeln
motor_zang.on_for_rotations(-50, 1.4)
motor_ele.on_for_rotations(50, fahrstulbewegung)
motor_zang.on_for_rotations(50, 1.4)
motor_ele.on_for_rotations(-50, fahrstulbewegung)

drive_for_cm.drive(-20, 9.8)
motor_zang.on_for_rotations(-50, 1.4)

motor_ele.on_for_rotations(50, fahrstulbewegung)
motor_zang.on_for_rotations(50, 1.4)
motor_ele.on_for_rotations(-50, fahrstulbewegung)

#zum Gelben Abstellbereich
turn_for_degrees.turn(30, 102, "right")
drive_for_cm.drive(50, 49)
absetzen()














spkr.speak('good job')

#Zeit ausgeben
#-------------------------------
end_time = time.time()
duration = round(end_time - start_time, 3)
print( duration, " Sekunden")

minutes = duration // 60
seconds = duration - 60 * minutes
print(round(minutes, 0), " Minuten und ", round(seconds, 2), " Sekunden")