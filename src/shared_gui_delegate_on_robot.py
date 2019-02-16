"""
  Capstone Project.  Code to run on the EV3 robot (NOT on a laptop).
  This code is the delegate for handling messages from the shared GUI.

  Author:  Your professors (for the framework)
    and Hannah Meisner and Alyssa Taylor.
  Winter term, 2018-2019.
"""
import rosebot
import mqtt_remote_method_calls as com
import time


def main():
    name1 = 'Robot09'
    name2 = 'Hannah'

    my_delegate = receiver()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect(name1, name2)
    time.sleep(1)  # Time to allow the MQTT setup.
    print()

    time.sleep(0.01)  # Time to allow message processing


class receiver(object):
    def __init__(self):
        self.robot = rosebot.RoseBot()
        self.is_time_to_stop = False

    def forward(self, speedL, speedR):
        self.robot.drive_system.go(speedL, speedR)

    def stop(self):
        self.robot.drive_system.stop()

    def raise_arm(self):
        self.robot.arm_and_claw.raise_arm()

    def calibrate_arm(self):
        self.robot.arm_and_claw.calibrate_arm()

    def arm_pos(self, pos):
        self.robot.arm_and_claw.move_arm_to_position(pos)

    def lower_arm(self):
        self.robot.arm_and_claw.lower_arm()

    def straight_time(self, seconds, speed):
        self.robot.drive_system.go_straight_for_seconds(seconds, speed)

    def straight_inches(self, inches, speed):
        self.robot.drive_system.go_straight_for_inches_using_time(inches, speed)

    def straight_encoder(self, inches, speed):
        self.robot.drive_system.go_straight_for_inches_using_encoder(inches, speed)

    def quit(self):
        print("Quit")
        self.is_time_to_stop = True

    def beep_number_of_times(self, n):
        print('BEEP')
        for k in range(n):
            self.robot.sound_system.beeper.beep().wait(0.5)

    def tone(self, f, d):
        print('Nice Tone')
        self.robot.sound_system.tone_maker.play_tone(f, d)

    def speech(self, s):
        print('Phrase')
        self.robot.sound_system.speech_maker.speak(s)

    def color_stop(self, c):
        self.robot.drive_system.go_straight_until_color_is(c, 30)

    def cw_camera(self):
        self.robot.drive_system.spin_clockwise_until_sees_object(30, 400)

    def ccw_camera(self):
        self.robot.drive_system.spin_counterclockwise_until_sees_object(30, 400)

    def proxy_forward(self, d):
        self.robot.drive_system.go_forward_until_distance_is_less_than(d, 70)

    def m2_proxy_tone(self, f, r):
        self.robot.drive_system.go(50, 50)
        self.robot.sound_system.tone_maker.play_tone(f, 500)
        while True:
            dis = self.robot.sensor_system.ir_proximity_sensor.get_distance_in_inches()
            print(dis)
            t = f + (r*(1/(dis+0.1)))
            self.robot.sound_system.tone_maker.play_tone(t, 1000)
            if dis <= 1:
                self.robot.drive_system.stop()
                self.robot.arm_and_claw.raise_arm()
                break

    def proximity_beep(self, p, m):
        d = self.robot.sensor_system.ir_proximity_sensor.get_distance_in_inches()
        self.robot.drive_system.go(70, 70)
        while True:
            dc = self.robot.sensor_system.ir_proximity_sensor.get_distance_in_inches()
            print(dc)
            t = p - (abs((d - dc)/d)*m)
            print(t)
            self.robot.sound_system.beeper.beep().wait()
            time.sleep(t)
            if dc <= 2.0:
                self.robot.drive_system.stop()
                self.robot.arm_and_claw.raise_arm()
                break

###############################################################################
# M2 Sprint 3 Codes (Individual GUI, Tests, Functions)
###############################################################################
    def song(self):
        robot = rosebot.RoseBot()
        NOTE_A4 = 440
        NOTE_B4 = 494
        NOTE_CS5 = 554
        NOTE_E5 = 659
        NOTE_FS5 = 740
        NOTE_GS5 = 831

        quarter_note = 500
        eighth_note = 250

        notes = [NOTE_A4, NOTE_B4, NOTE_CS5, NOTE_E5, NOTE_FS5, NOTE_GS5, NOTE_FS5, NOTE_E5, NOTE_CS5, NOTE_B4]

        robot.sound_system.tone_maker.play_tone(notes[0], quarter_note).wait()
        robot.sound_system.tone_maker.play_tone(notes[1], quarter_note).wait()
        robot.sound_system.tone_maker.play_tone(notes[2], quarter_note).wait()
        robot.sound_system.tone_maker.play_tone(notes[3], quarter_note).wait()
        robot.sound_system.tone_maker.play_tone(notes[4], quarter_note).wait()
        robot.sound_system.tone_maker.play_tone(notes[5], eighth_note).wait()
        robot.sound_system.tone_maker.play_tone(notes[6], quarter_note).wait()
        robot.sound_system.tone_maker.play_tone(notes[7], quarter_note).wait()
        robot.sound_system.tone_maker.play_tone(notes[8], 1500).wait()
        robot.sound_system.tone_maker.play_tone(notes[9], 1500).wait()

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

    def column_half(self, direction):
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
        self.robot.sound_system.speech_maker.speak("Air Power")

    def hua(self):
        self.robot.sound_system.speech_maker.speak('hoo ah')


###############################################################################
# M2 Sprint 3 Codes (Individual GUI, Tests, Functions)
###############################################################################
    # def m2_af_song(self):
        # self.robot.sound_system.tone_maker.play_tone_sequence()

    def m2_forward_march(self):
        self.robot.sound_system.speech_maker.speak('Forward Harch!')
        time.sleep(1)
        self.robot.drive_system.go(50, 50)

    def m2_double_time(self):
        self.robot.sound_system.speech_maker.speak('Double Time!')
        time.sleep(1)
        self.robot.drive_system.go(100, 100)

    def m2_column_right(self):
        self.robot.sound_system.speech_maker.speak('Column Right Harch!')
        time.sleep(1)
        self.robot.drive_system.go(50, 25)

    def m2_column_left(self):
        self.robot.sound_system.speech_maker.speak('Column Right Harch!')
        time.sleep(1)
        self.robot.drive_system.go(50, 25)

main()
