"""
  Capstone Project.  Code to run on the EV3 robot (NOT on a laptop).
  Author:  Your professors (for the framework)
    and Alyssa Taylor.
  Winter term, 2018-2019.
"""

import rosebot
import mqtt_remote_method_calls as com
import time


def main():
    """
    This code, which must run on the EV3 ROBOT:
      1. Makes the EV3 robot to various things.
      2. Communicates via MQTT with the GUI code that runs on the LAPTOP.
    """

    # test_raise_arm()
    test_calibrate_arm()
    time.sleep(3)
    test_move_arm_position()
    time.sleep(3)
    test_lower_arm()


def test_raise_arm():
    robot = rosebot.RoseBot()
    robot.arm_and_claw.raise_arm()


def test_calibrate_arm():
    robot = rosebot.RoseBot()
    robot.arm_and_claw.calibrate_arm()


def test_move_arm_position():
    robot = rosebot.RoseBot()
    robot.arm_and_claw.move_arm_to_position(5112)


def test_lower_arm():
    robot = rosebot.RoseBot()
    robot.arm_and_claw.lower_arm()

# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()