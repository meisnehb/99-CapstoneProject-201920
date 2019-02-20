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
        self.is_halt = False
        self.is_column = False

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
# M1 Sprint 3 Codes (Individual GUI, Tests, Functions)
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
            if self.is_halt is True:
                self.robot.drive_system.stop()
                self.is_halt = False
                break
            if self.robot.sensor_system.color_sensor.get_color_as_name() == 'White':
                self.safety()
                break
            elif self.robot.sensor_system.ir_proximity_sensor.get_distance_in_inches() <= 4:
                self.safety()
                break
            elif self.is_column == True:
                self.is_column = False
                break

    def paces_forward(self, paces):
        paces = int(paces)
        self.robot.drive_system.go_straight_for_inches_using_encoder(paces, 50)

    def face(self, direction):
        if direction == 'right':
            self.robot.drive_system.left_motor.turn_on(50)
            self.robot.drive_system.right_motor.turn_on(-50)
            time.sleep(1.55)
            self.robot.drive_system.stop()
        elif direction == 'left':
            self.robot.drive_system.right_motor.turn_on(50)
            self.robot.drive_system.left_motor.turn_on(-50)
            time.sleep(1.55)
            self.robot.drive_system.stop()
        elif direction == 'about':
            self.robot.drive_system.left_motor.turn_on(50)
            self.robot.drive_system.right_motor.turn_on(-50)
            time.sleep(3.1)
            self.robot.drive_system.stop()

    def halt(self):
        print(self.is_halt)
        self.is_halt = True
        print(self.is_halt)


    def cover(self):
        self.robot = rosebot.RoseBot()
        self.robot.drive_system.right_motor.turn_on(70)
        time.sleep(0.3)
        self.robot.drive_system.right_motor.turn_off()
        self.robot.drive_system.left_motor.turn_on(70)
        time.sleep(0.3)
        self.robot.drive_system.left_motor.turn_off()

    def column(self, direction):
        self.is_column = True
        if direction == 'right':
            self.robot.drive_system.right_motor.turn_off()
            time.sleep(2.75)
            self.forward_march()
        elif direction == 'left':
            self.robot.drive_system.left_motor.turn_off()
            time.sleep(2.75)
            self.forward_march()

    def column_half(self, direction):
        self.is_column = True
        if direction == 'right':
            self.robot.drive_system.right_motor.turn_off()
            time.sleep(1.325)
            self.forward_march()
        elif direction == 'left':
            self.robot.drive_system.left_motor.turn_off()
            time.sleep(1.325)
            self.forward_march()

    def hua(self):
        self.robot.sound_system.speech_maker.speak('hoo ah')

    def safety(self):
        self.robot.drive_system.stop()
        self.robot.sound_system.speech_maker.speak("Safety")

    def report(self):
        self.robot.drive_system.spin_clockwise_until_sees_object(30, 400)
        self.robot.drive_system.go_forward_until_distance_is_less_than(4, 65)
        self.robot.arm_and_claw.raise_arm()
        self.robot.arm_and_claw.lower_arm()
        self.robot.sound_system.speech_maker.speak("cadet robo reports in as ordered")

    def to_the_rear(self):
        self.robot.drive_system.right_motor.turn_off()
        time.sleep(5.3)
        self.forward_march()

    def find_superior_branch(self):
        self.robot.sound_system.speech_maker.speak("Air Force of Course")
        self.robot.sound_system.speech_maker.speak("Air Power")

