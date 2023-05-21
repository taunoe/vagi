#!/usr/bin/env python3
"""
File:    main.py
Author:  Tauno Erik
Started: 18.05.2023
Edited:  21.05.2023

pip install ttkbootstrap matplotlib pyserial

"""

import tkinter as tk
import ttkbootstrap as ttk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import sys
import numpy as np
import serial
import serial.tools.list_ports
import io


def scan_ports():
    """Returns a list of avable serial ports"""
    ports = list(serial.tools.list_ports.comports())
    avaible_ports = []
    for port in ports:
        #print(port[0]) # /dev/ttyACM0
        #print(port[1]) # USB2.0-Serial
        #print(port[2]) # USB VID:PID=2341:0043
                        # SER=9563430343235150C281
                        # LOCATION=1-1.4.4:1.0
        avaible_ports.append(port[0]) # add devices to list
    return avaible_ports


def set_baud(midagi):
    print(f"Set Baud {selected_baud.get()}")


def set_plot_size():
    print(f"Plot size {selected_plot_size.get()}")

def open_serial_port():
    print(f"Selected baud {selected_baud.get()}")
    print(f"Selected port{selected_port.get()}")
    ser = serial.Serial()
    ser.baudrate = selected_baud.get()
    ser.port = selected_port.get()
    ser.open()
    if ser.is_open:
        print(f"Serial {ser.name} is open")

def save_log_file():
    print("save_log_file()")
    if is_save_log.get():
        print("true")
    else:
        print("false")

def exit_qui():
    window.destroy()
    sys.exit()

ports = scan_ports() #['esimene', 'teine', 'kolmas']
bauds = [1200,1800,2400,4800,9600,19200,28800,38400,57600,76800,115200,230400,460800,576000,921600]

data1 = [0,1,2,3,4,5,1,5,4,3,2,1,0]
time1 = [0,1,2,3,4,5,6,7,8,9,10,11,12]

## matplot theme colors
plt.rcParams["axes.prop_cycle"] = plt.cycler(
  color=["#4C2A85",
         "#957DAD",
         "#5E366E",
         "#A98CCC"]
)

TXT_TITLE = "Vägi"
WIN_SIZE = "900x700"  # Default window size
PAD_SIZE = 10 # GUI padding


# Window theme
# 'journal' - light, red button
# 'darkly' - dark, blue button
window = ttk.Window(themename='darkly')
window.title(TXT_TITLE)
window.geometry(WIN_SIZE)  # Window start size

# Menu
menu = tk.Menu(master=window)
file_menu = tk.Menu(master=menu, tearoff=False)

menu.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='Settings', command=lambda: print('Settings'))
midagi_string = tk.StringVar()
file_menu.add_checkbutton(label='Midagi', onvalue='on', offvalue='off', variable=midagi_string)
file_menu.add_separator()
file_menu.add_command(label='Exit', command=exit_qui)

window.configure(menu=menu)

# menu button
menu_button = ttk.Menubutton(window, text='Menu Btn')
menu_button.pack()

button_sub_menu = tk.Menu(menu_button, tearoff=False)
button_sub_menu.add_command(label='Esimene', command=lambda:print('esimene'))
menu_button.configure(menu = button_sub_menu)

# Left Side Frame
left_side_frame = ttk.Frame(master=window)
left_side_frame.pack(side="left", fill="y")

# Sellect Port Title
select_port_label = ttk.Label(master=left_side_frame, text="Select Port:", font='Futura 12')
select_port_label.pack()

# Sellect Port Combobox
selected_port = tk.StringVar(value = ports[0])
select_port = ttk.Combobox(master=left_side_frame, textvariable=selected_port)
select_port['values'] = ports
select_port.pack()

# Sellect Baud Title
select_baud_label = ttk.Label(master=left_side_frame, text="Baud Rate:", font='Futura 12')
select_baud_label.pack()

# Sellect Baud Combobox
selected_baud = tk.StringVar(value = bauds[10])
select_baud = ttk.Combobox(master=left_side_frame, textvariable=selected_baud)
select_baud['values'] = bauds
select_baud.pack()

# Select Baud event
select_baud.bind('<<ComboboxSelected>>', set_baud) #(event, function)

# Blot size
select_blot_size_label = ttk.Label(master=left_side_frame, text="Plot size:", font='Futura 12')
select_blot_size_label.pack()

selected_plot_size = tk.IntVar(value=100)
select_blot_size = ttk.Spinbox(
    master=left_side_frame, 
    from_=10, 
    to=400, 
    increment=1, 
    command=set_plot_size,
    textvariable=selected_plot_size)
#select_blot_size.bind('<<Increment>>', func)
#select_blot_size.bind('<<Decrement>>', func)
select_blot_size.pack()

# Checkbox save log
# Blot size
save_log_label = ttk.Label(master=left_side_frame, text="Save", font='Futura 12')
save_log_label.pack()
is_save_log = tk.IntVar(value=0)
save_log = ttk.Checkbutton(master=left_side_frame, text="Log", variable=is_save_log, command=save_log_file)
save_log.pack()

# Button connect/ open serial
button_connect = ttk.Button(master=left_side_frame, text="Connect", command=open_serial_port)
button_connect.pack(side=ttk.BOTTOM)

# Button QUIT
#button_quit = ttk.Button(master=left_side_frame, text="Quit", command=window.destroy)
#button_quit.pack(side=ttk.BOTTOM)



# Plots Area
plots_area = ttk.Frame(master=window)
plots_area.pack()

# Line chart
fig1, ax1 = plt.subplots()
ax1.plot(time1, data1)
ax1.set_title("Plot 1")
ax1.set_xlabel("Time")
ax1.set_ylabel("Value")
#plt.show()

# Area chart
fig2, ax2 = plt.subplots()
ax2.fill_between(time1, data1)
ax2.set_title("Plot 2")
ax2.set_xlabel("Time")
ax2.set_ylabel("Value")
#plt.show()

# Upper plot
upper_frame = ttk.Frame(master=plots_area)
upper_frame.pack(fill="both", expand=True)

canvas1 = FigureCanvasTkAgg(fig1, upper_frame)
canvas1.draw()
canvas1.get_tk_widget().pack(side="left", fill="both", expand=True)

# Middel plot
middle_frame = ttk.Frame(master=plots_area)
middle_frame.pack(fill="both", expand=True)

canvas2 = FigureCanvasTkAgg(fig2, middle_frame)
canvas2.draw()
canvas2.get_tk_widget().pack(side="left", fill="both", expand=True)




window.mainloop()
sys.exit()
