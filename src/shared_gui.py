"""
  Capstone Project.  Code to run on a LAPTOP (NOT the robot).
  Constructs and returns Frame objects for the basics:
  -- teleoperation
  -- arm movement
  -- stopping the robot program

  This code is SHARED by all team members.  It contains both:
    -- High-level, general-purpose methods for a Snatch3r EV3 robot.
    -- Lower-level code to interact with the EV3 robot library.

  Author:  Your professors (for the framework and lower-level code)
    and Hannah Meisner and Alyssa Taylor.
  Winter term, 2018-2019.
"""

import tkinter
from tkinter import ttk
from PIL import ImageTk
from PIL import Image
import time


def get_teleoperation_frame(window, mqtt_sender):
    """
    Constructs and returns a frame on the given window, where the frame
    has Entry and Button objects that control the EV3 robot's motion
    by passing messages using the given MQTT Sender.
      :type  window:       ttk.Frame | ttk.Toplevel
      :type  mqtt_sender:  com.MqttClient
    """
    # Construct the frame to return:
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()

    # Construct the widgets on the frame:
    frame_label = ttk.Label(frame, text="Teleoperation")
    left_speed_label = ttk.Label(frame, text="Left wheel speed (0 to 100)")
    right_speed_label = ttk.Label(frame, text="Right wheel speed (0 to 100)")

    left_speed_entry = ttk.Entry(frame, width=8)
    left_speed_entry.insert(0, "100")
    right_speed_entry = ttk.Entry(frame, width=8, justify=tkinter.RIGHT)
    right_speed_entry.insert(0, "100")

    forward_button = ttk.Button(frame, text="Forward")
    backward_button = ttk.Button(frame, text="Backward")
    left_button = ttk.Button(frame, text="Left")
    right_button = ttk.Button(frame, text="Right")
    stop_button = ttk.Button(frame, text="Stop")

    # Grid the widgets:
    frame_label.grid(row=0, column=1)
    left_speed_label.grid(row=1, column=0)
    right_speed_label.grid(row=1, column=2)
    left_speed_entry.grid(row=2, column=0)
    right_speed_entry.grid(row=2, column=2)

    forward_button.grid(row=3, column=1)
    left_button.grid(row=4, column=0)
    stop_button.grid(row=4, column=1)
    right_button.grid(row=4, column=2)
    backward_button.grid(row=5, column=1)

    # Set the button callbacks:
    forward_button["command"] = lambda: handle_forward(
        left_speed_entry, right_speed_entry, mqtt_sender)
    backward_button["command"] = lambda: handle_backward(
        left_speed_entry, right_speed_entry, mqtt_sender)
    left_button["command"] = lambda: handle_left(
        left_speed_entry, right_speed_entry, mqtt_sender)
    right_button["command"] = lambda: handle_right(
        left_speed_entry, right_speed_entry, mqtt_sender)
    stop_button["command"] = lambda: handle_stop(mqtt_sender)

    return frame


def get_arm_frame(window, mqtt_sender):
    """
    Constructs and returns a frame on the given window, where the frame
    has Entry and Button objects that control the EV3 robot's Arm
    by passing messages using the given MQTT Sender.
      :type  window:       ttk.Frame | ttk.Toplevel
      :type  mqtt_sender:  com.MqttClient
    """
    # Construct the frame to return:
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()

    # Construct the widgets on the frame:
    frame_label = ttk.Label(frame, text="Arm and Claw")
    position_label = ttk.Label(frame, text="Desired arm position:")
    position_entry = ttk.Entry(frame, width=8)

    raise_arm_button = ttk.Button(frame, text="Raise arm")
    lower_arm_button = ttk.Button(frame, text="Lower arm")
    calibrate_arm_button = ttk.Button(frame, text="Calibrate arm")
    move_arm_button = ttk.Button(frame,
                                 text="Move arm to position (0 to 5112)")
    blank_label = ttk.Label(frame, text="")

    # Grid the widgets:
    frame_label.grid(row=0, column=1)
    position_label.grid(row=1, column=0)
    position_entry.grid(row=1, column=1)
    move_arm_button.grid(row=1, column=2)

    blank_label.grid(row=2, column=1)
    raise_arm_button.grid(row=3, column=0)
    lower_arm_button.grid(row=3, column=1)
    calibrate_arm_button.grid(row=3, column=2)

    # Set the Button callbacks:
    raise_arm_button["command"] = lambda: handle_raise_arm(mqtt_sender)
    lower_arm_button["command"] = lambda: handle_lower_arm(mqtt_sender)
    calibrate_arm_button["command"] = lambda: handle_calibrate_arm(mqtt_sender)
    move_arm_button["command"] = lambda: handle_move_arm_to_position(
        position_entry, mqtt_sender)

    return frame


