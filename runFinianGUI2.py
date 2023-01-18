import sys
import tkinter
from tkinter import messagebox
from importlib import *
from functools import partial

##from simpleprint import *
import setRPclock2
import DoPhotoCopy2
import imageme
import imagemeF
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
import matplotlib.pyplot as plt

top = tkinter.Tk()
top.title("Tilting Spine Operating Functions")
top.geometry('500x300')


txt = tkinter.Entry(top, width=15)
txt.grid(row=2,column=1)

## calibration inputs
#trig_txt1 = tkinter.Entry(top, width=10)
#trig_txt1.grid(row=9,column=1)
#trig_txt2 = tkinter.Entry(top, width=10)
#trig_txt2.grid(row=10,column=1)
#trig_txt3 = tkinter.Entry(top, width=10)
#trig_txt3.grid(row=11,column=1)
#trig_txt4 = tkinter.Entry(top, width=10)
#trig_txt4.grid(row=12,column=1)

## run_test inputs
test_txt1 = tkinter.Entry(top, width=10)
test_txt1.grid(row=9,column=3)
test_txt2 = tkinter.Entry(top, width=10)
test_txt2.grid(row=10,column=3)
test_txt3 = tkinter.Entry(top, width=10)
test_txt3.grid(row=11,column=3)

date_txt = tkinter.Entry(top, width=10)
date_txt.grid(row=9,column=1)

# text input for calc_uncertainty (unfinished)
N_txt = tkinter.Entry(top, width=10)
N_txt.grid(row= 7, column=1)

#def helloCallBack():
#   messagebox.showinfo( "Hello Python", "Hello World")

xlistpoints = []
ylistpoints = []
v_inputs = [0]
axis_inputs =[0]
dir_inputs = [0]
steps_inputs = [0]

theta1 = []
theta2 = []
move1 = []
move2 = []

slope1 = []
slope2 = []

def dophotoscp():
    imagename = str(txt.get())
    print("IMAGENAME", imagename)
    if len(imagename) == 0:
        imagename = "TodaysImage"
    print(imagename,x,"heredpscp")
    DoPhotoCopy2.takePhotoAndCopy(x,imagename)
    imagename=imagename+".jpg"
    #print('just before ',imagename)
    imageme.displaylast(x,imagename)
    #print(imagename,"just before")
    result=imagename


def testerCallBack():
## tester(x)
    setRPclock2.setRPclockTime(x)

def displaylast():
    imagename = str(txt.get())
    imagename=imagename+".jpg"
    print('disp: IMAGENAME: ',imagename)
    imageme.displaylast(x,imagename)
   
def get_tip():
    imagename = str(txt.get())
    imagename=imagename+".jpg"
    print('disp: IMAGENAME: ',imagename)
    pos = get_tip_pos.gettippos(x, imagename)
    xi = pos[0]
    yi = pos[1]
    xlistpoints.append(xi)
    ylistpoints.append(yi)
    print("XLISTPOINTS: ", xlistpoints)
    print("YLISTPOINTS: ", ylistpoints)
    imgc = 'ana-' + imagename
    imageme.displaylast(x, imgc)
 
