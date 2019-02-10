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
    name1 = 'Robot23'
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

    def forward(self, speedL, speedR):
        self.robot.drive_system.go(speedL, speedR)

    def stop(self):
        self.robot.drive_system.stop()

main()