def get_control_frame(window, mqtt_sender):
    """
    Constructs and returns a frame on the given window, where the frame has
    Button objects to exit this program and/or the robot's program (via MQTT).
      :type  window:       ttk.Frame | ttk.Toplevel
      :type  mqtt_sender:  com.MqttClient
    """
    # Construct the frame to return:
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()

    # Construct the widgets on the frame:
    frame_label = ttk.Label(frame, text="Control")
    quit_robot_button = ttk.Button(frame, text="Stop the robot's program")
    exit_button = ttk.Button(frame, text="Stop this and the robot's program")

    # Grid the widgets:
    frame_label.grid(row=0, column=1)
    quit_robot_button.grid(row=1, column=0)
    exit_button.grid(row=1, column=2)

    # Set the Button callbacks:
    quit_robot_button["command"] = lambda: handle_quit(mqtt_sender)
    exit_button["command"] = lambda: handle_exit(mqtt_sender)

    return frame


def get_drive_system_frame(window, mqtt_sender):
    # Construct the frame to return:
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()

    # Construct the widgets on the frame:
    frame_label = ttk.Label(frame, text="Drive System")
    time_button = ttk.Button(frame, text="Go Straight (Time)")
    inches_button = ttk.Button(frame, text="Go Straight (Inches)")
    encoder_button = ttk.Button(frame, text='Go Straight (Encoder)')

    speed_label = ttk.Label(frame, text="Speed")
    inches_label = ttk.Label(frame, text="Inches")
    time_label = ttk.Label(frame, text="Time")

    inches_entry = ttk.Entry(frame, width=8)
    speed_entry = ttk.Entry(frame, width=8)
    seconds_entry = ttk.Entry(frame, width=8)

    blank_label = ttk.Label(frame, text="")

    # Grid the widgets:
    frame_label.grid(row=0, column=1)
    speed_label.grid(row=1, column=1)
    inches_label.grid(row=1, column=2)
    time_label.grid(row=1, column=0)

    inches_entry.grid(row=2, column=2)
    speed_entry.grid(row=2, column=1)
    seconds_entry.grid(row=2, column=0)

    blank_label.grid(row=3, column=1)

    time_button.grid(row=4, column=0)
    inches_button.grid(row=4, column=2)
    encoder_button.grid(row=4, column=1)

    # Set the Button callbacks:
    time_button["command"] = lambda: handle_timeStraight(seconds_entry, speed_entry, mqtt_sender)
    inches_button["command"] = lambda: handle_inchesStraight(inches_entry, speed_entry, mqtt_sender)
    encoder_button["command"] = lambda: handle_encoderStraight(inches_entry, speed_entry, mqtt_sender)


    return frame