## TAKEN FROM TKFUN, MIGHT NEED TO CHANGE SOMEWHAT
def circlefit():
    from fit2circle import calc_R, f_2, fitmycircle

    if len(xlistpoints) > 2:
        control = '__main__'
        print('XLISTPOINTS', xlistpoints)
        print('YLISTPOINTS', ylistpoints)
        circlecenterx, circlecentery, circleR, chi2 = fitmycircle(control,xlistpoints,ylistpoints)
        print("fitresult ",circlecenterx, circlecentery, circleR, chi2)
       
        ## CODE FOR DRAWING CIRCLE ON COPY IMAGE
        imagename = str(txt.get())
        imagename=imagename+".jpg"
        print('disp: IMAGENAME: ',imagename)
        pos = get_tip_pos.gettippos(x, imagename)
        image = cv2.imread(imagename)
        output = image.copy()
       
        cx = int(circlecenterx)
        cy = int(circlecentery)
        cr = int(circleR)
        print('CIRCLE X, Y, R: ', cx, cy, cr)
       
        # draw the circle in the output image, then draw a rectangle corresponding to the center of the circle
        cv2.circle(output, (cx, cy), cr, (0, 255, 0), 8)
        cv2.rectangle(output, (cx - 5, cy - 5), (cx + 5, cy + 5), (0, 128, 255), -1)
        cv2.imwrite('fit-'+imagename,output) # store the output image
       
        imgf = 'fit-' + imagename
        imageme.displaylast(x, imgf)

    else:
        print("need more data")
        print("XLISTPOINTS: ", xlistpoints)
        print("YLISTPOINTS: ", ylistpoints)
       
def reset_data_lists():
    print("XLISTPOINTS: ", xlistpoints)
    print("YLISTPOINTS: ", ylistpoints)
    print("V INPUTS: ", v_inputs)
    print("AXIS INPUTS: ", axis_inputs)
    print("DIR. INPUTS: ", dir_inputs)
    print("STEPS INPUTS: ", steps_inputs)
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
    print("XLISTPOINTS: ", xlistpoints)
    print("YLISTPOINTS: ", ylistpoints)
    print("V INPUTS: ", v_inputs)
    print("AXIS INPUTS: ", axis_inputs)
    print("DIR. INPUTS: ", dir_inputs)
    print("STEPS INPUTS: ", steps_inputs)


def trigger_keysight():
    v = float(trig_txt1.get())
    axis=int(trig_txt2.get())
    d=str(trig_txt3.get())
    steps=int(trig_txt4.get())
    print("args", v, axis, d, steps)
    v_inputs.append(v)
    axis_inputs.append(axis)
    dir_inputs.append(d)
    steps_inputs.append(steps)
    print("V INPUTS: ", v_inputs)
    print("AXIS INPUTS: ", axis_inputs)
    print("DIR. INPUTS: ", dir_inputs)
    print("STEPS INPUTS: ", steps_inputs)
    #print("args", axis, d, steps)
    #finian_keysight_trigger.trigger_keysight(v, axis, d, steps)
    finian_keysight_trigger_poltest.trigger_keysight(v, axis, d, steps)
   
def calc_uncertainty():
    xlistpoints.clear()
    ylistpoints.clear()
    N = int(N_txt.get())
    i=0
    while i < N:
        #take photo
        imagename = "unc_img" + str(i)
        DoPhotoCopy2.takePhotoAndCopy(x,imagename)
        imagename=imagename+".jpg"
        #imageme.displaylast(x,imagename)
        #result=imagename
        #find tip
        print('disp: IMAGENAME: ',imagename)
        pos = get_tip_pos.gettippos(x, imagename)
        xi = pos[0]
        yi = pos[1]
        xlistpoints.append(xi)
        ylistpoints.append(yi)
        print("XLISTPOINTS: ", xlistpoints)
        print("YLISTPOINTS: ", ylistpoints)
        #imgc = 'ana-' + imagename #might not want to dispay
        #imageme.displaylast(x, imgc)
       
        i += 1
       
    x_uncert = np.std(xlistpoints)
    y_uncert = np.std(ylistpoints)
    print("XLISTPOINTS: ", xlistpoints)
    print("YLISTPOINTS: ", ylistpoints)
    print("X STANDARD DEVIATION: ", x_uncert)
    print("Y STANDARD DEVIATION: ", y_uncert)
   
def write_csv():
    df = pd.DataFrame(list(zip(*[xlistpoints, ylistpoints, v_inputs, axis_inputs, dir_inputs, steps_inputs]))).add_prefix('Col')
    df.columns = ['X_pix', 'Y_pix', 'V_input', 'Ax_input', 'Dir_input', 'Steps_input']
    print("DF: ", df)
    ### MIGHT WANT TO ADD TEXT BOX TO DEFINE CSV NAME AT A LATER STATE
    df.to_csv('test_data', index=False)
   
   
