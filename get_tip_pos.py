def gettippos(control,imagein):
    import numpy as np
    import statistics
    import argparse
    import cv2
# load the image, clone it for output, and then convert it to grayscale
    if control == '__main__' :
        image = cv2.imread(imagein)
        output = image.copy()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# detect circles in the image
        listX = []
        listY = []
        listR = []
        ilistIndex = 0
        for dp10 in range(20,27):
            circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp10/10, minDist = 3000, param1 = 100, param2 = 0.985, minRadius = 20, maxRadius = 75) 
            if circles is not None:
# convert the (x, y) coordinates and radius of the circles to integers
                circles = np.round(circles[0, :]).astype("int")
#                print("{0} => {1} Circles found!".format(dp10/10,len(circles)))
# loop over the (x, y) coordinates and radius of the circles
                for (x, y, r) in circles:
                    listX.append(x)
                    listY.append(y)
                    listR.append(r)
                    ilistIndex=ilistIndex+1
# Select answer among possible solutionis using median
        if ilistIndex > 0: 
            medianListX = statistics.median(listX)
            medianListY = statistics.median(listY)
            medianListR = statistics.median(listR)
# draw the circle in the output image, then draw a rectangle corresponding to the center of the circle
            cv2.circle(output, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
            cv2.imwrite('ana-'+imagein,output) # store the output image
        else:
            medianListX = -1
            medianListY = -1
            medianListR = -1

#        print('Results ',ilistIndex)

        return medianListX, medianListY, medianListR, ilistIndex, output

if __name__ == '__main__':
   import sys
   if len(str(sys.argv[1]))>0:
       imagein = str(sys.argv[1])
       print("IMAGEIN: ", imagein)
#   print('From Main')
   x = '__main__'
#   stdout_nofile = sys.stdout
#   stdout_nofile.write('Done'+'\n')
   XM, YM, RM, N, OUT = gettippos(x,imagein)
   print('X, Y, R, Solutions = ',XM,YM,RM,N, OUT)
