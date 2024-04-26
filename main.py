#!/usr/bin/env python3

import time
from ev3dev2.motor import OUTPUT_A, OUTPUT_D, LargeMotor, MediumMotor
from ev3dev2.sound import Sound
from ev3dev2.sensor import INPUT_2
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.led import Leds

from ev3dev2.motor import OUTPUT_B, OUTPUT_C, MoveSteering, LargeMotor
from ev3dev2.button import Button

import math


spkr = Sound()
#color_sensor = ColorSensor(INPUT_3)
line_sensor = ColorSensor(INPUT_2)
move_motors = MoveSteering(OUTPUT_B, OUTPUT_C)

leds = Leds()



#classen 
#----------------------------------

from ev3dev2.motor import OUTPUT_B, OUTPUT_C, MoveSteering, LargeMotor
from ev3dev2.sensor import INPUT_1, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor, GyroSensor
from ev3dev2.button import Button

import math

move_motors = MoveSteering(OUTPUT_B, OUTPUT_C)
motor_right = LargeMotor(OUTPUT_C)
motor_left = LargeMotor(OUTPUT_B)



#color_sensor_right = ColorSensor(INPUT_4)
#color_sensor_left = ColorSensor(INPUT_1)

#gyro = GyroSensor(INPUT_3)

button = Button()


class wait_for_button:
    def wait():
        button.wait_for_released('middle')



#drive forward/backward for cm
class drive_for_cm:

    one_turns_cm = None

    def set_cm(value):
        global one_turns_cm
        one_turns_cm = value

    def drive(speed, cm):

        rotations = cm / one_turns_cm
        move_motors.on_for_rotations(0, speed, rotations)

#beschleunigtes anfahren
class beschleunigt:
    
    def drive_for_rounds(max_speed, start_speed, degrees):

        #-(x-a)^2*b+c
        c = max_speed - start_speed
        b = -c / -((degrees / 2)**2)
        a = math.sqrt(c / b)
        c += start_speed

        motor_left.position = 0
        speed = start_speed

        while speed >= start_speed:
            print(speed)
            x = motor_left.position
            speed = -((x - a)**2) * b + c
            print(speed)
            move_motors.on(0, speed)
        move_motors.off()

    def drive_for_cm(max_speed, start_speed, cm):
        #-(x-a)^2*b+c
        c = max_speed - start_speed
        b = -c / -((((cm / one_turns_cm)*360) / 2)**2)
        a = math.sqrt(c / b)
        c += start_speed

        motor_left.position = 0
        speed = start_speed

        while speed >= start_speed:
            x = motor_left.position
            speed = -((x - a)**2) * b + c
            move_motors.on(0, speed)
        move_motors.off()

    def drive_for_cm_back(max_speed, start_speed, cm):
        c_back = max_speed - start_speed
        b_back = -c_back / -((((cm / one_turns_cm)*360) / 2)**2)
        a_back = math.sqrt(c_back / b_back)
        c_back += start_speed

        motor_left.position = 0
        speed_back = start_speed

        while speed_back >= start_speed:
            x_back = -motor_left.position
            speed_back = -((x_back - a_back)**2) * b_back + c_back
            move_motors.on(0, -speed_back)
        move_motors.off()



#gerade aus fahren mit Gyro
class drive_with_gyro:

    def drive(speed, rounds):
        motor_right.position = 0
        motor_left.position = 0
        gyro.reset()

        move_motors.on(0, speed)

        berichtigung = 0

        while (motor_left.position + motor_right.position) / 2 <= rounds * 360:
            angle = gyro.angle
            if gyro > 0:
                berichtigung = 3
            elif gyro < 0:
                berichtigung = -3
            else:
                berichtigung = 0
            
            move_motors.on(berichtigung, speed)

        move_motors.off()



#turn on the spot by degrees
class turn_on_spot_for_degrees:

    motor_rotations_for_full_turn = None #how many motor rotations are needed for a 360° turn

    def set_motor_rotations_for_full_turn(value):
        global motor_rotations_for_full_turnn
        motor_rotations_for_full_turnn = value

    def turn(speed, degrees):
        rotations = motor_rotations_for_full_turnn / (360 / degrees)
        move_motors.on_for_rotations(100, speed, rotations)

    def turn_beschleunigt(max_speed, start_speed, degrees, side):
        degrees = (motor_rotations_for_full_turnn / (360 / degrees)) * 360

        #-(x-a)^2*b+c
        c = max_speed - start_speed
        b = -c / -((degrees / 2)**2)
        a = math.sqrt(c / b)
        c += start_speed

        motor_left.position = 0
        motor_right.position = 0
        
        speed = start_speed

        if (side == "right"):

            while speed >= start_speed:
                x = motor_left.position
                speed = -((x - a)**2) * b + c
                move_motors.on(100, speed)
            move_motors.off()
        elif (side == "left"):

            while speed >= start_speed:
                x = motor_right.position
                speed = -((x - a)**2) * b + c  # Geschwindigkeit mit umgekehrtem Vorzeichen
                print(speed)
                move_motors.on(100, -speed)  # Umkehrung des Vorzeichens hier
            move_motors.off()


        else:
            print("Error: the attribut'" + side + "' is not corekt")



