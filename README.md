# fiber_positioner
CODE PERTAINING TO MY WORK ON R&D FOR A SPECTROGRAPH FIBER POSITIONER

some essential codes were put together by Dr. Tom Diehl and Dr. Alex Drlica-Wagner, including codes to take a picture on the camera connected to the Raspberry Pi, identify the pixel coordinates of the fiber tip in the picture, communicate with the Keysight EDU33212A waveform generator, and define a circle in pixel coordinates corresponding to the fiber positioner's range of motion.
[LIST THESE CODES HERE]

since starting work on this project, I have built a series of GUIs using Tkinter to combine these codes, and incorporate my own codes, into an integrated control system for the experimental apparatus

the first GUI (runFinianGUI.py) includes control panels for taking a picture, locating the fiber tip, and defining the range of motion, as well as controls for an individual trigger of the waveform generator with choices of axis (x / y), direction (+ / -), input voltage, and number of waveform cycles. in the bottom right of the GUI are controls to run a large automated test of the positioner, with choices of voltage step, maximum voltage, number of trials per voltage-direction, number of cycles for each trial, and the date (used in image and file naming).
[LIST AND EXPLAIN THE DIFFERENT GUIS]
