#!/usr/bin/env python3
"""
File:    main.py
Author:  Tauno Erik
Started: 18.05.2023
Edited:  18.05.2023
"""

import tkinter as tk
from tkinter import ttk

TXT_TITLE = "Vägi"
WIN_SIZE = "300x400"  # Default window size
PAD_SIZE = 10 # GUI padding

def cmd_teemidagi():
  print('cmd_teemidagi')
  print(entry_val.get())


def main():
  # Window
  window = tk.Tk()
  window.title(TXT_TITLE)
  window.geometry(WIN_SIZE)

  #Title
  title_label = ttk.Label(master=window, text=TXT_TITLE, font='Futura 24')
  title_label.pack()

  # Input
  input_frame = ttk.Frame(master=window)
  global entry_val
  entry_val = tk.IntVar()
  entry = ttk.Entry(master=input_frame, textvariable=entry_val)
  button = ttk.Button(master=input_frame, text='Tee midagi', command=cmd_teemidagi)
  entry.pack(side='left', padx=PAD_SIZE)
  button.pack(side='left')
  input_frame.pack(pady=PAD_SIZE)

  # Output
  output_label = ttk.Label(master=window, text='Output')
  output_label.pack()


  window.mainloop()


if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    # Exit when CTRL-C pressed
    print('Closing!')
    exit(0)