def calibrate():
    ## get inputs from text boxes
    trials = 2.
    v_step= 0.5
    v_max= 3.0
    steps= 10.
    date=str(date_txt.get())
    print("args: ", " trials: ", trials, " v_step: ", v_step, " v_max: ", v_max, " steps: ", steps)
    v_min = 1.0
    v_stop = v_max + v_step
   
    ##reset lists to proper values
    xlistpoints.clear()
    ylistpoints.clear()
    v_inputs.clear()
    axis_inputs.clear()
    dir_inputs.clear()
    steps_inputs.clear()
    theta1.clear()
    theta2.clear()
    move1.clear()
    move2.clear()
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
    axis = 1
    while v < v_stop:
        i = 0
        while i < trials:
       
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
       
    axis = 2
    v = v_min
    #REPEAT
    while v < v_stop:
        i = 0
        while i < trials:
       
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
    calfname = 'cal_data_' + str(date)
    df.to_csv(calfname, index=False)
   
   
    ## CALCULATE DISP/VOLT/STEP
    ## disp_func
    #dfile = 'cal_data_'+str(date)
    #df = pd.read_csv(dfile)
    df['dx'] = 0.0
    df['dy'] = 0.0
    df['disp'] = 0.0

    xs = list(df['X_pix'])
    ys = list(df['Y_pix'])
    #print(xs, ys)

    for i in range(len(df)):
        if i != 0:
            argx = xs[i] - xs[i-1]
            argy = ys[i] - ys[i-1]
            df['dx'][i] = argx
            df['dy'][i] = argy
            df['disp'] = (df['dx']**2 + df['dy']**2)**(1/2)
           
    ## CALCULATE ANGLES AND DISP/V/STEP
    ## CALCULATE ANGLES
    ax1slice = df['Ax_input'] == 1.0
    ax2slice = df['Ax_input'] == 2.0
    ax1data = df[ax1slice]
    ax2data = df[ax2slice]
   
    m11, b11 = np.polyfit(ax1data['X_pix'], ax1data['Y_pix'], 1)
    m21, b21 = np.polyfit(ax2data['X_pix'], ax2data['Y_pix'], 1)
   
    slope1.append(m11)
    slope2.append(m21)
    theta1.append(np.rad2deg(np.arctan(m11)))
    theta2.append(np.rad2deg(np.arctan(m21)))
    print("SLOPE1: ", m11)
    print("SLOPE2: ", m21)
   
    ## volt_disp_linear
    ## ax1
    volts1 = ax1data['V_input']
    disps1 = ax1data['disp']
    steps1 = ax1data['Steps_input'].mean()
    m12, b12 = np.polyfit(volts1, disps1, 1)
    move1_1 = m12 / steps1
    move1.append(move1_1)
    print(move1, " PIXELS/VOLT/STEP (CH1)")
    ## ax2
    volts2 = ax2data['V_input']
    disps2 = ax2data['disp']
    steps2 = ax2data['Steps_input'].mean()
    m22, b22 = np.polyfit(volts2, disps2, 1)
    move2_1 = m22 / steps2
    move2.append(move2_1)
    print(move2, " PIXELS/VOLT/STEP (CH2)")
   
    ## make position plot:
    fig = plt.figure(figsize=(10,10))
    ax=fig.add_subplot(111)
    ax.scatter(ax1data['X_pix'], ax1data['Y_pix'], c='b', alpha=0.5, s=100.)
    ax.scatter(ax2data['X_pix'], ax2data['Y_pix'], c='g', alpha=0.5, s=100.)
    #ax.set_xlim(1650., 1950.)
    #ax.set_ylim(800., 1100.)
    fit1 = plt.plot(ax1data['X_pix'], m11*ax1data['X_pix'] + b11, c='r', ls='-.', lw=2.)
    fit2 = plt.plot(ax2data['X_pix'], m21*ax2data['X_pix'] + b21, c='r', ls='-.', lw=2.)
    figname1 = 'pos_scatterplot_'+str(date)+'.png'
    fig.savefig(figname1)
    ## DISPLAY PLOT
    print('DISPLAY SCATTER')
    imagemeF.displaylast(x,figname1)
   
    print('MAKING VOLT DISP PLOTS')
    ## make volt_disp_linear plots:
    plt.figure(figsize=(8,8))
    plt.title('CH1 Voltage vs. Displacement')
    plt.scatter(volts1, disps1, alpha=0.7, s=90.)
    plt.xlabel('voltage input')
    plt.ylabel('displacement (pixels)')
    plt.plot(volts1, m12*volts1 + b12, c='r', ls='-.', lw=1.5)
    figname2 = 'volt_disp_linear_ax1_'+str(date)+'.png'
    plt.savefig(figname2)
    print('SAVED AX1 PLOT')
    ## DISPLAY PLOT
    imagemeF.displaylast(x,figname2)
   
    plt.figure(figsize=(8,8))
    plt.title('CH2 Voltage vs. Displacement')
    plt.scatter(volts2, disps2, alpha=0.7, s=90.)
    plt.xlabel('voltage input')
    plt.ylabel('displacement (pixels)')
    plt.plot(volts2, m22*volts2 + b22, c='r', ls='-.', lw=1.5)
    figname3 = 'volt_disp_linear_ax2_'+str(date)+'.png'
    plt.savefig(figname3)
    ## DISPLAY PLOT
    imagemeF.displaylast(x,figname3)
   
    ### CODE FROM DISPLAYLAST
    #imagename = str(txt.get())
    #imagename=imagename+".jpg"
    #print('disp: IMAGENAME: ',imagename)
    #imageme.displaylast(x,imagename)
   
    print("CALIBRATED")
    print("THETA1: ", theta1)
    print("THETA2: ", theta2)
    print("ORTHOGONALITY: ", (abs(theta1[0])+abs(theta2[0])))
    print("DISP/VOLT/STEP 1: ", move1)
    print("DISP/VOLT/STEP 2: ", move2)
   
    ## WRITE DF
    filename = 'calibration_data_' + str(date)
    df.to_csv(filename, index=False)
    
   
