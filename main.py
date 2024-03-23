#!/usr/bin/env python3

from drive import *
import time
from ev3dev2.motor import OUTPUT_A, LargeMotor

drive_for_cm.set_cm(17.5929)
turn_on_spot_for_degrees.set_motor_rotations_for_full_turn(2.02)

motor_tool = LargeMotor(OUTPUT_A)


for i in range(4):
    motor_tool.on_for_rotations(-50, 1)
    motor_tool.on_for_rotations(50, 1)
    drive_for_cm.drive(-20, 10.8)
    #9.8 nach vorne
    drive_for_cm.drive(20, 1)