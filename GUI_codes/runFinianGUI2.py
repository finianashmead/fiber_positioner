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

top = tkinter.Tk()
top.title("Tilting Spine Operating Functions")
top.geometry('500x300')


txt = tkinter.Entry(top, width=15)
txt.grid(row=2,column=1)

## trigger inputs
trig_txt1 = tkinter.Entry(top, width=10)
trig_txt1.grid(row=9,column=1)
trig_txt2 = tkinter.Entry(top, width=10)
trig_txt2.grid(row=10,column=1)
trig_txt3 = tkinter.Entry(top, width=10)
trig_txt3.grid(row=11,column=1)
trig_txt4 = tkinter.Entry(top, width=10)
trig_txt4.grid(row=12,column=1)

## run_test inputs
test_txt1 = tkinter.Entry(top, width=10)
test_txt1.grid(row=9,column=3)
test_txt2 = tkinter.Entry(top, width=10)
test_txt2.grid(row=10,column=3)
test_txt3 = tkinter.Entry(top, width=10)
test_txt3.grid(row=11,column=3)
test_txt4 = tkinter.Entry(top, width=10)
test_txt4.grid(row=12,column=3)
test_txt5 = tkinter.Entry(top, width=10)
test_txt5.grid(row=13,column=3)

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
    
    date=str(test_txt5.get())
    # clear data lists
    xlistpoints.clear()
    ylistpoints.clear()
    
    # trigger keysight several times to take data
    finian_keysight_trigger_poltest.trigger_keysight(2.5, 1, 'pos', 50)
    
    time.sleep(15)
    # take photo
    i = 0
    imagename = "circle_test_img_" + "i" + str(i) + '_date_' + date
    DoPhotoCopy2.takePhotoAndCopy(x,imagename)
    imagename=imagename+".jpg"
    while os.path.exists(imagename) == False:
        imagename = "circle_test_img_" + "i" + str(i) + '_date_' + date
        DoPhotoCopy2.takePhotoAndCopy(x,imagename)
        imagename=imagename+".jpg"
    else:
        print("IMAGE TAKEN!")            
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
    i+=1
    
    finian_keysight_trigger_poltest.trigger_keysight(2.5, 1, 'neg', 70)
    
    time.sleep(15)
    # take photo
    imagename = "circle_test_img_" + "i" + str(i) + '_date_' + date
    DoPhotoCopy2.takePhotoAndCopy(x,imagename)
    imagename=imagename+".jpg"
    while os.path.exists(imagename) == False:
        imagename = "circle_test_img_" + "i" + str(i) + '_date_' + date
        DoPhotoCopy2.takePhotoAndCopy(x,imagename)
        imagename=imagename+".jpg"
    else:
        print("IMAGE TAKEN!")            
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
    i+=1
    
    finian_keysight_trigger_poltest.trigger_keysight(1.5, 1, 'pos', 10)
    
    time.sleep(10)
    
    finian_keysight_trigger_poltest.trigger_keysight(2.5, 2, 'neg', 50)
    
    time.sleep(15)
    # take photo
    imagename = "circle_test_img_" + "i" + str(i) + '_date_' + date
    DoPhotoCopy2.takePhotoAndCopy(x,imagename)
    imagename=imagename+".jpg"
    while os.path.exists(imagename) == False:
        imagename = "circle_test_img_" + "i" + str(i) + '_date_' + date
        DoPhotoCopy2.takePhotoAndCopy(x,imagename)
        imagename=imagename+".jpg"
    else:
        print("IMAGE TAKEN!")            
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
    i+=1
    
    finian_keysight_trigger_poltest.trigger_keysight(2.5, 2, 'pos', 70)
    
    time.sleep(15)
    # take photo
    imagename = "circle_test_img_" + "i" + str(i) + '_date_' + date
    DoPhotoCopy2.takePhotoAndCopy(x,imagename)
    imagename=imagename+".jpg"
    while os.path.exists(imagename) == False:
        imagename = "circle_test_img_" + "i" + str(i) + '_date_' + date
        DoPhotoCopy2.takePhotoAndCopy(x,imagename)
        imagename=imagename+".jpg"
    else:
        print("IMAGE TAKEN!")            
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
    i+=1
    
    #original circlefit starting point
    if len(xlistpoints) > 2:
        control = '__main__'
        print('XLISTPOINTS', xlistpoints)
        print('YLISTPOINTS', ylistpoints)
        circlecenterx, circlecentery, circleR, chi2 = fitmycircle(control,xlistpoints,ylistpoints)
        print("fitresult ",circlecenterx, circlecentery, circleR, chi2)
        
        ## CODE FOR DRAWING CIRCLE ON COPY IMAGE
        #imagename = str(txt.get())
        #imagename=imagename+".jpg"
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
    
    
def run_test():
    ## get inputs from text boxes
    trials = int(test_txt1.get())
    step_step=int(test_txt2.get())
    step_max=int(test_txt3.get())
    v=float(test_txt4.get())
    date=str(test_txt5.get())
    print("args: ", " trials: ", trials, " step_step: ", step_step, " step_max: ", step_max, " v: ", v)
    step_min = 1  #0.0 + v_step
    step_stop = step_max + step_step
    
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
    steps = step_min
    axis = 2
    while steps < step_stop:
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
            imagename = "test_img" + str(steps) + "i" + str(i) + str(axis) + str(d) + date
            DoPhotoCopy2.takePhotoAndCopy(x,imagename)
            imagename=imagename+".jpg"
            while os.path.exists(imagename) == False:
                imagename = "test_img" + str(steps) + "i" + str(i) + str(axis) + str(d) + date
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
            imagename = "test_img" + str(steps) + "i" + str(i) + str(axis) + str(d) + date
            DoPhotoCopy2.takePhotoAndCopy(x,imagename)
            imagename=imagename+".jpg"
            while os.path.exists(imagename) == False:
                imagename = "test_img" + str(steps) + "i" + str(i) + str(axis) + str(d) + date
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
        
        steps += step_step
        
    axis = 1
    steps = step_min
    #REPEAT
    while steps < step_stop:
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
            imagename = "test_img" + str(steps) + "i" + str(i) + str(axis) + str(d) + date
            DoPhotoCopy2.takePhotoAndCopy(x,imagename)
            imagename=imagename+".jpg"
            while os.path.exists(imagename) == False:
                imagename = "test_img" + str(steps) + "i" + str(i) + str(axis) + str(d) + date
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
            imagename = "test_img" + str(steps) + "i" + str(i) + str(axis) + str(d) + date
            DoPhotoCopy2.takePhotoAndCopy(x,imagename)
            imagename=imagename+".jpg"
            while os.path.exists(imagename) == False:
                imagename = "test_img" + str(steps) + "i" + str(i) + str(axis) + str(d) + date
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
        
        steps += step_step
    
    ## write data to csv
    df = pd.DataFrame(list(zip(*[xlistpoints, ylistpoints, v_inputs, axis_inputs, dir_inputs, steps_inputs]))).add_prefix('Col')
    df.columns = ['X_pix', 'Y_pix', 'V_input', 'Ax_input', 'Dir_input', 'Steps_input']
    print("DF: ", df)
    ### MIGHT WANT TO ADD TEXT BOX TO DEFINE CSV NAME AT A LATER STATE
    df.to_csv('test_data', index=False)
    


