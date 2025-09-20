import tkinter as tk
from tkinter import ttk
import argparse
import asyncio
import math
import moteus
import time
import threading



# Title of the window
root = tk.Tk()
root.title("Move")
root.geometry("240x240")


#Variables of the GUI
position = tk.DoubleVar(value=0.0)
velocity = tk.DoubleVar(value=0.5)
torque = tk.DoubleVar(value=2.0)
v_limit = tk.DoubleVar(value=3.0)
a_limit = tk.DoubleVar(value=15)



# Motor Functions 
drive = moteus.Controller(id=1)

async def motor_drive():
    # While Position is not reached move
  
    while True:
        # Move the motor
        result = await drive.set_position( position=float(position.get()), velocity=float(velocity.get()), maximum_torque=float(torque.get()), velocity_limit=float(v_limit.get()), accel_limit=float(a_limit.get()), query=True)
        # get the current position 
        positionNew = result.values[moteus.Register.POSITION]
      
        if result and abs(positionNew - position.get()) < 0.02:
            print("Completed")
            # Do this to stop the motor from running
            result = await drive.set_position( position=float(position.get()), velocity=0.0, maximum_torque=float(torque.get()), velocity_limit=float(v_limit.get()), accel_limit=float(a_limit.get()), query=True)
            break
    
# Disable the motor 
async def stop():
    result = await drive.set_stop()
    print("stop")


# GUI Functions

def gui_stop():
    asyncio.run(stop())

def gui_drive():
    asyncio.run(motor_drive())



#Layout of the window
# 5 X 3 
# Rows 
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.rowconfigure(3, weight=1)
root.rowconfigure(4, weight=1)
# Colums 
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)

# Position
position_label = ttk.Label(root, text="Position:")
position_label.grid(column=0, row=0, sticky=tk.EW, padx=2, pady=0)

position_entry = ttk.Entry(root, textvariable=position)
position_entry.grid(column=1, row=0, sticky=tk.EW, padx=2, pady=0, )

# Velocity 
velocity_lable = ttk.Label(root, text="Velocity:")
velocity_lable.grid(column=0, row=1, sticky=tk.EW, padx=2, pady=0)

velocity_entry = ttk.Entry(root, textvariable=velocity)
velocity_entry.grid(column=1, row=1, sticky=tk.EW, padx=2, pady=0)


# Torque 
torque_lable = ttk.Label(root, text="Torque:")
torque_lable.grid(column=0, row=2, sticky=tk.EW, padx=2, pady=0)

torque_entry = ttk.Entry(root, textvariable=torque)
torque_entry.grid(column=1, row=2, sticky=tk.EW, padx=2, pady=0)


# V Limit 
v_limit_lable = ttk.Label(root, text="V Limit:")
v_limit_lable.grid(column=0, row=3, sticky=tk.EW, padx=2, pady=0)

v_limit_entry = ttk.Entry(root, textvariable=v_limit)
v_limit_entry.grid(column=1, row=3, sticky=tk.EW, padx=2, pady=0)

# A Limit
a_limit_lable = ttk.Label(root, text="A Limit:")
a_limit_lable.grid(column=0, row=4, sticky=tk.EW, padx=2, pady=0)

a_limit_entry = ttk.Entry(root, textvariable=a_limit)
a_limit_entry.grid(column=1, row=4, sticky=tk.EW, padx=2, pady=0)

# Stop Button 
stop_button = ttk.Button(root, text="Stop", command=gui_stop)
stop_button.grid(column=2, row=2, sticky=tk.EW, padx=2, pady=0)

# Start Button 
start_button = ttk.Button(root, text="Start", command=gui_drive)
start_button.grid(column=2, row=3, sticky=tk.EW, padx=2, pady=0)


root.mainloop()
