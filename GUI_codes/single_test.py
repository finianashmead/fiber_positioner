def single_test():
  
    ##WILL NOW NEED SOME IMPORTS:
    import pyvisa as visa
    import argparse
    import time
    import sys
    import tkinter
    from tkinter import messagebox
    from importlib import *
    from functools import partial

    ##from simpleprint import *
    import setRPclock2
    import DoPhotoCopy2
    import imageme
    import get_tip_pos
    #import finian_keysight_trigger
    import finian_keysight_trigger_poltest
    import numpy as np
    #import csv
    import pandas as pd
    import statistics
    import argparse
    import cv2
    import time
    import os
    
    ## THIS IS WHERE I'M GOING TO MAKE A FUNCTION TO DO ALL OF THESE THINGS
    ## INPUT VARIABLES: v, axis, d, steps, date, i, 
    ## OUTPUTS: 
    
    ## get inputs from text boxes
    trials = float(test_txt1.get())
    v_step=float(test_txt2.get())
    v_max=float(test_txt3.get())
    steps=int(test_txt4.get())
    date=str(test_txt5.get())
    print("args: ", " trials: ", trials, " v_step: ", v_step, " v_max: ", v_max, " steps: ", steps)
    v_min = 1.0 - v_step  #0.0 + v_step
    v_stop = v_max + v_step
    
    ##reset lists to proper values
    xlistpoints.clear()
    ylistpoints.clear()
    v_inputs.clear()
    axis_inputs.clear()
    dir_inputs.clear()
    steps_inputs.clear()
    v_inputs.append(0.0)
    axis_inputs.append(0.0)
    dir_inputs.append(0.0)
    steps_inputs.append(0.0)
    
    ##take baseline image:
    # take photo
    imagename = "test_img_start" + date
    DoPhotoCopy2.takePhotoAndCopy(x,imagename)
    imagename=imagename+".jpg"
    ##FINIAN: adding if/else switch to take picture again if the first time failed
    while os.path.exists(imagename) == False:
        imagename = "test_img_start" + date
        DoPhotoCopy2.takePhotoAndCopy(x,imagename)
        imagename=imagename+".jpg"
    else:
        print("IMAGE TAKEN")
    #imageme.displaylast(x,imagename)
    #result=imagename
    # find tip
    print('disp: IMAGENAME: ',imagename)
    pos = get_tip_pos.gettippos(x, imagename)
    xi = pos[0]
    yi = pos[1]
    xlistpoints.append(xi)
    ylistpoints.append(yi)
    print("XLISTPOINTS: ", xlistpoints)
    print("YLISTPOINTS: ", ylistpoints)
    
    ## while loop based on uncert
    v = v_min
    axis = 2
    while v < v_stop:
        i = 0
        while i < trials:
          
            ## THIS IS WHERE I'M GOING TO MAKE A FUNCTION TO DO ALL OF THESE THINGS
        
            ## taken from trigger_keysight
            # MOVE POS DIRECTION
            d='pos'
            v = round(v, 3)
            print("args", v, axis, d, steps)
            v_inputs.append(v)
            axis_inputs.append(axis)
            dir_inputs.append(d)
            steps_inputs.append(steps)
            print("V INPUTS: ", v_inputs)
            print("AXIS INPUTS: ", axis_inputs)
            print("DIR. INPUTS: ", dir_inputs)
            print("STEPS INPUTS: ", steps_inputs)
            finian_keysight_trigger_poltest.trigger_keysight(v, axis, d, steps)
            ## TIME DELAY WHILE SPINE MOVES
            print("TIME BEFORE: ", time.ctime())
            time.sleep(15)
            print("TIME AFTER: ", time.ctime())
            # take photo
            vlabeld = str(v)
            vlabel = vlabeld.replace(".", "p")
            print("VLABEL: ", vlabel)
            imagename = "test_img" + str(vlabel) + "i" + str(i) + str(axis) + str(d) + date
            DoPhotoCopy2.takePhotoAndCopy(x,imagename)
            imagename=imagename+".jpg"
            while os.path.exists(imagename) == False:
                imagename = "test_img" + str(vlabel) + "i" + str(i) + str(axis) + str(d) + date
                DoPhotoCopy2.takePhotoAndCopy(x,imagename)
                imagename=imagename+".jpg"
            else:
                print("IMAGE TAKEN!")            
            #imageme.displaylast(x,imagename)
            #result=imagename
            # find tip
            
            
            ## THIS PART MIGHT NEED TO BE OUTSIDE OF THE FUNCTION
            print('disp: IMAGENAME: ',imagename)
            pos = get_tip_pos.gettippos(x, imagename)
            xi = pos[0]
            yi = pos[1]
            xlistpoints.append(xi)
            ylistpoints.append(yi)
            print("XLISTPOINTS: ", xlistpoints)
            print("YLISTPOINTS: ", ylistpoints)
            imgc = 'ana-' + imagename #might not want to dispay
            #imageme.displaylast(x, imgc)
            
            # REPEAT IN NEG DIRECTION
            d='neg'
            print("args", v, axis, d, steps)
            v_inputs.append(v)
            axis_inputs.append(axis)
            dir_inputs.append(d)
            steps_inputs.append(steps)
            print("V INPUTS: ", v_inputs)
            print("AXIS INPUTS: ", axis_inputs)
            print("DIR. INPUTS: ", dir_inputs)
            print("STEPS INPUTS: ", steps_inputs)
            finian_keysight_trigger_poltest.trigger_keysight(v, axis, d, steps)
            ## TIME DELAY WHILE SPINE MOVES
            print("TIME BEFORE: ", time.ctime())
            time.sleep(15)
            print("TIME AFTER: ", time.ctime())
            # take photo
            vlabeld = str(v)
            vlabel = vlabeld.replace(".", "p")
            print("VLABEL: ", vlabel)
            imagename = "test_img" + str(vlabel) + "i" + str(i) + str(axis) + str(d) + date
            DoPhotoCopy2.takePhotoAndCopy(x,imagename)
            imagename=imagename+".jpg"
            while os.path.exists(imagename) == False:
                imagename = "test_img" + str(vlabel) + "i" + str(i) + str(axis) + str(d) + date
                DoPhotoCopy2.takePhotoAndCopy(x,imagename)
                imagename=imagename+".jpg"
            else:
                print("IMAGE TAKEN!")           
            #imageme.displaylast(x,imagename)
            #result=imagename
            # find tip
            print('disp: IMAGENAME: ',imagename)
            pos = get_tip_pos.gettippos(x, imagename)
            xi = pos[0]
            yi = pos[1]
            xlistpoints.append(xi)
            ylistpoints.append(yi)
            print("XLISTPOINTS: ", xlistpoints)
            print("YLISTPOINTS: ", ylistpoints)
            imgc = 'ana-' + imagename #might not want to dispay
            #imageme.displaylast(x, imgc)
            print("TRIAL " + str(i) + " DONE")
            i += 1
        
        v += round(v_step, 3)
    
    ## write data to csv
    df = pd.DataFrame(list(zip(*[xlistpoints, ylistpoints, v_inputs, axis_inputs, dir_inputs, steps_inputs]))).add_prefix('Col')
    df.columns = ['X_pix', 'Y_pix', 'V_input', 'Ax_input', 'Dir_input', 'Steps_input']
    print("DF: ", df)
    ### MIGHT WANT TO ADD TEXT BOX TO DEFINE CSV NAME AT A LATER STATE
    df.to_csv('test_data', index=False)
