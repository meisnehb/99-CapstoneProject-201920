import rosebot
import mqtt_remote_method_calls as com
import time
import tkinter as tk
from PIL import ImageTk, Image
import shared_gui_delegate_on_robot

def main():
    frame()

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

def gui_sender():
    robot = rosebot.RoseBot()
    delegate = shared_gui_delegate_on_robot.receiver()
    mqtt_receiver = com.MqttClient(delegate)
    mqtt_receiver.connect_to_pc()

    while True:
        time.sleep(0.01)
        if delegate.is_time_to_stop:
            break

main()