def get_beeps_tones(window, mqtt_sender):
    # Construct the frame to return:
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()

    # Construct the widgets on the frame:
    frame_label = ttk.Label(frame, text="Beep and Tone")

    num_of_beeps_label = ttk.Label(frame, text="Number of Beeps:")
    num_of_beeps_entry = ttk.Entry(frame, width=8)
    num_of_beeps_button = ttk.Button(frame, text="Number of Beeps")

    freq_label = ttk.Label(frame, text='Frequency')
    freq_entry = ttk.Entry(frame, width=8)
    duration_label = ttk.Label(frame, text='Duration')
    duration_entry = ttk.Entry(frame, width=8)
    play_button = ttk.Button(frame, text="Play Tone")

    phrase_label = ttk.Label(frame, text='Desired Phrase:')
    phrase_entry = ttk.Entry(frame, width=8)
    phrase_button = ttk.Button(frame, text="Speak")

    blank_label1 = ttk.Label(frame, text="")
    blank_label2 = ttk.Label(frame, text="")
    blank_label3 = ttk.Label(frame, text="")


    # Grid the widgets:
    frame_label.grid(row=0, column=1)
    num_of_beeps_label.grid(row=1, column=0)
    freq_label.grid(row=5, column=0)
    duration_label.grid(row=5, column=2)
    phrase_label.grid(row=1, column=2)

    num_of_beeps_entry.grid(row=2, column=0)
    freq_entry.grid(row=6, column=0)
    duration_entry.grid(row=6, column=2)
    phrase_entry.grid(row=2, column=2)

    blank_label1.grid(row=4, column=0)
    blank_label2.grid(row=8, column=0)
    blank_label3.grid(row=2, column=1)

    num_of_beeps_button.grid(row=3, column=0)
    play_button.grid(row=6, column=1)
    phrase_button.grid(row=3, column=2)

    # Set the Button callbacks:
    num_of_beeps_button["command"] = lambda: handle_beep(num_of_beeps_entry, mqtt_sender)
    play_button["command"] = lambda: handle_tone(freq_entry, duration_entry, mqtt_sender)
    phrase_button["command"] = lambda: handle_speech(phrase_entry, mqtt_sender)

    return frame


def get_sensor_frame(window, mqtt_sender):
    # Construct the frame to return:
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()

    # Construct the widgets on the frame:
    frame_label = ttk.Label(frame, text="Sensors and Camera")

    color_label = ttk.Label(frame, text="Color Number/Name:")
    color_entry = ttk.Entry(frame, width=8)
    color_button = ttk.Button(frame, text="Forward")

    camera_label = ttk.Label(frame, text="Camera:")
    cw_button = ttk.Button(frame, text="CW")
    ccw_button = ttk.Button(frame, text='CCW')

    prox_label = ttk.Label(frame, text="Distance (Inches):")
    prox_entry = ttk.Entry(frame, width=8)
    prox_button = ttk.Button(frame, text="Forward")

    # Grid the widgets:
    frame_label.grid(row=0, column=1)
    color_label.grid(row=1, column=0)
    camera_label.grid(row=1, column=1)
    prox_label.grid(row=1, column=2)

    color_entry.grid(row=2, column=0)
    prox_entry.grid(row=2, column=2)

    color_button.grid(row=4, column=0)
    cw_button.grid(row=3, column=1)
    ccw_button.grid(row=4, column=1)
    prox_button.grid(row=4, column=2)

    # Doing stuff with buttons and boxes
    color_button['command'] = lambda: handle_color_stop(mqtt_sender, color_entry)
    cw_button['command'] = lambda: handle_cw_camera(mqtt_sender)
    ccw_button['command'] = lambda: handle_ccw_camera(mqtt_sender)
    prox_button['command'] = lambda: handle_proxy_forward(mqtt_sender, prox_entry)

    return frame


def get_proximity_tone_frame(window, mqtt_sender):
    # Construct the frame to return:
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()

    # Construct the widgets on the frame:
    frame_label = ttk.Label(frame, text="Increasing Frequency")

    freq_entry = ttk.Entry(frame, width=8)
    rate_entry = ttk.Entry(frame, width=8)
    forward_button = ttk.Button(frame, text="Forward")
    freq_label = ttk.Label(frame, text="Starting Frequency")
    rate_label = ttk.Label(frame, text="Rate of Change")

    # Grid the widgets:
    frame_label.grid(row=0, column=1)
    freq_label.grid(row=1, column=0)
    freq_entry.grid(row=2, column=0)
    rate_label.grid(row=1, column=2)
    rate_entry.grid(row=2, column=2)
    forward_button.grid(row=3, column=1)

    # Doing stuff with buttons and boxes
    forward_button['command'] = lambda: m2_handle_proximity_tone(mqtt_sender, freq_entry, rate_entry)

    return frame