x='__main__'
name = 'image3'

lblw = tkinter.Label(top,text = "Set the RP to current time:")
lblw.grid(row = 1, column = 0)
w = tkinter.Button(top, text="setRPclock", command=testerCallBack )
w.grid(row = 1, column = 1)

lbldpc=tkinter.Label(top,text = "Take and SCP Image of name:")
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
fitme = tkinter.Button(top, text="fitcircle",command=circlefit)
fitme.grid(row=3, column=1)

## ADDING UNCERT CALC
lblunc=tkinter.Label(top, text="N (trials for uncert. calc):")
lblunc.grid(row=7, column=0)
unc = tkinter.Button(top, text="Calc. Uncertainty", command=calc_uncertainty)
unc.grid(row=7, column=2)


##WRAPPING IN MY TRIGGERING MODULE finian_keysight_trigger.py
fktCommand = tkinter.Label(top,text = "Trigger Inputs:")
fktCommand.grid(row=8, column=0)

lblfkt1=tkinter.Label(top,text = "V:")
lblfkt1.grid(row=9, column=0)
lblfkt2=tkinter.Label(top,text = "Axis (1 or 2):")
lblfkt2.grid(row=10, column=0)
lblfkt3=tkinter.Label(top,text = "Direction (pos or neg):")
lblfkt3.grid(row=11, column=0)
lblfkt4=tkinter.Label(top,text = "Steps:")
lblfkt4.grid(row=12, column=0)


fkt = tkinter.Button(top, text="Trigger Keysight", command=trigger_keysight)
fkt.grid(row = 13, column = 1)

## ADDING "RUN TESTS" (trials/V, V_step, steps, V_max)
frtCommand = tkinter.Label(top,text = "Test Inputs:")
frtCommand.grid(row=8, column=2)

lblfrt1=tkinter.Label(top,text = "Trials/stepsize:")
lblfrt1.grid(row=9, column=2)
lblfrt2=tkinter.Label(top,text = "step_step:")
lblfrt2.grid(row=10, column=2)
lblfrt3=tkinter.Label(top,text = "step_max:")
lblfrt3.grid(row=11, column=2)
lblfrt4=tkinter.Label(top,text = "V:")
lblfrt4.grid(row=12, column=2)
lblfrt4=tkinter.Label(top,text = "Date (no /):")
lblfrt4.grid(row=13, column=2)


frt = tkinter.Button(top, text="Run Test", command=run_test)
frt.grid(row = 14, column = 3)


###
### NEW BUTTON IDEA: CALC POSITIONAL UNCERTAINTY (PIXEL COORDINATES), have number N of trials to use as input, 
### then will run takephoto/findtip N times and calculate the uncertainty in coordinates
###



top.mainloop()
