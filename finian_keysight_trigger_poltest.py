def trigger_keysight(v=3, axis=2, d="pos", steps=20): 
    ##FINIAN: use control to define __main__, v to define voltage, axis to define CH1 or CH2, steps to define # of cycles in burst
    ## not sure how to pass voltage to Terri's waveforms yet, leave out to start
    ## FINIAN 10/5 : trying to put the voltage controls back in
    import pyvisa as visa
    import argparse
    import time
    
    ####
    ####FINIAN: this argparse bit doesn't seem to be used other than for v, based on fit2circle.py probably not needed for my purpose
    ####
    
#    parser = argparse.ArgumentParser()
#    print("here00")
#    args = parser.parse_args()
#    print("here0")
#    parser.add_argument("-v", type=float,
#                        help="Amplitude of ramp between 0 and 5",default=3.0)
#    parser.add_argument("-axis", type=int,
#                        help="1/2 are orthogonal directions",default=2)

#    parser.add_argument("-d", type=str,
#                        help="Direction, 'pos' or 'neg'",default='pos')
#    parser.add_argument("-steps", type=int,
#                        help="number of cycles for burst",default=100)                    

#    print("here1")
#    args = parser.parse_args()
#    print("here2")
    #print("V={0}, Freq={1}, Dir={"SOURC2}".format(args.V,args.F,args.D))
#    v=float(args.v)
#    axis=int(args.axis)
#    d=args.d
#   steps=int(args.steps)
#    print("args", v, axis, d, steps)

    rm = visa.ResourceManager()
    rm.list_resources()
    AWG = rm.open_resource('USB0::10893::36097::CN61310002::0::INSTR')
    print("AWG QUERY IDN" , AWG.query('*IDN?'))

####
####FINIAN: here I want to put a switch for the axis that defines all the strings needed below according to which one it is
####
    if axis==1:
        #print("accessed axis 1")
        dosour1 = "TRUE"
        dosour2 = "FALSE"
        basestr = "SOURCE1:"
        cntstr = "1"
    else:
        #print("accessed axis 2")
        dosour1 = "FALSE"
        dosour2 = "TRUE"
        basestr = "SOURCE2:"
        cntstr = "2"
    if d=="pos":    
        goright = "TRUE"  # Moves the tip to the right or away
        AWG.write(basestr+"VOLT:OFFS 0")
 
    else:
        goright = "FALSE" #Moves the tip to the left or towards#
        #AWG.write(basestr+"VOLT:OFFS "+str(-v))
    
    #print("GORIGHT?: ", goright)
        
    ### RAMPS ARE CALLED "TMSNegRamp.arb" and "TMSPosRamp.arb"
    ### 
    #print("BASESTR: ", basestr)
    
    ### HERE I AM NOW ATTEMPTING TO USE THE ARB FUNCTION: trial 1: replace RAMP in all string messages with ARB 
    ### --> didn't seem to work, queries still returned RAMP
    
    #AWG.write("SOURCE1:FUNC STATE 0")
    AWG.write(basestr+"VOLT:OFFS 0")
    AWG.write(basestr+"FUNC ARB")
    #AWG.write(basestr+"FUNC:ARB:SRAT 1e4")
    print("SRAT: ", AWG.query(basestr+"FUNC:ARB:SRAT?"))
    func = str(AWG.query(basestr+"FUNC?"))
    if func != 'ARB':
        AWG.write("MMEM:LOAD:DATA"+cntstr+" 'USB:\\ARBITRARY WAVEFORMS RAMPS\\TMSPOSRAMP.ARB'")
        print("LOAD WORKED?: ", AWG.query("SOURCE"+cntstr+":DATA:VOL:CAT?"))
        AWG.write(basestr+"FUNC ARB")
    
    mess = basestr+"FUNC:ARB 'USB:\\ARBITRARY WAVEFORMS RAMPS\\TMSPOSRAMP.ARB'"
    print("MESSAGE: ", mess)
    AWG.write(mess)
    print("FUNC: ", AWG.query(basestr+"FUNC?"))
    AWG.write(basestr+"FUNC:ARB:PTP "+str(v))
    AWG.write(basestr+"VOLT:RANGE:AUTO ON")
    #AWG.write("SOURCE2:VOLT:RANGE:AUTO OFF")
    
    #print("UNITS: ", AWG.query(basestr+"VOLT:UNIT?"))
    #print("OFFSET000: ", AWG.query(basestr+"VOLT:OFFS?"))
    #print("PTP: ", AWG.query(basestr+"FUNC:ARB:PTP?"))
    #print("FUNC: ", AWG.query(basestr+"FUNC?"))
    #print("OUTPUT LOAD: ", AWG.query("OUTP"+cntstr+":LOAD?"))
    
    #AWG.write("SOURCE1:FUNC:ARB 'USB:\\ARBITRARY WAVEFORMS RAMPS\\TMSNEGRAMP.ARB'")
    #AWG.write("SOURCE1:FUNC:ARB:NEG_RAMP:SYMMETRY 100")
    #print("DID IT WORK?", AWG.query("SOURCE1:FUNC?"))
    #AWG.write("SOURCE2:FUNC:ARB 'USB:\\ARBITRARY WAVEFORMS RAMPS\\TMSNEGRAMP.ARB'")
    #AWG.write("SOURCE2:FUNC:ARB:NEG_RAMP")
    #print("DID IT WORK?", AWG.query("SOURCE2:FUNC?"))

    #AWG.write("OUTP"+cntstr+" OFF")

    # These two following write commands produce a stray voltage. That's why I turned output off here. 

    #print(AWG.query("FUNC:USER?"))
    #AWG.write("FUNC USER")
    #print(AWG.query("FUNC?"))
    AWG.write("OUTP"+cntstr+" ON")

    #time.sleep(10)
    #
    # Set the amplitude
    #v = 1.5
    #v = 3.0
    #


    # params for ramp
    print("OFFSET00: ", AWG.query(basestr+"VOLT:OFFS?"))
    vhigh = float(v)
    #voff = -0.5 * v
    #voff = 0.
    
    #mess = basestr+"FUNC:ARB 'USB:\\ARBITRARY WAVEFORMS RAMPS\\TMSPOSRAMP.ARB'"
    #print("MESSAGE: ", mess)
    #AWG.write(mess)
    