def plot_cal_data():
    date=str(date_txt.get())
    #date = '1107'
    ## CALCULATE DISP/VOLT/STEP
    ## disp_func
    dfile = 'cal_data_'+str(date)
    df = pd.read_csv(dfile)
    df['dx'] = 0.0
    df['dy'] = 0.0
    df['disp'] = 0.0

    xs = list(df['X_pix'])
    ys = list(df['Y_pix'])
    #print(xs, ys)

    for i in range(len(df)):
        if i != 0:
            argx = xs[i] - xs[i-1]
            argy = ys[i] - ys[i-1]
            df['dx'][i] = argx
            df['dy'][i] = argy
            df['disp'] = (df['dx']**2 + df['dy']**2)**(1/2)
           
    ## CALCULATE ANGLES AND DISP/V/STEP
    ## CALCULATE ANGLES
    ax1slice = df['Ax_input'] == 1.0
    ax2slice = df['Ax_input'] == 2.0
    ax1data = df[ax1slice]
    ax2data = df[ax2slice]
   
    m11, b11 = np.polyfit(ax1data['X_pix'], ax1data['Y_pix'], 1)
    m21, b21 = np.polyfit(ax2data['X_pix'], ax2data['Y_pix'], 1)
   
    slope1.append(m11)
    slope2.append(m21)
    theta1.append(np.rad2deg(np.arctan(m11)))
    theta2.append(np.rad2deg(np.arctan(m21)))
    print("SLOPE1: ", m11)
    print("SLOPE2: ", m21)
   
    ## volt_disp_linear
    ## ax1
    volts1 = ax1data['V_input']
    disps1 = ax1data['disp']
    steps1 = ax1data['Steps_input'].mean()
    m12, b12 = np.polyfit(volts1, disps1, 1)
    move1_1 = m12 / steps1
    move1.append(move1_1)
    print(move1, " PIXELS/VOLT/STEP (CH1)")
    ## ax2
    volts2 = ax2data['V_input']
    disps2 = ax2data['disp']
    steps2 = ax2data['Steps_input'].mean()
    m22, b22 = np.polyfit(volts2, disps2, 1)
    move2_1 = m22 / steps2
    move2.append(move2_1)
    print(move2, " PIXELS/VOLT/STEP (CH2)")
   
    ## make position plot:
    fig = plt.figure(figsize=(10,10))
    ax=fig.add_subplot(111)
    ax.scatter(ax1data['X_pix'], ax1data['Y_pix'], c='b', alpha=0.5, s=100.)
    ax.scatter(ax2data['X_pix'], ax2data['Y_pix'], c='g', alpha=0.5, s=100.)
    #ax.set_xlim(1650., 1950.)
    #ax.set_ylim(800., 1100.)
    fit1 = plt.plot(ax1data['X_pix'], m11*ax1data['X_pix'] + b11, c='r', ls='-.', lw=2.)
    fit2 = plt.plot(ax2data['X_pix'], m21*ax2data['X_pix'] + b21, c='r', ls='-.', lw=2.)
    figname1 = 'pos_scatterplot_'+str(date)+'.png'
    fig.savefig(figname1)
    ## DISPLAY PLOT
    print('DISPLAY SCATTER')
    imagemeF.displaylast(x,figname1)
   
    print('MAKING VOLT DISP PLOTS')
    ## make volt_disp_linear plots:
    plt.figure(figsize=(8,8))
    plt.title('CH1 Voltage vs. Displacement')
    plt.scatter(volts1, disps1, alpha=0.7, s=90.)
    plt.xlabel('voltage input')
    plt.ylabel('displacement (pixels)')
    plt.plot(volts1, m12*volts1 + b12, c='r', ls='-.', lw=1.5)
    figname2 = 'volt_disp_linear_ax1_'+str(date)+'.png'
    plt.savefig(figname2)
    print('SAVED AX1 PLOT')
    ## DISPLAY PLOT
    imagemeF.displaylast(x,figname2)
   
    plt.figure(figsize=(8,8))
    plt.title('CH2 Voltage vs. Displacement')
    plt.scatter(volts2, disps2, alpha=0.7, s=90.)
    plt.xlabel('voltage input')
    plt.ylabel('displacement (pixels)')
    plt.plot(volts2, m22*volts2 + b22, c='r', ls='-.', lw=1.5)
    figname3 = 'volt_disp_linear_ax2_'+str(date)+'.png'
    plt.savefig(figname3)
    ## DISPLAY PLOT
    imagemeF.displaylast(x,figname3)
   
    ### CODE FROM DISPLAYLAST
    #imagename = str(txt.get())
    #imagename=imagename+".jpg"
    #print('disp: IMAGENAME: ',imagename)
    #imageme.displaylast(x,imagename)
   
    print("CALIBRATED")
    print("THETA1: ", theta1)
    print("THETA2: ", theta2)
    print("ORTHOGONALITY: ", (abs(theta1[0])+abs(theta2[0])))
    print("DISP/VOLT/STEP 1: ", move1)
    print("DISP/VOLT/STEP 2: ", move2)
   
    ## WRITE DF
    #filename = 'calibration_data_' + str(date)
    #df.to_csv(filename, index=False)