def get_proximity_beep_frame(window, mqtt_sender):
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()

    frame_label = ttk.Label(frame, text="Beep Proximity")

    pause_entry = ttk.Entry(frame, width=8)
    multiplier_entry = ttk.Entry(frame, width=8)
    forward_button = ttk.Button(frame, text='Forward')

    frame_label.grid(row=0, column=1)
    pause_entry.grid(row=1, column=0)
    multiplier_entry.grid(row=1, column=1)
    forward_button.grid(row=1, column=2)

    forward_button['command'] = lambda: handle_proximity_beep(mqtt_sender, pause_entry, multiplier_entry)

    return frame

###############################################################################
###############################################################################
# The following specifies, for each Button,
# what should happen when the Button is pressed.
###############################################################################
###############################################################################

###############################################################################
# Handlers for Buttons in the Teleoperation frame.
###############################################################################


def handle_forward(left_entry_box, right_entry_box, mqtt_sender):
    print('Forward')
    l = left_entry_box.get()
    r = right_entry_box.get()
    mqtt_sender.send_message("forward", [l, r])
    """
    Tells the robot to move using the speeds in the given entry boxes,
    with the speeds used as given.
      :type  left_entry_box:   ttk.Entry
      :type  right_entry_box:  ttk.Entry
      :type  mqtt_sender:      com.MqttClient
    """


def handle_backward(left_entry_box, right_entry_box, mqtt_sender):
    print('Backward')
    l = int(left_entry_box.get()) * -1
    r = int(right_entry_box.get()) * -1
    mqtt_sender.send_message("forward", [l, r])

    """
    Tells the robot to move using the speeds in the given entry boxes,
    but using the negatives of the speeds in the entry boxes.
      :type  left_entry_box:   ttk.Entry
      :type  right_entry_box:  ttk.Entry
      :type  mqtt_sender:      com.MqttClient
    """


def handle_left(left_entry_box, right_entry_box, mqtt_sender):
    print("Left")
    l = int(left_entry_box.get()) * 0.5
    r = int(right_entry_box.get())
    mqtt_sender.send_message("forward", [l, r])

    """
    Tells the robot to move using the speeds in the given entry boxes,
    but using the negative of the speed in the left entry box.
      :type  left_entry_box:   ttk.Entry
      :type  right_entry_box:  ttk.Entry
      :type  mqtt_sender:      com.MqttClient
    """


def handle_right(left_entry_box, right_entry_box, mqtt_sender):
    print("Right")
    l = int(left_entry_box.get())
    r = int(right_entry_box.get()) * 0.5
    mqtt_sender.send_message("forward", [l, r])

    """
    Tells the robot to move using the speeds in the given entry boxes,
    but using the negative of the speed in the right entry box.
      :type  left_entry_box:   ttk.Entry
      :type  right_entry_box:  ttk.Entry
      :type  mqtt_sender:      com.MqttClient
    """


def handle_stop(mqtt_sender):
    print("Stop")
    mqtt_sender.send_message('stop')

    """
    Tells the robot to stop.
      :type  mqtt_sender:  com.MqttClient
    """


###############################################################################
# Handlers for Buttons in the DriveSystem frame.
###############################################################################
def handle_timeStraight(seconds_entry, speed_entry, mqtt_sender):
    print()
    sec = int(seconds_entry.get())
    s = int(speed_entry.get())
    mqtt_sender.send_message('straight_time', [sec, s])


def handle_inchesStraight(inches_entry, speed_entry, mqtt_sender):
    print()
    i = int(inches_entry.get())
    s = int(speed_entry.get())
    mqtt_sender.send_message('straight_inches', [i, s])


def handle_encoderStraight(inches_entry, speed_entry, mqtt_sender):
    print()
    i = int(inches_entry.get())
    s = int(speed_entry.get())
    mqtt_sender.send_message('straight_encoder', [i, s])


###############################################################################
# Handlers for Buttons in the BeepsAndTones frame.
###############################################################################

