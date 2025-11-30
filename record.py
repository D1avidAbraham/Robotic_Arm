import tkinter as tk
from tkinter import ttk
import moteus
import asyncio


# Motor Functions 
driveOne = moteus.Controller(id=1)
driveTwo = moteus.Controller(id=2)
async def motor_drive():
    time = 0 
    with open("temp.txt", "w") as f:
        while time != 5000:

            result = await driveOne.query()
            resultTwo = await driveTwo.query()
            position = result.values[moteus.Register.POSITION]
            positionTwo = resultTwo.values[moteus.Register.POSITION]
            print("Position:", position)
            print("Position 2:", positionTwo)
            f.write(str(position) + "," + str(positionTwo) + "\n")
            await asyncio.sleep(0.005)
            print(time)
            time += 1
        
    

asyncio.run(motor_drive())