#    AWG.write(basestr+"VOLT:LIM:LOW 0")
#    AWG.write(basestr+"VOLT:LIM:HIGH "+str(vhigh))
#    AWG.write(basestr+"VOLT:LIM:STAT ON")
#    print("WRITE VOLT LIMS")
#    AWG.write(basestr+"VOLT:LIM:LOW 0")
#    print("VLOWLIM: ", AWG.query(basestr+"VOLT:LIM:LOW?"))
#    AWG.write(basestr+"VOLT:LIM:HIGH "+str(vhigh))
#    print("VHIGHLIM: ", AWG.query(basestr+"VOLT:LIM:HIGH?"))
    
#    mess = basestr+"VOLT:OFFS 0"
    #print(mess)
#    AWG.write(mess)
#    print("WRITE OFFSET")
#    print("VHIGH: ", AWG.query(basestr+"VOLT:HIGH?"))
#    print("VLOW: ", AWG.query(basestr+"VOLT:LOW?"))
#    print("OFFSET: ", AWG.query(basestr+"VOLT:OFFS?"))
    
    mess = basestr+"VOLT "+str(v)
    #print("V MESS", mess)
    AWG.write(mess)
    #print("WRITE VOLTAGE")
    #print("VHIGH: ", AWG.query(basestr+"VOLT:HIGH?"))
    #print("VLOW: ", AWG.query(basestr+"VOLT:LOW?"))
    #print("OFFSET: ", AWG.query(basestr+"VOLT:OFFS?"))
    
    
#    mess = basestr+"VOLT:HIGH "+str(v)
#    AWG.write(mess)
#    print("WRITE HIGH VOLTAGE")
#    print("VHIGH: ", AWG.query(basestr+"VOLT:HIGH?"))
#    print("VLOW: ", AWG.query(basestr+"VOLT:LOW?"))
#    print("OFFSET: ", AWG.query(basestr+"VOLT:OFFS?"))
    
    mess = basestr+"VOLT:OFFS 0"
    #print(mess)
    AWG.write(mess)
    #print("WRITE OFFSET")
    #print("VHIGH: ", AWG.query(basestr+"VOLT:HIGH?"))
    #print("VLOW: ", AWG.query(basestr+"VOLT:LOW?"))
    #print("OFFSET: ", AWG.query(basestr+"VOLT:OFFS?"))
    
#    mess = basestr+"VOLT "+str(v)
#    AWG.write(mess)
#    print("WRITE VOLTAGE")
#    print("VHIGH: ", AWG.query(basestr+"VOLT:HIGH?"))
#    print("VLOW: ", AWG.query(basestr+"VOLT:LOW?"))
#    print("OFFSET: ", AWG.query(basestr+"VOLT:OFFS?"))
    
