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
      2. Communicates via MQTT with the GUI code tphat runs on the LAPTOP.
    """

    # test_raise_arm()
    # test_calibrate_arm()
    # test_move_arm_position()
    # test_lower_arm()

    # test_gos()

    # test_proximity()
    # test_camera()
    # test_color()

    real_thing()


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


def test_gos():
    robot = rosebot.RoseBot()
    robot.drive_system.go_straight_for_seconds(3, 50)
    robot.drive_system.stop()
    time.sleep(1)
    robot.drive_system.go_straight_for_inches_using_time(12, 100)
    robot.drive_system.stop()
    time.sleep(1)
    robot.drive_system.go_straight_for_inches_using_encoder(12, 50)


def test_proximity():
    robot = rosebot.RoseBot()
    # robot.drive_system.go_forward_until_distance_is_less_than(7, 50)

    robot.drive_system.go_backward_until_distance_is_greater_than(7, 50)


def test_camera():
    robot = rosebot.RoseBot()
    robot.drive_system.spin_clockwise_until_sees_object(30, 500)


def test_color():
    robot = rosebot.RoseBot()
    robot.drive_system.go_straight_until_intensity_is_greater_than(20, 50)


def real_thing():
    delegate = shared_gui_delegate_on_robot.receiver()
    mqtt_receiver = com.MqttClient(delegate)
    mqtt_receiver.connect_to_pc()

    while True:
        time.sleep(0.01)
        if delegate.is_time_to_stop:
            break

# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()