def handle_beep(num_of_beeps_entry, mqtt_sender):
    print()
    n = int(num_of_beeps_entry.get())
    mqtt_sender.send_message('beep_number_of_times', [n])


def handle_tone(freq_entry, duration_entry, mqtt_sender):
    print()
    f = int(freq_entry.get())
    d = int(duration_entry.get())
    mqtt_sender.send_message('tone', [f, d])


def handle_speech(phrase_entry, mqtt_sender):
    print()
    p = phrase_entry.get()
    mqtt_sender.send_message('speech', [p])


###############################################################################
# Handlers for Buttons in the ArmAndClaw frame.
###############################################################################
def handle_raise_arm(mqtt_sender):
    print("Raise")
    mqtt_sender.send_message('raise_arm')

    """
    Tells the robot to raise its Arm until its touch sensor is pressed.
      :type  mqtt_sender:  com.MqttClient
    """


def handle_lower_arm(mqtt_sender):
    print('Lower')
    mqtt_sender.send_message('lower_arm')

    """
    Tells the robot to lower its Arm until it is all the way down.
      :type  mqtt_sender:  com.MqttClient
    """


def handle_calibrate_arm(mqtt_sender):
    print('Calibrate that Boi')
    mqtt_sender.send_message('calibrate_arm')

    """
    Tells the robot to calibrate its Arm, that is, first to raise its Arm
    until its touch sensor is pressed, then to lower its Arm until it is
    all the way down, and then to mark taht position as position 0.
      :type  mqtt_sender:  com.MqttClient
    """


def handle_move_arm_to_position(arm_position_entry, mqtt_sender):
    print('Move Arm to Position')
    pos = int(arm_position_entry.get())
    mqtt_sender.send_message('arm_pos', [pos])

    """
    Tells the robot to move its Arm to the position in the given Entry box.
    The robot must have previously calibrated its Arm.
      :type  arm_position_entry  ttk.Entry
      :type  mqtt_sender:        com.MqttClient
    """


###############################################################################
# Handlers for sensors
###############################################################################
def handle_color_stop(mqtt_sender, color_entry):
    c = color_entry.get()
    print('Forward until not color:', c)
    mqtt_sender.send_message('color_stop', [c])


def handle_cw_camera(mqtt_sender):
    print("Spin clockwise to object")
    mqtt_sender.send_message('cw_camera')


def handle_ccw_camera(mqtt_sender):
    print("Spin counter-clockwise to object")
    mqtt_sender.send_message('ccw_camera')


def handle_proxy_forward(mqtt_sender, proxy_entry):
    d = float(proxy_entry.get())
    print("Go forward until:", d, 'inches away')
    mqtt_sender.send_message('proxy_forward', [d])


###############################################################################
# Handlers for sensors
###############################################################################
def handle_proximity_beep(mqtt_sender, pause_entry, multiplier_entry):
    p = float(pause_entry.get())
    m = float(multiplier_entry.get())
    print("Baseline pause is", p, "with multiplier", m)
    mqtt_sender.send_message('proximity_beep', [p, m])


def m2_handle_proximity_tone(mqtt_sender, freq_entry, rate_entry):
    f = float(freq_entry.get())
    r = float(rate_entry.get())
    print('Start frequency is', f, 'rate of change is', r)
    mqtt_sender.send_message('m2_proxy_tone', [f, r])


###############################################################################
# Handlers for Buttons in the Control frame.
###############################################################################
def handle_quit(mqtt_sender):
    print('Quit')
    mqtt_sender.send_message('quit')

    """
    Tell the robot's program to stop its loop (and hence quit).
      :type  mqtt_sender:  com.MqttClient
    """


def handle_exit(mqtt_sender):
    print('Exit')
    handle_quit(mqtt_sender)
    exit()

    """
    Tell the robot's program to stop its loop (and hence quit).
    Then exit this program.
      :type mqtt_sender: com.MqttClient
    """

