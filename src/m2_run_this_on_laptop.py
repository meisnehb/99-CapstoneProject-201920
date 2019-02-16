"""
  Capstone Project.  Code to run on a LAPTOP (NOT the robot).
  Displays the Graphical User Interface (GUI) and communicates with the robot.

  Authors:  Your professors (for the framework)
    and Alyssa Taylor.
  Winter term, 2018-2019.
"""

import mqtt_remote_method_calls as com
import tkinter
from tkinter import ttk
import shared_gui


def main():
    """
    This code, which must run on a LAPTOP:
      1. Constructs a GUI for my part of the Capstone Project.
      2. Communicates via MQTT with the code that runs on the EV3 robot.
    """
    # -------------------------------------------------------------------------
    # Construct and connect the MQTT Client:
    # -------------------------------------------------------------------------
    mqtt_sender = com.MqttClient()
    mqtt_sender.connect_to_ev3()

    # -------------------------------------------------------------------------
    # The root TK object for the GUI:
    # -------------------------------------------------------------------------
    root = tkinter.Tk()
    root.title = ('CSSE 120 CAPSTONE PROJECT, WINTER 18-19')

    # -------------------------------------------------------------------------
    # The main frame, upon which the other frames are placed.
    # -------------------------------------------------------------------------
    main_frame = ttk.Frame(root, padding=10, borderwidth=5, relief='groove')
    main_frame.grid()

    # -------------------------------------------------------------------------
    # Sub-frames for the shared GUI that the team developed:
    # -------------------------------------------------------------------------
    # teleop_frame, drive_system_frame, beeps_tones_frame, arm_frame, control_frame, sensor_frame, tone_frame = get_shared_frames(main_frame, mqtt_sender)

    # -------------------------------------------------------------------------
    # Frames that are particular to my individual contributions to the project.
    # -------------------------------------------------------------------------
    m2_marching_frame, m2_salute_frame = get_my_frames(main_frame, mqtt_sender)

    # -------------------------------------------------------------------------
    # Grid the frames.
    # -------------------------------------------------------------------------
    my_grid_frames(m2_marching_frame, m2_salute_frame)

    # -------------------------------------------------------------------------
    # The event loop:
    # -------------------------------------------------------------------------
    root.mainloop()


def get_shared_frames(main_frame, mqtt_sender):
    teleop_frame = shared_gui.get_teleoperation_frame(main_frame, mqtt_sender)
    drive_system_frame = shared_gui.get_drive_system_frame(main_frame, mqtt_sender)
    arm_frame = shared_gui.get_arm_frame(main_frame, mqtt_sender)
    control_frame = shared_gui.get_control_frame(main_frame, mqtt_sender)
    beeps_tones_frame = shared_gui.get_beeps_tones(main_frame, mqtt_sender)
    sensor_frame = shared_gui.get_sensor_frame(main_frame, mqtt_sender)
    tone_frame = shared_gui.get_proximity_tone_frame(main_frame, mqtt_sender)

    return teleop_frame, arm_frame, control_frame, drive_system_frame, beeps_tones_frame, sensor_frame, tone_frame


def get_my_frames(main_frame, mqtt_sender):
    m2_marching_frame = shared_gui.get_m2_marching_frame(main_frame, mqtt_sender)

    return m2_marching_frame, m2_salute_frame


def grid_frames(teleop_frame, arm_frame, control_frame, drive_system_frame,
                beeps_tones_frame, sensor_frame, tone_frame):
    teleop_frame.grid(row=0, column=0)
    arm_frame.grid(row=1, column=0)
    drive_system_frame.grid(row=0, column=1)
    control_frame.grid(row=2, column=0)
    beeps_tones_frame.grid(row=1, column=1)
    sensor_frame.grid(row=2, column=1)
    tone_frame.grid(row=0, column=2)


def my_grid_frames(m2_marching_frame, m2_salute_frame):
    m2_marching_frame.grid()
    m2_salute_frame.grid()


# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()