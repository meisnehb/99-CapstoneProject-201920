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

    def proxy_tone(self, f, r):
        self.robot.drive_system.go(50, 50)
        self.robot.sound_system.tone_maker.play_tone(f, 1000)
        while True:
            dis = self.robot.sensor_system.ir_proximity_sensor.get_distance_in_inches()
            print(dis)
            t = f + (r*dis)
            self.robot.sound_system.tone_maker.play_tone(t, 1000)
            if dis <= 1:
                self.robot.drive_system.stop()
                self.robot.arm_and_claw.raise_arm()
                break

    def proximity_beep(self, p, m):
        self.robot.drive_system.go(70, 70)
        while True:
            d = self.robot.sensor_system.ir_proximity_sensor.get_distance_in_inches()
            print(d)

            self.robot.sound_system.beeper.beep().wait(p)
            p = p - (m * d)
            if d <= 2:
                self.robot.drive_system.stop()
                self.robot.arm_and_claw.raise_arm()
                break


main()