###############################################################################
# M1 Sprint 3 Codes (Individual GUI, Tests, Functions)
###############################################################################
def get_m1_frame(window, mqtt_sender):
    # window.title("AFROTC Simulator")
    # window.geometry("500x500")
    # window.configure(background='white')

    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()

    # Buttons
    harch_button = ttk.Button(frame, text="MARCH!")
    harch_button['command'] = lambda: handle_march(mqtt_sender, main_entry)

    halt_button = ttk.Button(frame, text="HALT!")
    halt_button.grid(row=10, column=10)
    halt_button['command'] = lambda: handle_halt(mqtt_sender, main_entry)

    cover_button = ttk.Button(frame, text='COVER!')
    cover_button['command'] = lambda: handle_cover(mqtt_sender)

    hua_button = ttk.Button(frame, text="HUA!")
    hua_button['command'] = lambda: handle_hua(mqtt_sender)

    # Entry Boxes
    main_entry = ttk.Entry(frame)

    # Grid Everything
    main_entry.grid()
    harch_button.grid()
    cover_button.grid(row=1, column=1)
    hua_button.grid(row=2, column=2)

    return frame
def image(window, mqtt_sender):
    # Background Image
    path = "C:/Users/meisnehb/pictures/ROTC/airforce.png"
    img = ImageTk.PhotoImage(Image.open(path))
    panel = ttk.Label(window, image=img)

    panel.pack()


def handle_halt(mqtt_sender, main_entry):
    entry = main_entry.get()
    print(entry.upper())
    if entry == 'flight':
        print(" HALT!")
        mqtt_sender.send_message('halt')
        print('FLIGHT HALT WHAT?')

def handle_march(mqtt_sender, main_entry):
    entry = main_entry.get()
    print(entry.upper())
    print(" HARCH!")

    if len(entry) >= 11:                                      # Column Movements
        if entry[7] == 'l':
            mqtt_sender.send_message('column', 'left')
        elif entry[7] == 'r':
            mqtt_sender.send_message('column', 'right')
        elif entry[7] == 'h':
            if entry[12] == 'r':
                mqtt_sender.send_message('column_half', 'right')
            elif entry[12] == 'l':
                mqtt_sender.send_message('column_half', 'left')
        elif entry[0] is 'f':                               # Forward
            mqtt_sender.send_message('forward_march')
    elif type(entry[0]) == int:                             # Paces Forward
        mqtt_sender.send_message('paces_forward', entry[0])

def handle_hua(mqtt_sender):
    print("HUA!")
    mqtt_sender.send_message('hua')

def handle_cover(mqtt_sender):
    print("COVER!")
    mqtt_sender.send_message('cover')


###############################################################################
# M2 Sprint 3 Codes (Individual GUI, Tests, Functions)
###############################################################################
def get_m2_marching_frame(window, mqtt_sender):
    # Construct the frame to return:
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()

    # Construct the widgets on the frame:
    frame_label = ttk.Label(frame, text="Marching")
    forward_march_button = ttk.Button(frame, text="Forward March")
    column_left_button = ttk.Button(frame, text="Column Left")
    column_right_button = ttk.Button(frame, text="Column Right")
    halt_button = ttk.Button(frame, text="Halt")
    double_time_button = ttk.Button(frame, text='Double Time')

    # Grid the widgets
    frame_label.grid(row=0, column=1)
    forward_march_button.grid(row=3, column=1)
    column_left_button.grid(row=4, column=0)
    halt_button.grid(row=5, column=1)
    column_right_button.grid(row=4, column=2)
    double_time_button.grid(row=4, column=1)

    # Set the button callbacks:
    forward_march_button["command"] = lambda: handle_m2_forward_march(mqtt_sender)
    halt_button["command"] = lambda: handle_m2_halt(mqtt_sender)
    column_right_button["command"] = lambda: handle_m2_column_right(mqtt_sender)
    column_left_button["command"] = lambda: handle_m2_column_left(mqtt_sender)
    double_time_button["command"] = lambda: handle_m2_double_time(mqtt_sender)

    return frame