###############################################################################
# M2 Sprint 3 Codes (Individual GUI, Tests, Functions)
###############################################################################
    def m2_af_song(self):
        NOTE_C4 = 262
        NOTE_D4 = 294
        NOTE_E4 = 330
        NOTE_F4 = 349
        NOTE_G4 = 392
        NOTE_A4 = 440
        NOTE_B4 = 494
        NOTE_C5 = 523

        eighth_notes = 250
        quarter_note = 400
        triplet_note = 750
        whole_note = 1000

        notes = [NOTE_C4, NOTE_D4, NOTE_E4, NOTE_F4, NOTE_G4, NOTE_A4, NOTE_B4, NOTE_C5]

        self.robot.sound_system.tone_maker.play_tone(notes[1], quarter_note).wait()
        self.robot.sound_system.tone_maker.play_tone(notes[3], quarter_note).wait()
        self.robot.sound_system.tone_maker.play_tone(notes[3], whole_note).wait()

        self.robot.sound_system.tone_maker.play_tone(notes[2], quarter_note).wait()
        self.robot.sound_system.tone_maker.play_tone(notes[1], quarter_note).wait()
        self.robot.sound_system.tone_maker.play_tone(notes[0], quarter_note).wait()
        self.robot.sound_system.tone_maker.play_tone(notes[1], triplet_note).wait()
        self.robot.sound_system.tone_maker.play_tone(notes[2], triplet_note).wait()
        self.robot.sound_system.tone_maker.play_tone(notes[3], triplet_note).wait()
        self.robot.sound_system.tone_maker.play_tone(notes[3], triplet_note).wait()

        self.robot.sound_system.tone_maker.play_tone(notes[4], quarter_note).wait()
        self.robot.sound_system.tone_maker.play_tone(notes[6], quarter_note).wait()
        self.robot.sound_system.tone_maker.play_tone(notes[6], triplet_note).wait()
        self.robot.sound_system.tone_maker.play_tone(notes[7], quarter_note).wait()
        self.robot.sound_system.tone_maker.play_tone(notes[6], quarter_note).wait()
        self.robot.sound_system.tone_maker.play_tone(notes[4], quarter_note).wait()
        self.robot.sound_system.tone_maker.play_tone(notes[2], whole_note).wait()

        self.robot.sound_system.tone_maker.play_tone(notes[1], quarter_note).wait()
        self.robot.sound_system.tone_maker.play_tone(notes[3], quarter_note).wait()
        self.robot.sound_system.tone_maker.play_tone(notes[3], whole_note).wait()

        self.robot.sound_system.tone_maker.play_tone(notes[2], quarter_note).wait()
        self.robot.sound_system.tone_maker.play_tone(notes[1], quarter_note).wait()
        self.robot.sound_system.tone_maker.play_tone(notes[0], quarter_note).wait()
        self.robot.sound_system.tone_maker.play_tone(notes[1], triplet_note).wait()
        self.robot.sound_system.tone_maker.play_tone(notes[2], triplet_note).wait()
        self.robot.sound_system.tone_maker.play_tone(notes[3], triplet_note).wait()
        self.robot.sound_system.tone_maker.play_tone(notes[3], triplet_note).wait()

    def m2_airmans_creed(self):
        self.robot.sound_system.speech_maker.speak("I AM AN AMERICAN AIRMAN, "
                                                   "I AM A WARRIOR, I HAVE ANSWERED MY NATION’S CALL, "
                                                   "I AM AN AMERICAN AIRMAN, "
                                                   "MY MISSION IS TO FLY FIGHT AND WIN, "
                                                   "I AM FAITHFUL TO A PROUD HERITAGE, "
                                                   "A TRADITION OF HONOR, "
                                                   "AND A LEGACY OF VALOR, "
                                                   "I AM AN AMERICAN AIRMAN, "
                                                   "GUARDIAN OF FREEDOM AND JUSTICE, "
                                                   "MY NATION’S SWORD AND SHIELD, "
                                                   "ITS SENTRY AND AVENGER, "
                                                   "I DEFEND MY COUNTRY WITH MY LIFE, "
                                                   "I AM AN AMERICAN AIRMAN, "
                                                   "WINGMAN, LEADER, WARRIOR, "
                                                   "I WILL NEVER LEAVE AN AIRMAN BEHIND, "
                                                   "I WILL NEVER FALTER, AND I WILL NOT FAIL")

    def m2_forward_march(self):
        self.robot.sound_system.speech_maker.speak('Forward Harch!').wait()
        time.sleep(1)
        self.robot.drive_system.go(50, 50)

    def m2_double_time(self):
        self.robot.sound_system.speech_maker.speak('Double Time!').wait()
        time.sleep(1)
        self.robot.drive_system.go(100, 100)

    def m2_column_right(self):
        self.robot.sound_system.speech_maker.speak('Column Right Harch!').wait()
        time.sleep(1)
        self.robot.drive_system.go(50, 0)
        time.sleep(2.8)
        self.robot.drive_system.go(25, 25)
        time.sleep(1)
        self.robot.sound_system.speech_maker.speak('Forward Harch!').wait()
        time.sleep(1)
        self.robot.drive_system.go(50, 50)

    def m2_column_left(self):
        self.robot.sound_system.speech_maker.speak('Column Left Harch!').wait()
        time.sleep(1)
        self.robot.drive_system.go(0, 50)
        time.sleep(2.8)
        self.robot.drive_system.go(25, 25)
        time.sleep(1)
        self.robot.sound_system.speech_maker.speak('Forward Harch!').wait()
        time.sleep(1)
        self.robot.drive_system.go(50, 50)

    def m2_halt(self):
        self.robot.sound_system.speech_maker.speak('Halt!').wait()
        time.sleep(1)
        self.robot.drive_system.stop()

    def m2_present_arms(self):
        self.robot.sound_system.speech_maker.speak('Present Harms!').wait()
        time.sleep(1)
        self.robot.arm_and_claw.raise_arm()

    def m2_order_arms(self):
        self.robot.sound_system.speech_maker.speak('Order Harms!').wait()
        time.sleep(1)
        self.robot.arm_and_claw.lower_arm()

    def m2_color_sense(self, c):
        self.robot.drive_system.go_straight_until_color_is(c, 50)
        self.robot.sound_system.speech_maker.speak('I have found the Color you are looking for')

    def m2_find_object(self, i):
        self.robot.drive_system.go_straight_for_inches_using_encoder(i, 50)
        time.sleep(0.5)
        self.robot.drive_system.spin_counterclockwise_until_sees_object(50, 400)
        time.sleep(0.5)
        self.robot.drive_system.go(0, -20)
        time.sleep(0.8)
        self.robot.drive_system.go_forward_until_distance_is_less_than(1.5, 50)
        time.sleep(0.5)
        self.robot.drive_system.go_straight_for_inches_using_encoder(1.5, 50)
        time.sleep(1)
        self.robot.arm_and_claw.raise_arm()



main()