def load_cal_data():
    date = str(date_txt.get())
    ## CALCULATE DISP/VOLT/STEP
    ## disp_func
    dfile = 'cal_data_'+str(date)
    df = pd.read_csv(dfile)
    df['dx'] = 0.0
    df['dy'] = 0.0
    df['disp'] = 0.0

    xs = list(df['X_pix'])
    ys = list(df['Y_pix'])
    #print(xs, ys)

    for i in range(len(df)):
        if i != 0:
            argx = xs[i] - xs[i-1]
            argy = ys[i] - ys[i-1]
            df['dx'][i] = argx
            df['dy'][i] = argy
            df['disp'] = (df['dx']**2 + df['dy']**2)**(1/2)
           
    ## CALCULATE ANGLES AND DISP/V/STEP
    ## CALCULATE ANGLES
    ax1slice = df['Ax_input'] == 1.0
    ax2slice = df['Ax_input'] == 2.0
    ax1data = df[ax1slice]
    ax2data = df[ax2slice]
   
    m11, b11 = np.polyfit(ax1data['X_pix'], ax1data['Y_pix'], 1)
    m21, b21 = np.polyfit(ax2data['X_pix'], ax2data['Y_pix'], 1)
   
    slope1.append(m11)
    slope2.append(m21)
    theta1.append(np.rad2deg(np.arctan(m11)))
    theta2.append(np.rad2deg(np.arctan(m21)))
    print("SLOPE1: ", m11)
    print("SLOPE2: ", m21)
   
    ## volt_disp_linear
    ## ax1
    volts1 = ax1data['V_input']
    disps1 = ax1data['disp']
    steps1 = ax1data['Steps_input'].mean()
    m12, b12 = np.polyfit(volts1, disps1, 1)
    move1_1 = m12 / steps1
    move1.append(move1_1)
    print(move1, " PIXELS/VOLT/STEP (CH1)")
    ## ax2
    volts2 = ax2data['V_input']
    disps2 = ax2data['disp']
    steps2 = ax2data['Steps_input'].mean()
    m22, b22 = np.polyfit(volts2, disps2, 1)
    move2_1 = m22 / steps2
    move2.append(move2_1)
    print(move2, " PIXELS/VOLT/STEP (CH2)")
   
    print("CALIBRATED")
    print("THETA1: ", theta1)
    print("THETA2: ", theta2)
    print("ORTHOGONALITY: ", (abs(theta1[0])+abs(theta2[0])))
    print("DISP/VOLT/STEP 1: ", move1)
    print("DISP/VOLT/STEP 2: ", move2)
   
