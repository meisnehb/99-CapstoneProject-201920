import rosebot
import mqtt_remote_method_calls as com
import time
#import shared_gui_delegate_on_robot
import tkinter as tk
from PIL import ImageTk, Image

def main():
    frame()

class air_power(object):

    def __init__(self):
        self.robot = rosebot.RoseBot()

    def song(self):

        NOTE_A4 = 440
        NOTE_B4 = 494
        NOTE_CS5 = 554
        NOTE_E5 = 659
        NOTE_FS5 = 740
        NOTE_GS5 = 831

        quarter_note = 500
        eighth_note = 250

        notes = [NOTE_A4, NOTE_B4, NOTE_CS5, NOTE_E5, NOTE_FS5, NOTE_GS5, NOTE_FS5, NOTE_E5, NOTE_CS5, NOTE_B4]

        self.robot.sound_system.tone_maker.play_tone(notes[0], quarter_note)
        self.robot.sound_system.tone_maker.play_tone(notes[1], quarter_note)
        self.robot.sound_system.tone_maker.play_tone(notes[2], quarter_note)
        self.robot.sound_system.tone_maker.play_tone(notes[4], quarter_note)
        self.robot.sound_system.tone_maker.play_tone(notes[5], quarter_note)

        self.robot.sound_system.tone_maker.play_tone(notes[6], eighth_note)

        self.robot.sound_system.tone_maker.play_tone(notes[7], quarter_note)
        self.robot.sound_system.tone_maker.play_tone(notes[8], quarter_note)
        self.robot.sound_system.tone_maker.play_tone(notes[9], 1500)
        self.robot.sound_system.tone_maker.play_tone(notes[10], 1500)

    def forward_march(self):
        self.robot.drive_system.go(50, 50)

        while True:
            if self.robot.sensor_system.ir_proximity_sensor.get_distance_in_inches() <= 4:
                self.robot.drive_system.stop()
                self.robot.arm_and_claw.raise_arm()
                self.robot.sound_system.speech_maker('safety')
                break

    def paces_forward(self, paces):
        self.robot.drive_system.go_straight_for_inches_using_encoder(paces, 50)

    def face(self, direction):
        if direction == 'right':
            self.robot.drive_system.left_motor.turn_on(50)
            time.sleep(2)
            self.robot.drive_system.stop()
        elif direction == 'left':
            self.robot.drive_system.right_motor.turn_on(50)
            time.sleep(2)
            self.robot.drive_system.stop()
        elif direction == 'about':
            self.robot.drive_system.left_motor.turn_on(50)
            time.sleep(4)
            self.robot.drive_system.stop()

    def halt(self):
        self.robot = rosebot.RoseBot()
        self.robot.drive_system.stop()

    def cover(self):
        self.robot = rosebot.RoseBot()
        self.robot.drive_system.right_motor.turn_on(70)
        time.sleep(0.3)
        self.robot.drive_system.right_motor.turn_off()
        self.robot.drive_system.left_motor.turn_on(70)
        time.sleep(0.3)
        self.robot.drive_system.left_motor.turn_off()

    def column(self, direction):

        if direction == 'right':
            self.robot.drive_system.right_motor.turn_off()
            time.sleep(2)
            self.robot.drive_system.right_motor.turn_on(50)
        elif direction == 'left':
            self.robot.drive_system.left_motor.turn_off()
            time.sleep(2)
            self.robot.drive_system.left_motor.turn_on(50)


    def column_half(direction):
        robot = rosebot.RoseBot()

        if direction == 'right':
            robot.drive_system.right_motor.turn_off()
            time.sleep(1)
            robot.drive_system.right_motor.turn_on(50)
        elif direction == 'left':
            robot.drive_system.left_motor.turn_off()
            time.sleep(1)
            robot.drive_system.left_motor.turn_on(50)

    def stretch(self):
        self.robot.arm_and_claw.raise_arm()
        self.robot.drive_system.right_motor.turn_on(4, 100)

    def recover(self):
        self.robot.arm_and_claw.lower_arm()
        self.robot.sound_system.speech_maker("Air Power")

    def hua(self):
        self.robot.sound_system.speech_maker('hoo ah')

def frame():
    mqtt_sender = com.MqttClient()
    mqtt_sender.connect_to_ev3()

    window = tk.Tk()
    window.title("AFROTC Simulator")
    window.geometry("500x500")
    window.configure(background='white')

    # Background Image
    path = "C:/Users/meisnehb/pictures/ROTC/airforce.png"

    img = ImageTk.PhotoImage(Image.open(path))

    panel = tk.Label(window, image=img)

    panel.pack(side="top", fill="both", expand="no")

    # Buttons
    harch_button = tk.Button(text="MARCH!")
    harch_button.place(relx=0.5, rely=.75, anchor='se')
    harch_button['command'] = lambda: handle_march(mqtt_sender, main_entry)

    halt_button = tk.Button(text="HALT!")
    halt_button.place(relx=0.6, rely=.75, anchor='se')
    halt_button['command'] = lambda: handle_halt(mqtt_sender, main_entry)

    cover_button = tk.Button(text='COVER!')
    cover_button.place(relx=0.7, rely=.75, anchor='se')
    cover_button['command'] = lambda: handle_cover(mqtt_sender)

    hua_button = tk.Button(text="HUA!")
    hua_button.place(relx=0.8, rely=.75, anchor='se')
    hua_button['command'] = lambda: handle_hua(mqtt_sender)


    # Entry Boxes
    main_entry = tk.Entry(window, bd=5)
    main_entry.pack(side='left', fill='none', expand='no')

    window.mainloop()

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

    if len(entry) == 7:                  # Column Movements
        if entry[7] == 'r':
            mqtt_sender.send_message('column', 'right')
        elif entry[7] == 'l':
            mqtt_sender.send_message('column', 'left')
        elif entry[7] == 'h':
            if entry[12] == 'r':
                mqtt_sender.send_message('column_half', 'right')
            elif entry[12] == 'l':
                mqtt_sender.send_message('column_half', 'left')
        elif entry[0] is 'f':                # Forward
            mqtt_sender.send_message('forward_march')
    elif type(entry[0]) == int:          # Paces Forward
        mqtt_sender.send_message('paces_forward', entry[0])

def handle_hua(mqtt_sender):
    print("HUA!")
    mqtt_sender.send_message('hua')

def handle_cover(mqtt_sender):
    print("COVER!")
    mqtt_sender.send_message('cover')

main()
