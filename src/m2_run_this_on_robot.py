"""
  Capstone Project.  Code to run on the EV3 robot (NOT on a laptop).
  Author:  Your professors (for the framework)
    and Alyssa Taylor.
  Winter term, 2018-2019.
"""

import rosebot
import mqtt_remote_method_calls as com
import time
import shared_gui_delegate_on_robot


def main():
    """
    This code, which must run on the EV3 ROBOT:
      1. Makes the EV3 robot to various things.
      2. Communicates via MQTT with the GUI code that runs on the LAPTOP.
    """

    # test_raise_arm()
    test_calibrate_arm()
    print('calibrate')
    time.sleep(3)
    test_move_arm_position()
    print('move')
    time.sleep(3)
    test_lower_arm()
    print('lower')

    # real_thing()


def test_raise_arm():
    robot = rosebot.RoseBot()
    robot.arm_and_claw.raise_arm()


def test_calibrate_arm():
    robot = rosebot.RoseBot()
    robot.arm_and_claw.calibrate_arm()


def test_move_arm_position():
    robot = rosebot.RoseBot()
    robot.arm_and_claw.move_arm_to_position(5000)


def test_lower_arm():
    robot = rosebot.RoseBot()
    robot.arm_and_claw.lower_arm()


# def real_thing():
#     robot = rosebot.RoseBot()
#     delegate = shared_gui_delegate_on_robot.receiver(robot)
#     mqtt_receiver = com.MqttClient(delegate)
#     mqtt_receiver.connect_to_pc()
#
#     while True:
#         time.sleep(0.01)

# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()