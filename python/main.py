#!/usr/bin/env python3
"""
File:    main.py
Author:  Tauno Erik
Started: 18.05.2023
Edited:  20.05.2023

pip install ttkbootstrap matplotlib

"""

import tkinter as tk
import ttkbootstrap as ttk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np

ports = ['esimene', 'teine', 'kolmas']
bauds = [1200,1800,2400,4800,9600,19200,28800,38400,57600,76800,115200,230400,460800,576000,921600]

data1 = [0,1,2,3,4,5,1,5,4,3,2,1,0]
time1 = [0,1,2,3,4,5,6,7,8,9,10,11,12]

## matplot theme colors
plt.rcParams["axes.prop_cycle"] = plt.cycler(
  color=["#4C2A85",
         "#BE96FF",
         "#957DAD",
         "#5E366E",
         "#A98CCC"]
)

TXT_TITLE = "Vägi"
WIN_SIZE = "900x700"  # Default window size
PAD_SIZE = 10 # GUI padding


def set_baud(midagi):
    print(f"Set Baud {selected_baud.get()}")

def set_plot_size():
    print(f"Plot size {selected_plot_size.get()}")


# Window theme
# 'journal' - light, red button
# 'darkly' - dark, blue button
window = ttk.Window(themename='darkly')
window.title(TXT_TITLE)
window.geometry(WIN_SIZE)  # Window start size


# Left Side Frame
left_side_frame = ttk.Frame(master=window)
left_side_frame.pack(side="left", fill="y")

# Sellect Port Title
select_port_label = ttk.Label(master=left_side_frame, text="Select Port:", font='Futura 12')
select_port_label.pack()

# Sellect Port Combobox
default_port = tk.StringVar(value = ports[0])
select_port = ttk.Combobox(master=left_side_frame, textvariable=default_port)
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

# Button QUIT
button_quit = ttk.Button(master=left_side_frame, text="Quit", command=window.destroy)
button_quit.pack(side=ttk.BOTTOM)

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
