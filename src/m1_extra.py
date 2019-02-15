import rosebot
import mqtt_remote_method_calls as com
import time
import shared_gui_delegate_on_robot


def main():
    song()

def song():
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

    robot.sound_system.tone_maker.play_tone(notes[0], quarter_note)
    robot.sound_system.tone_maker.play_tone(notes[1], quarter_note)
    robot.sound_system.tone_maker.play_tone(notes[2], quarter_note)
    robot.sound_system.tone_maker.play_tone(notes[4], quarter_note)
    robot.sound_system.tone_maker.play_tone(notes[5], quarter_note)

    robot.sound_system.tone_maker.play_tone(notes[6], eighth_note)

    robot.sound_system.tone_maker.play_tone(notes[7], quarter_note)
    robot.sound_system.tone_maker.play_tone(notes[8], quarter_note)
    robot.sound_system.tone_maker.play_tone(notes[9], 1500)
    robot.sound_system.tone_maker.play_tone(notes[10], 1500)