def go_there():
    print("GO THERE TRIGGERED")
    xf = float(test_txt1.get())
    yf = float(test_txt2.get())
    max_iter = int(test_txt3.get())
    date = str(date_txt.get())
   
    m1 = slope1[0]
    m2 = slope2[0]
    
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
   
    # take photo
    i = 0
    imagename = "go_there_" + "i" + str(i)
    DoPhotoCopy2.takePhotoAndCopy(x,imagename)
    imagename=imagename+".jpg"
    while os.path.exists(imagename) == False:
        imagename = "go_there_" + "i" + str(i)
        DoPhotoCopy2.takePhotoAndCopy(x,imagename)
        imagename=imagename+".jpg"
    else:
        print("IMAGE TAKEN!")
    #imageme.displaylast(x,imagename)
    #result=imagename
    # locate tip
    print('disp: IMAGENAME: ',imagename)
    time.sleep(5)
    pos = get_tip_pos.gettippos(x, imagename)
    xi = pos[0]
    yi = pos[1]
    xlistpoints.append(xi)
    ylistpoints.append(yi)
    print("START LOCATION: xpix: ", xi, " ypix: ", yi)
    #xlistpoints.append(xi)
    #ylistpoints.append(yi)
   
   
    ### SET UP LOOP:
    while i < (max_iter):
        # calculate the needed motion
        ##
        delta_x = xf - xi
        delta_y = yf - yi
        print('DELTA_X: ', delta_x)
        print('DELTA_Y: ', delta_y)
        
        b = (delta_y - delta_x*m1) / (m2 - m1)
        a = delta_x - b
        udisp1 = (m1**2 + 1)*(0.5)
        udisp2 = (m2**2 + 1)*(0.5)
        disp1 = a*udisp1
        disp2 = b*udisp2
        print('DISP1: ', disp1)
        print('DISP2: ', disp2)

        ### FACTOR IN VOLTAGES THAT WILL BE USED
        v1 = 2.0
        v2 = 3.5
        print(v1, 'VOLTS CH1')
        print(v2, 'VOLTS CH2')
        steps_1 = disp1 / (v1*move1[0])
        steps_2 = disp2 / (v2*move2[0])
        print("STEPS1: ", steps_1)
        print("STEPS2: ", steps_2)
       
        ## TRIGGER:
        ##CH1 trigger:
        ### remember to factor in voltage above!!
        if steps_1 < 0:
            d1 = 'pos'
        else:
            d1 = 'neg'
       
        if steps_2 < 0:
            d2 = 'neg'
        else:
            d2 = 'pos'
           
        if steps_1 < 100.:
            rest1 = 20
        else:
            rest1 = 30
           
        if steps_2 < 50.:
            rest2 = 20
        else:
            steps_2 = 40
            rest2 = 20
           
        finian_keysight_trigger_poltest.trigger_keysight(v1, 1, d1, abs(round(steps_1)))
        v_inputs.append(v1)
        axis_inputs.append(1)
        dir_inputs.append(d1)
        steps_inputs.append(abs(round(steps_1)))
        xlistpoints.append(0.0)
        ylistpoints.append(0.0)
        ##TIME DELAY
        time.sleep(rest1)
       
        #finian_keysight_trigger_poltest.trigger_keysight(v2, 2, d2, abs(round(steps_2)))
        #v_inputs.append(v2)
        #axis_inputs.append(2)
        #dir_inputs.append(d2)
        #steps_inputs.append(abs(round(steps_2)))
        ##TIME DELAY
        #time.sleep(rest2)
       
        ### LOCATE TIP AGAIN!
        # take photo
        i+=1
        imagename = "go_there_" + "i" + str(i)
        DoPhotoCopy2.takePhotoAndCopy(x,imagename)
        imagename=imagename+".jpg"
        while os.path.exists(imagename) == False:
            imagename = "go_there_" + "i" + str(i)
            DoPhotoCopy2.takePhotoAndCopy(x,imagename)
            imagename=imagename+".jpg"
        else:
            print("IMAGE TAKEN!")
        #imageme.displaylast(x,imagename)
        #result=imagename
        # locate tip
        time.sleep(5)
        print('disp: IMAGENAME: ',imagename)
        pos = get_tip_pos.gettippos(x, imagename)
        x_test = pos[0]
        y_test = pos[1]
        xlistpoints.append(x_test)
        ylistpoints.append(y_test)
        dx = abs(x_test - xf)
        dy = abs(y_test - yf)
       
        # STARTING WITH 5 PIXEL RANGE FOR TESTING PURPOSES; TRY TIGHTENING LATER
        if (dx**2 + dy**2)**(0.5) < 5.:
            print('MADE IT!')
            print('LOCATION: ', 'X_pix: ', x_test, 'Y_pix: ', y_test)
            imgc = 'ana-' + imagename
            imageme.displaylast(x, imgc)
           
            break
            # if break doesn't work: i+=max_iter
           
        else:
            print('NOT THERE YET!')
            print('LOCATION: ', 'X_pix: ', x_test, 'Y_pix: ', y_test)
            xi = x_test
            yi = y_test
            print('RESTART LOOP: ITERATION: ', i)

    print("OUT OF LOOP")
    print("writing trigger inputs and position data to csv")
    df = pd.DataFrame(list(zip(*[xlistpoints, ylistpoints, v_inputs, axis_inputs, dir_inputs, steps_inputs]))).add_prefix('Col')
    df.columns = ['X_pix', 'Y_pix', 'V_input', 'Ax_input', 'Dir_input', 'Steps_input']
    print("DF: ", df)
    ### MIGHT WANT TO ADD TEXT BOX TO DEFINE CSV NAME AT A LATER STATE
    csvname = 'go_there_data_'+str(date)
    df.to_csv(csvname, index=False)
    print("wrote file: ", str(csvname))

       

