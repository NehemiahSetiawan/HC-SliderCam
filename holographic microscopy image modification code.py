#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 10:05:17 2024

@author: dianaceron
"""
import cv2  
import time
import numpy as np
import tkinter as tk
import reco
import sys

Z = 0
recording = False
video = None
Z_SCALE = 1e-6
started = False
cropping = 0
croprec = False
photo = False
MIN_EXPOSURE = -13
imagedir = r'C:\Users\Noami Budi\Downloads\Holo2-main\Holo2-main\rawImage/'
recodir = r'C:\Users\Noami Budi\Downloads\Holo2-main\Holo2-main\recoImage/'

def nothing(x):
    pass

def Exposure(x):
    global exposure
    exposure = MIN_EXPOSURE + x
    cap.set(cv2.CAP_PROP_EXPOSURE, exposure)

def Brightness(x):
    global brightness
    brightness = x
    cap.set(cv2.CAP_PROP_BRIGHTNESS, brightness)

def Contrast(x):
    global contrast
    contrast = x
    cap.set(cv2.CAP_PROP_CONTRAST, contrast)

def Saturation(x):
    global saturation
    saturation = x
    cap.set(cv2.CAP_PROP_SATURATION, saturation)

def Gain(x):
    global gain
    gain = x
    cap.set(cv2.CAP_PROP_GAIN, gain)

def Zf(x):
    global Z
    Z = x

def Cropping(x):
    global cropping
    cropping = x

def Record(x):
    global recording, video, w, h, vname, master, croprec, photo, Z, imagedir
    if x == 1:
        master = tk.Tk()
        master.geometry("340x270")

        f = tk.Label(master, text="Enter video name", font=("Arial", 16), height=1, width=16)
        f.pack()

        e = tk.Entry(master, width=20, font=("Arial", 16))
        e.pack()
        e.focus_set()

        def callback(*args):
            global vname, croprec, photo
            croprec = False
            photo = False
            vname = e.get()
            master.destroy()

        b = tk.Button(master, text="OK", font=("Arial", 12), width=20, command=callback)
        b.pack()

        master.protocol('WM_DELETE_WINDOW', lambda: master.destroy())
        master.bind("<Return>", callback)

        tk.mainloop()

        if vname != 'cancel':
            vid = r'C:\Users\Noami Budi\Downloads\Holo2-main\Holo2-main\rawVideo/' + vname + '.mp4'
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            video = cv2.VideoWriter(vid, fourcc, 20.0, (int(w), int(h)), 0)
            cv2.imshow("Controls", cv2.imread("recording.png"))
            recording = True
    else:
        if video is not None:
            recording = False
            video.release()
            video = None
            cv2.imshow("Controls", cv2.imread("off.png"))

def Crop(event, x, y, flags, param):
    global cropping, cwindow, ix, iy
    if cropping:
        x = int(x)
        y = int(y)
        x = np.clip(x, 0, w)
        y = np.clip(y, 0, h)
        if event == cv2.EVENT_LBUTTONDOWN:
            iy = int(y)
            ix = int(x)
        elif event == cv2.EVENT_LBUTTONUP and iy is not None and ix is not None:
            cwindow[0], cwindow[1] = sorted([iy, y])
            cwindow[2], cwindow[3] = sorted([ix, x])

# Initialize camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    sys.exit()

# Set camera resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 326400)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 244800)
w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print("Frame default resolution:", w, h)

# Create control windows
cv2.namedWindow("Controls")
cv2.namedWindow("Camera")
cv2.createTrackbar("Exposure", "Controls", -MIN_EXPOSURE, -MIN_EXPOSURE, Exposure)
cv2.createTrackbar("Brightness", "Controls", 128, 255, Brightness)
cv2.createTrackbar("Contrast", "Controls", 32, 100, Contrast)
cv2.createTrackbar("Saturation", "Controls", 64, 100, Saturation)
cv2.createTrackbar("Gain", "Controls", 0, 100, Gain)
cv2.createTrackbar("Z value", "Controls", 0, 40000, Zf)
cv2.createTrackbar("Record", "Controls", 0, 1, Record)
cv2.createTrackbar("Crop", "Controls", 0, 1, Cropping)

cwindow = [0, 100, 0, 100]

cv2.setMouseCallback('Camera', Crop)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cropframe = frame[cwindow[0]:cwindow[1], cwindow[2]:cwindow[3]]

    if recording:
        video.write(cropframe if croprec else frame)

    cv2.imshow('Camera', frame)
    cv2.imshow('Crop', cropframe)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release everything
cap.release()
if recording:
    video.release()
cv2.destroyAllWindows()
print('bye')