#    mess = basestr+"VOLT:LOW 0"
#    #print(mess)
#    AWG.write(mess)
#    print("WRITE LOW VOLTAGE")
#    print("VHIGH: ", AWG.query(basestr+"VOLT:HIGH?"))
#    print("VLOW: ", AWG.query(basestr+"VOLT:LOW?"))
#    print("OFFSET: ", AWG.query(basestr+"VOLT:OFFS?"))
    
    
    #print("POLARITY: ", AWG.query("OUTP"+cntstr+":POL?"))
    #AWG.write("OUTP"+cntstr+":POL NORM")
    #print("VHIGH: ", AWG.query(basestr+"VOLT:HIGH?"))
    #print("VLOW: ", AWG.query(basestr+"VOLT:LOW?"))
    #print("VHIGHLIM: ", AWG.query(basestr+"VOLT:LIM:HIGH?"))
    #print("VLOWLIM: ", AWG.query(basestr+"VOLT:LIM:LOW?"))        
    #print("OFFSET: ", AWG.query(basestr+"VOLT:OFFS?"))
        
    #AWG.write(cntstr+"FUNC:ARB:PTP "+str(v))
    print("PTP: ", AWG.query(basestr+"FUNC:ARB:PTP?"))
    print("VHIGH: ", AWG.query(basestr+"VOLT:HIGH?"))
    print("VLOW: ", AWG.query(basestr+"VOLT:LOW?"))
    print("VHIGHLIM: ", AWG.query(basestr+"VOLT:LIM:HIGH?"))
    print("VLOWLIM: ", AWG.query(basestr+"VOLT:LIM:LOW?"))        
    print("OFFSET: ", AWG.query(basestr+"VOLT:OFFS?"))
        
    #print("GORIGHT?: ", goright)
    
    if goright == "FALSE":
        #print("AT SWITCH: F")
        AWG.write("OUTP"+cntstr+":POL INV")
    else:
        #print("AT SWITCH: T")
        AWG.write("OUTP"+cntstr+":POL NORM")
        
    print("POLARITY: ", AWG.query("OUTP"+cntstr+":POL?"))

    #
    # Now issue the control commands
    #
    # I don't know if this is working right.
    # But it does deliver output on push of front panel trigger command
    #
    ncyc = str(steps) ##SET NCYC TO STRING FORM OF STEPS INPUT
    
    AWG.write(basestr+"BURS:STAT ON")
    AWG.write(basestr+"BURS:MODE:TRIG")
    AWG.write(basestr+"BURS:NCYC "+ncyc)  ##FINIAN: THIS SEEMS TO DEFINE THE NUMBER OF CYCLES! ADD VARIABLE TO DEFINE
    AWG.write(basestr+"FREQ 5")
    #AWG.write(basestr+"TRIG:IMM")
    AWG.write("TRIG"+cntstr+":SOURCE BUS")
    AWG.write("TRIG:COUNT 10")
    #AWG.write("*TRG")
    
    AWG.write("TRIG"+cntstr)
    print("TRIGGER!")
    #AWG.write(basestr+"BURS:INT:PER INF")
    #
    # Print stuff
    #
    #print(AWG.query(basestr+"VOLT:HIGH?")+"gothere")
    #print(AWG.query(basestr+"VOLT:LOW?"))
    #print(AWG.query(basestr+"FUNC:ARB:SYMM?")) # pointless
    print("NCYC: ", AWG.query(basestr+"BURS:NCYC?"))
    #print("AUTO?", AWG.query("SOURCE1:VOLT:RANGE:AUTO?"))
    #print("AUTO?", AWG.query("SOURCE2:VOLT:RANGE:AUTO?"))

    #
    # Junk below, but don't delete
    #
#    time.sleep(0.5)
    #if (v>0) and (v<=5):
    #    vs=str(v)
    #    mess="VOLT "+vs
    #    print(mess)
    #    AWG.write(mess)

#    if (freq>0):
#        fs=str(freq)
#        mess="FREQ "+fs
    #    print(mess)
    #    AWG.write(mess)

#    if (dir==0):
#        mess="FUNC:RAMP:SYMM 100"
    #    print(mess)
    #    AWG.write(mess)

#    if (dir==1):
#        mess="FUNC:RAMP:SYMM 0"
    #    print(mess)
    #    AWG.write(mess)
    
####
####FINIAN: added block below (taken from fit2circle as template)
####

if __name__ == '__main__':
    print("MAIN?" , __name__)
    import pyvisa as visa
    import argparse
    import time
    import sys
    print(sys.argv)
    print(sys.argv[1:])

    v=float(sys.argv[1])
    axis=int(sys.argv[2])
    d=str(sys.argv[3])
    steps=int(sys.argv[4])
    print("args", v, axis, d, steps)
    #print("args", axis, d, steps)
#   if len(str(sys.argv[1]))>0:
#       y = str(sys.argv[1])
#       print(y)
#   print('From Main')
    control = '__main__'
#   stdout_nofile = sys.stdout
#   stdout_nofile.write('Done'+'\n')
    #trigger_keysight(control='__main__', sys.argv)
    #trigger_keysight(sys.argv[1:])
    trigger_keysight(v, axis, d, steps)