

def calc_R(cx, cy, xlistpoints, ylistpoints):
    print("calc_R CALLED")
    import numpy as np
#    if control == '__main__':
    return np.sqrt( (xlistpoints - cx)**2 + (ylistpoints - cy)**2)

def f_2(c,xlistpoints,ylistpoints): 
    import numpy as np
#    print(c)
#    if __name__ =='__main__':
    print('f_2 CALLED')
    print("C" , c)
    args = (c[0],c[1],xlistpoints,ylistpoints)
    Ri=calc_R(*args)

    return Ri - Ri.mean()


def fitmycircle(control,xlistpoints,ylistpoints):
    print("fit_my_circle CALLED")
    import numpy as np
    from scipy import optimize
    from scipy.optimize import curve_fit
#    print('infmc ',xlistpoints,control)

    if control =='__main__':
        x_m = np.mean(xlistpoints)
        y_m = np.mean(ylistpoints)

        center_guess = x_m, y_m
#        center_guess = x_m, y_m, xlistpoints, ylistpoints
#        print(center_guess)
        center_2, ier = optimize.leastsq(f_2, center_guess, args=(xlistpoints,ylistpoints)) # works
#        center_2, ier = optimize.leastsq(f_2, center_guess)

        xc_2, yc_2 = center_2
        Ri_2 = calc_R(xc_2, yc_2,xlistpoints,ylistpoints)
        R_2 = Ri_2.mean()
        residu2 = sum((Ri_2 - R_2)**2)
        residu2_2 = sum((Ri_2**2-R_2**2)**2)
        
        return xc_2, yc_2, R_2, residu2_2
   



if __name__ == '__main__':
   print("MAIN?" , __name__)
   import sys
   import numpy as np
#   if len(str(sys.argv[1]))>0:
#       y = str(sys.argv[1])
#       print(y)
#   print('From Main')
   control = '__main__'
#   stdout_nofile = sys.stdout
#   stdout_nofile.write('Done'+'\n')



   #xlistpoints2 = np.array([1.0, -1.0, 1.0, -1.0])
   #ylistpoints2 = np.array([1.0, -1.0, -1.0, 1.0])


   x, y, R, residu2 = fitmycircle(control,xlistpoints,ylistpoints)
   print("X: " , x, " Y: " , y, " R: " , R, " RESIDU2: " , residu2)





