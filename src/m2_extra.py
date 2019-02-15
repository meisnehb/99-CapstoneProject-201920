###############################################################################
# Sprint 3 Codes (Individual GUI, Tests, Functions)
###############################################################################
import rosebot
import mqtt_remote_method_calls as com
import time
import shared_gui_delegate_on_robot


def main():


def forward_march():
    asd

def af_song():
    asdf

def gui_sender():
    robot = rosebot.RoseBot()
    delegate = shared_gui_delegate_on_robot.receiver()
    mqtt_receiver = com.MqttClient(delegate)
    mqtt_receiver.connect_to_pc()

    while True:
        time.sleep(0.01)
        if delegate.is_time_to_stop:
            break