def go_home():
    print("GO HOME TRIGGERED")
    max_iter = int(test_txt3.get())
    ## GET MAX ITERATION!!
    go_there(1770, 750, max_iter)
   

x='__main__'
name = 'image3'

lblw = tkinter.Label(top,text = "Set the RP to current time:")
lblw.grid(row = 1, column = 0)
w = tkinter.Button(top, text="setRPclock", command=testerCallBack )
w.grid(row = 1, column = 1)

lbldpc=tkinter.Label(top,text = "image name:")
lbldpc.grid(row=2, column=0)

imagename=""
part_dopho=partial(dophotoscp,imagename) ##FINIAN: IS THIS USED? (I don't think so)
dpc = tkinter.Button(top, text="TakePhoto", command=dophotoscp )
dpc.grid(row = 2, column = 2)

wdb = tkinter.Button(top, text="write data", command=write_csv)
wdb.grid(row=3, column=2)

dispim = tkinter.Button(top, text="display last image", command = displaylast)
dispim.grid(row = 3, column=0)

findtip = tkinter.Button(top, text="find tip in image", command = get_tip)
findtip.grid(row = 4, column=0)

reset_coords = tkinter.Button(top, text="reset data lists", command = reset_data_lists)
reset_coords.grid(row = 4, column = 1)

