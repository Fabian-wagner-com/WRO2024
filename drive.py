#!/usr/bin/env python3

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