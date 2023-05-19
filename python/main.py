#!/usr/bin/env python3
"""
File:    main.py
Author:  Tauno Erik
Started: 18.05.2023
Edited:  19.05.2023

pip install ttkbootstrap
"""

import tkinter as tk
#from tkinter import ttk
import ttkbootstrap as ttk  # pip install ttkbootstrap

TXT_TITLE = "Vägi"
WIN_SIZE = "300x400"  # Default window size
PAD_SIZE = 10 # GUI padding


def cmd_teemidagi():
  input_var = entry_val.get()
  output_string.set(f'Tehtud {input_var}')


# Window theme
# 'journal' - light, red button
# 'darkly' - dark, blue button
window = ttk.Window(themename='darkly')
window.title(TXT_TITLE)
window.geometry(WIN_SIZE)  # Window start size

#Title
title_label = ttk.Label(master=window, text=TXT_TITLE, font='Futura 24')
title_label.pack()

# Input
input_frame = ttk.Frame(master=window)
entry_val = tk.IntVar()
entry = ttk.Entry(master=input_frame, textvariable=entry_val)
button = ttk.Button(master=input_frame, text='Tee midagi', command=cmd_teemidagi)
entry.pack(side='left', padx=PAD_SIZE)
button.pack(side='left')
input_frame.pack(pady=PAD_SIZE)

# Output
global output_string
output_string = tk.StringVar()
output_label = ttk.Label(master=window, text='Output', textvariable=output_string)
output_label.pack(pady=PAD_SIZE)


window.mainloop()