#turn with one reel by degrees
class turn_for_degrees:

    motor_rotations_for_full_turn = None #how many motor rotations are needed for a 360° turn

    def set_motor_rotations_for_full_turn(value):
        global motor_rotations_for_full_turn
        motor_rotations_for_full_turn = value

    def turn(speed, degrees, side):
        rotations = motor_rotations_for_full_turn / (360 / degrees)
        if (side == "right"):
            motor_right.on_for_rotations(speed, rotations)
        elif (side == "left"):
            motor_left.on_for_rotations(speed, rotations)
        else:
            print("Error: the attribut'" + side + "' is not corekt")



#line follower with pid controler
class pid_line_folower():

    kp = 2
    ki = 0.02
    kd = 5

    target_value = 50

    def set_pid(p, i, d):
        global kp
        global ki
        global kd

        kp = p
        ki = i
        kd = d

    def set_target_value(value):
        global target_value
        target_value = value

    def folow_for_rotations(speed, rotations):
        global target_value
        global kp 
        global ki
        global kd 

        motor_left.position = 0

        integral = 0
        last_error = 0

        while (motor_left.position <= rotations * 360):
            value = color_sensor_right.reflected_light_intensity
            error = target_value - value
            integral += error
            derivative = error - last_error

            last_error = error

            output = kp * error + ki * integral + kd * derivative

            move_motors.on(output, speed)
        move_motors.stop()


    def folow_for_cm(speed, cm):
        global target_value
        global kp 
        global ki
        global kd 

        motor_left.position = 0

        integral = 0
        last_error = 0
        rotations = cm / one_turns_cm

        while (motor_left.position <= rotations * 360):
            value = color_sensor_right.reflected_light_intensity
            error = target_value - value
            integral += error
            derivative = error - last_error

            last_error = error

            output = kp * error + ki * integral + kd * derivative

            move_motors.on(output, speed)
        move_motors.stop()



#drive to black line
class drive_to_line:

    #drive to black line and stop
    def drive_and_stop(speed, side):

        color_sensor = None

        if (side == "right"):
            color_sensor = color_sensor_right
        elif (side == "left"):
            color_sensor = color_sensor_left
        else:
             print("Error: the attribut'" + side + "' is not corekt")

        while (color_sensor.reflected_light_intensity >= 7):
            move_motors.on(0, speed)
        move_motors.stop()

    #drive to the white line edge, slowly and stop at the line
    def drive_slow_stop(speed, slow_speed, side):

        color_sensor = None

        if (side == "right"):
            color_sensor = color_sensor_right
        elif (side == "left"):
            color_sensor = color_sensor_left
        else:
             print("Error: the attribut'" + side + "' is not corekt")

        while (color_sensor.reflected_light_intensity <= 30):
            move_motors.on(0, speed)
        while (color_sensor.reflected_light_intensity >= 20):
            move_motors.on(0, slow_speed)
        move_motors.stop()



#Align with the black line
class align_line:

    def drive_and_stop(speed):

        left = False
        right = False

        move_motors.on(0, speed)
        while (True):
            if (color_sensor_left.reflected_light_intensity <= 7):
                motor_left.stop(stop_action='brake')
                left = True
            if ( color_sensor_right.reflected_light_intensity <= 7):
                motor_right.stop(stop_action='brake')
                right = True
            if (right and left):
                break

        
    # drive to white, stop, drive slow to black    
    def drive_slow_stop(speed, slow_speed):

        left = False
        right = False

        move_motors.on(0, speed)

        while (True):
            if (color_sensor_left.reflected_light_intensity >= 30):
                motor_left.stop(stop_action='brake')
                left = True
            if ( color_sensor_right.reflected_light_intensity >= 30):
                motor_right.stop(stop_action='brake')
                right = True
            if (right and left):
                break


        left = False
        right = False

        move_motors.on(0, slow_speed)

        while (True):
            if (color_sensor_left.reflected_light_intensity <= 20):
                motor_left.stop(stop_action='brake')
                left = True
            if ( color_sensor_right.reflected_light_intensity <= 20):
                motor_right.stop(stop_action='brake')
                right = True
            if (right and left):
                break









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