## TAKEN FROM TKFUN. WILL LIKELY NEED TO CHANGE SOMEWHAT
## GET RID OF HARD CODED INPUTS, FIND WHAT THEY NEED TO BE
#xlistpoints = [1.0, -1.0, 1.0, -1.0]
#ylistpoints = [1.0, -1.0, -1.0, 1.0]
control = '__main__'
fitme = tkinter.Button(top, text="show plots",command=plot_cal_data)
fitme.grid(row=3, column=1)

## ADDING UNCERT CALC
lblunc=tkinter.Label(top, text="N (trials for uncert. calc):")
lblunc.grid(row=7, column=0)
unc = tkinter.Button(top, text="Calc. Uncertainty", command=calc_uncertainty)
unc.grid(row=7, column=2)

##DEFINE CALIBRATION FUNCTIONALITY
fktCommand = tkinter.Label(top,text = "Calibrations:")
fktCommand.grid(row=8, column=0)

lblfrt4=tkinter.Label(top,text = "Date (no /):")
lblfrt4.grid(row=9, column=0)

loadbtn = tkinter.Button(top, text='load cal data (date)', command=load_cal_data)
loadbtn.grid(row=10, column=0)

ghb = tkinter.Button(top, text="Go Home (1770,750)", command=go_home)
ghb.grid(row = 11, column = 0)

ch1cb = tkinter.Button(top, text="Calibrate System", command=calibrate)
ch1cb.grid(row = 12, column = 0)

## ADDING "GO THERE" (trials/V, V_step, steps, V_max)
frtCommand = tkinter.Label(top,text = "Motion Inputs:")
frtCommand.grid(row=8, column=2)

lblfrt1=tkinter.Label(top,text = "X_pix:")
lblfrt1.grid(row=9, column=2)
lblfrt2=tkinter.Label(top,text = "Y_pix:")
lblfrt2.grid(row=10, column=2)
lblfrt3=tkinter.Label(top,text = "Max_iter:")
lblfrt3.grid(row=11, column=2)

frt = tkinter.Button(top, text="GO THERE", command=go_there)
frt.grid(row = 12, column = 3)

###
### NEW BUTTON IDEA: CALC POSITIONAL UNCERTAINTY (PIXEL COORDINATES), have number N of trials to use as input,
### then will run takephoto/findtip N times and calculate the uncertainty in coordinates
###

top.mainloop()