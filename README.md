# fiber_positioner
CODE PERTAINING TO MY WORK ON R&D FOR A "TILTING SPINE" SPECTROGRAPH FIBER POSITIONER

some essential codes were put together by Dr. Tom Diehl and Dr. Alex Drlica-Wagner, including codes to take a picture on the camera connected to the Raspberry Pi, identify the pixel coordinates of the fiber tip in the picture, communicate with the Keysight EDU33212A waveform generator, and define a circle in pixel coordinates corresponding to the fiber positioner's range of motion.
[LIST THESE CODES HERE]

since starting work on this project, I have built a series of GUIs using Tkinter to combine these codes, and incorporate my own codes, into an integrated control system for the experimental apparatus

runFinianGUI.py [single triggers + large automated consistency test] includes control panels for taking a picture, locating the fiber tip, and defining the range of motion, as well as controls for an individual trigger of the waveform generator with choices of axis (x / y), direction (+ / -), input voltage, and number of waveform cycles. in the bottom right of the GUI are controls to run a large automated test of the positioner, with choices of voltage step, maximum voltage, number of trials per voltage-direction, number of cycles for each trial, and the date (used in image and file naming).

runFinianGUI3.py [calibration + pixel-coordinate seeking algorithm] includes control panels for taking a picture, locating the fiber tip, and defining the range of motion, as well as controls to run a calibration of the system consisting of a test of 5 successive positive and negative triggers of each channel of the waveform generator, at the voltages each channel uses in the location-seeking function (go_there). the resulting file is named cal_data_[date].csv, where [date] is the text input labeled Date: in the GUI, a string of digits with no slashes. the calibration determines the angle relative to the pixel coordinates at which each channel of the waveform generator is moving the fiber, as well as the displacement in pixel coordinates per waveform cycle at the voltage being used by each channel. this information is used in the go_there function to calculate the combination of CH1 and CH2 inputs to the waveform generator required to move the fiber to the pixel coordinates input using the text boxes labeled 'X_pix:' and 'Y_pix:'. the maximum number of triggers of each channel allowed is set using a text input to the box labeled 'Max_iter:', otherwise the function will stop when the fiber tip is located within the threshold for displacement in pixel coordinates set within the function, currently at 5 pixels. 

runFinianGUI4.py [calibration + automated test of pixel-coordinate seeking algorithm]

there are uploaded example calibration data from 01/13/23 (cal_data_0113.csv, calibration_data_0113.csv, written at different points during calibrate), and example data from the automated test run using run_test in runFinianGUI.py (test_data_0113.csv)
