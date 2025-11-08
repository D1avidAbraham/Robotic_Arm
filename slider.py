import tkinter as tk
from tkinter import ttk
import threading
import asyncio
import math
import moteus
import time

# --- Shared state object (thread-safe-ish using simple attributes) ---
class SharedState:
    def __init__(self):
        self.position = 0.0
        self.running = True  # True means driving; False means stop motor
        self.exit_flag = False  # When True, background loop should exit

state = SharedState()

# --- Motor controller (created inside background thread / loop) ---
# We will create the moteus.Controller inside the async loop thread to avoid
# transport / socket lifetime issues on the main thread.
async def drive_loop():
    # create controller inside the asyncio thread
    drive = moteus.Controller(id=1)
    try:
        while not state.exit_flag:
            if state.running:
                # send position command; set velocity != 0 if you want motion by velocity
                # Use math.nan for position to command a velocity-only move instead
                # e.g., position=math.nan, velocity=1.0 -> continuous motion
                pos = state.position
                # Use a nonzero velocity only if you intend to move; here we command
                # a position target with velocity 0 (hold the position) — that was your original intent.
                await drive.set_position(position=pos, velocity=0, maximum_torque=3, accel_limit=2, query=True)
            else:
                # send stop command once; you can await a short sleep to avoid spamming
                await drive.set_stop()
                # after stopping, keep waiting until running becomes True or exit_flag set
            await asyncio.sleep(0.01)
    except asyncio.CancelledError:
        # Do any cleanup if needed
        pass
    finally:
        # Optionally ensure motor stopped on exit
        try:
            await drive.set_stop()
        except Exception:
            pass

# --- Thread target to run asyncio loop ---
def start_asyncio_loop_in_thread():
    # Each thread needs its own loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    task = loop.create_task(drive_loop())
    try:
        loop.run_until_complete(task)
    finally:
        loop.close()

# --- Tkinter GUI (must run on main thread) ---
root = tk.Tk()
root.title("Slider -1 to 1 by 0.1")
root.resizable(False, False)
root.geometry("360x140")

frame = ttk.Frame(root, padding=12)
frame.pack(fill="both", expand=True)

label = ttk.Label(frame, text="Move the slider")
label.pack(anchor="w")

value_var = tk.StringVar(value="0.0")
display = ttk.Label(frame, textvariable=value_var, font=("Segoe UI", 14))
display.pack(anchor="e", pady=(0, 8))

def on_change(value):
    # Update shared state so background loop reads new position
    val = round(float(value) * 10) / 10.0  # keep one decimal
    value_var.set(f"{val:.1f}")
    state.position = val

def snap_to_step(event=None):
    raw = slider.get()
    stepped = round(raw * 10) / 10.0
    slider.set(stepped)
    value_var.set(f"{stepped:.1f}")
    state.position = stepped

slider = ttk.Scale(
    frame,
    from_=-1.0,
    to=1.0,
    orient="horizontal",
    command=on_change
)
slider.pack(fill="x")
slider.bind("<ButtonRelease-1>", snap_to_step)
slider.bind("<KeyRelease>", snap_to_step)

# Buttons frame
btn_frame = ttk.Frame(frame)
btn_frame.pack(fill="x", pady=(10, 0))

def stop_button_cmd():
    # toggle running vs stopped
    state.running = False

def run_button_cmd():
    state.running = True

def quit_app():
    # signal background loop to exit and then destroy GUI
    state.exit_flag = True
    # give background thread a moment to stop (or join from main)
    # we'll destroy the GUI after a short delay
    root.after(200, root.destroy)

stop_button = ttk.Button(btn_frame, text="Stop", command=stop_button_cmd)
stop_button.pack(side="right", padx=(6,0))

run_button = ttk.Button(btn_frame, text="Run", command=run_button_cmd)
run_button.pack(side="right")

quit_button = ttk.Button(btn_frame, text="Quit", command=quit_app)
quit_button.pack(side="left")

slider.set(0.0)
value_var.set("0.0")

# --- Start background thread with asyncio loop ---
bg_thread = threading.Thread(target=start_asyncio_loop_in_thread, daemon=True)
bg_thread.start()

# Run Tk mainloop on main thread
root.mainloop()

# When GUI exits, wait a moment for background thread to finish
# (it should exit because state.exit_flag True)
time.sleep(0.2)