def get_m2_salute_frame(window, mqtt_sender):
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()

    # Construct the widgets on the frame:
    frame_label = ttk.Label(frame, text="Salute")
    present_arms_button = ttk.Button(frame, text="Present Arms")
    order_arms_button = ttk.Button(frame, text="Order Arms")

    # Grid the widgets
    frame_label.grid(row=0, column=1)
    present_arms_button.grid(row=3, column=0)
    order_arms_button.grid(row=3, column=3)

    # Button Callbacks
    present_arms_button["command"] = lambda: handle_m2_present_arms(mqtt_sender)
    order_arms_button["command"] = lambda: handle_m2_order_arms(mqtt_sender)

    return frame


def get_m2_af_morale_frame(window, mqtt_sender):
    # Construct the frame to return:
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()

    # Construct the widgets on the frame:
    frame_label = ttk.Label(frame, text="Air Force Morale")
    af_song_button = ttk.Button(frame, text="AF Song")
    airmans_creed_button = ttk.Button(frame, text="Airman's Creed")

    blank_label = ttk.Label(frame, text='')

    # Grid the widgets
    frame_label.grid(row=0, column=1)
    af_song_button.grid(row=2, column=0)
    airmans_creed_button.grid(row=2, column=2)
    blank_label.grid(row=1, column=1)

    # Set the button callbacks:
    af_song_button["command"] = lambda: handle_m2_af_song(mqtt_sender)
    airmans_creed_button["command"] = lambda: handle_m2_airmans_creed(mqtt_sender)

    return frame


def get_m2_sensor_frame(window, mqtt_sender):
    # Construct the frame to return:
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()

    # Construct the widgets on the frame:
    frame_label = ttk.Label(frame, text="Sensors")
    color_button = ttk.Button(frame, text="Find Color")
    find_button = ttk.Button(frame, text="Find Object")
    inches_label = ttk.Label(frame, text="How Far is the Object?")
    color_label = ttk.Label(frame, text="What Color Do You Want?")
    inches_entry = ttk.Entry(frame, width=8)
    color_entry = ttk.Entry(frame, width=8)

    # Grid the widgets
    frame_label.grid(row=0, column=1)
    color_button.grid(row=5, column=0)
    find_button.grid(row=5, column=2)
    color_label.grid(row=2, column=0)
    inches_entry.grid(row=4, column=2)
    inches_label.grid(row=2, column=2)
    color_entry.grid(row=4, column=0)

    # Set the button callbacks:
    color_button["command"] = lambda: handle_m2_color_sense(mqtt_sender, color_entry)
    find_button["command"] = lambda: handle_m2_find_object(mqtt_sender, inches_entry)


    return frame


def handle_m2_forward_march(mqtt_sender):
    print('Forward Harch!')
    mqtt_sender.send_message('m2_forward_march')


def handle_m2_halt(mqtt_sender):
    print('Halt!')
    mqtt_sender.send_message('m2_halt')


def handle_m2_double_time(mqtt_sender):
    print('Double Time')
    mqtt_sender.send_message('m2_double_time')


def handle_m2_column_right(mqtt_sender):
    print('Column Right')
    mqtt_sender.send_message('m2_column_right')


def handle_m2_column_left(mqtt_sender):
    print('Column Left')
    mqtt_sender.send_message('m2_column_left')


def handle_m2_present_arms(mqtt_sender):
    print('Present Arms')
    mqtt_sender.send_message('m2_present_arms')


def handle_m2_order_arms(mqtt_sender):
    print('Order Arms')
    mqtt_sender.send_message('m2_order_arms')


def handle_m2_af_song(mqtt_sender):
    print('Wild Blue Yonder!')
    mqtt_sender.send_message('m2_af_song')


def handle_m2_airmans_creed(mqtt_sender):
    print('Airmans Creed')
    mqtt_sender.send_message('m2_airmans_creed')


def handle_m2_color_sense(color_entry, mqtt_sender):
    print('Finding Colors')
    c = color_entry.get()
    mqtt_sender.send_message('m2_color_sense', [c])


def handle_m2_find_object(inches_entry, mqtt_sender):
    print('Finding Object')
    i = int(inches_entry.get())
    mqtt_sender.send_message('m2_find_object', [i])