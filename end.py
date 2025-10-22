#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import subprocess

MONITOR_NAME = "eDP-1-1"

def load_icon(path, size):
    img = Image.open(path)
    img = img.resize(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)

def set_gamma_rgb(r, g, b):
    cmd = f"xrandr --output {MONITOR_NAME} --gamma {r}:{g}:{b}"
    subprocess.run(cmd, shell=True)

def set_gamma_uniform(val):
    cmd = f"xrandr --output {MONITOR_NAME} --gamma {val}:{val}:{val}"
    subprocess.run(cmd, shell=True)

def round_to_step(val, step=0.1):
    return round(float(val) / step) * step

def update_rgb(val=None):
    r = round_to_step(red_var.get())
    g = round_to_step(green_var.get())
    b = round_to_step(blue_var.get())
    red_var.set(r)
    green_var.set(g)
    blue_var.set(b)
    set_gamma_rgb(r, g, b)
    label_red.config(text=f"Red: {r:.1f}")
    label_green.config(text=f"Green: {g:.1f}")
    label_blue.config(text=f"Blue: {b:.1f}")

def update_uniform(val=None):
    val = round_to_step(uniform_var.get())
    uniform_var.set(val)
    set_gamma_uniform(val)
    label_uniform.config(text=f"Uniform Gamma: {val:.1f}")

def reset_all():
    red_var.set(1.0)
    green_var.set(1.0)
    blue_var.set(1.0)
    uniform_var.set(1.0)
    update_rgb()
    update_uniform()

def animate_k7(frame_idx=0):
    k7_label.config(image=k7_frames[frame_idx])
    root.after(100, animate_k7, (frame_idx + 1) % len(k7_frames))

root = tk.Tk()
root.title("Gamma Control")

frame = ttk.Frame(root, padding=20)
frame.grid(row=0, column=0, sticky="nsew")

# Carica icone statiche
lampadina_icon = load_icon("lampadina.png", size=(64, 64))
monitor_icon = load_icon("monitor.png", size=(64, 64))

# Carica GIF animata k7.gif
k7_gif = Image.open("k7.gif")
k7_frames = []
try:
    while True:
        frame_img = k7_gif.copy().resize((72, 72), Image.Resampling.LANCZOS)
        k7_frames.append(ImageTk.PhotoImage(frame_img))
        k7_gif.seek(len(k7_frames))  # passa al frame successivo
except EOFError:
    pass

# Variabili
red_var = tk.DoubleVar(value=1.0)
green_var = tk.DoubleVar(value=1.0)
blue_var = tk.DoubleVar(value=1.0)
uniform_var = tk.DoubleVar(value=1.0)

# Monitor icon
icon_label_monitor = ttk.Label(frame, image=monitor_icon)
icon_label_monitor.grid(row=0, column=0, rowspan=3, sticky="n", padx=(0, 15), pady=10)

label_red = ttk.Label(frame, text="Red: 1.0")
label_red.grid(row=0, column=1, sticky="w", pady=10)
tk.Scale(frame, from_=0.1, to=3.0, variable=red_var, orient=tk.HORIZONTAL,
         command=update_rgb, length=400, sliderlength=30, width=30, resolution=0.1).grid(row=0, column=2, sticky="ew", pady=10)

label_green = ttk.Label(frame, text="Green: 1.0")
label_green.grid(row=1, column=1, sticky="w", pady=10)
tk.Scale(frame, from_=0.1, to=3.0, variable=green_var, orient=tk.HORIZONTAL,
         command=update_rgb, length=400, sliderlength=30, width=30, resolution=0.1).grid(row=1, column=2, sticky="ew", pady=10)

label_blue = ttk.Label(frame, text="Blue: 1.0")
label_blue.grid(row=2, column=1, sticky="w", pady=10)
tk.Scale(frame, from_=0.1, to=3.0, variable=blue_var, orient=tk.HORIZONTAL,
         command=update_rgb, length=400, sliderlength=30, width=30, resolution=0.1).grid(row=2, column=2, sticky="ew", pady=10)

# Lampadina
icon_label_lampadina = ttk.Label(frame, image=lampadina_icon)
icon_label_lampadina.grid(row=3, column=0, sticky="n", padx=(0, 15), pady=10)

label_uniform = ttk.Label(frame, text="Uniform Gamma: 1.0")
label_uniform.grid(row=3, column=1, sticky="w", pady=10)
tk.Scale(frame, from_=0.1, to=3.0, variable=uniform_var, orient=tk.HORIZONTAL,
         command=update_uniform, length=400, sliderlength=30, width=30, resolution=0.1).grid(row=3, column=2, sticky="ew", pady=10)

# Reset button
ttk.Button(frame, text="Reset", command=reset_all).grid(row=4, column=0, columnspan=3, pady=20)

# K7 GIF animata in basso a destra
k7_label = ttk.Label(frame)
k7_label.grid(row=5, column=2, sticky="se", padx=(0, 10), pady=(10, 0))

# Configura layout
frame.columnconfigure(2, weight=1)
frame.rowconfigure(5, weight=1)

# Avvia animazione
if k7_frames:
    animate_k7()

root.mainloop()

