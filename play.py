import tkinter as tk
from tkinter import ttk
import moteus
import asyncio


# Motor Functions 
driveOne = moteus.Controller(id=1)
driveTwo = moteus.Controller(id=2)
async def motor_drive():
  
    with open("temp.txt", "r") as f:
        for raw in f:
            position = raw.split(",")
            print(position)
            await driveOne.set_position(position=float(position[0].strip()), velocity=0, maximum_torque=3, accel_limit=10, query=True)
            await driveTwo.set_position(position=float(position[1].strip()), velocity=0, maximum_torque=3, accel_limit=10, query=True)
            await asyncio.sleep(0.005)
        await driveOne.set_stop()
        await driveTwo.set_stop()
            
        
    

asyncio.run(motor_drive())