#!/usr/bin/env python
#Currently this program must be run from the command line.
from opencv import highgui, cv
from math import sin, cos, pi, sqrt
from types import NoneType
import os, sys, getopt, string


def main():
    for j in [3, 5, 7]:
        for i in range(8):
            solveHWProblem((i*pi)/4, j, iA1)
            solveHWProblem((i*pi)/4, j, iA2)
        for i in range(4):
            solveHWProblem((i*pi)/4, j, dofIA2)

        
#Open the image, and assign it to the global variable image.
try:
    image = highgui.cvLoadImage(sys.argv[1], highgui.CV_LOAD_IMAGE_GRAYSCALE)
    if(type(image) == NoneType):
        print >> sys.stderr, "  The filename provided does not exist."
        sys.exit(1)
except IndexError as e:
    print >> sys.stderr, "  Please provide the name of a local image."
    sys.exit(1)


#Determines if the angle is diagonal with respect to the x or y axes.
def checkAngle(theta):
    if((theta*2)/pi == int((theta*2)/pi)):
        return 1
    else:
        return sqrt(2) 


def intensityAccum1(x, y, theta, scale):
#Pixel value array
    pxArray = []
    sum = 0
    d = checkAngle(theta)
    for i in range(scale):
        #print "x: %s" %  int(x + i*cos(theta))
        pxArray.append(image[int(x + i*d*cos(theta)), int(y + i*d*sin(theta))])
    #There's probably an easy way to average an array in py
    for i in range(scale):
        sum += pxArray[i]
    return (sum/scale)
#Shorten the function name
iA1 = intensityAccum1


def intensityAccum2(x, y, theta, s):
    d = checkAngle(theta)
    if(d == 1): #If theta is along a straight line.
        term1 = iA1(x, y, theta, s)
        term2 = iA1(x+d*cos(theta), y+d*sin(theta), theta, s)
        term3 = iA1(x-d*sin(theta), y+d*cos(theta), theta, s)
        term4 = iA1(x+d*sin(theta), y-d*cos(theta), theta, s)
        ia2 = (term1 + term2 + term3 + term4)/4
        return ia2
    else:       #If theta is along a diagonal.
        term1 = iA1(x, y, theta, s)
        term2 = iA1(x+d*cos(theta), y+d*sin(theta), theta, s)
        term3 = iA1(x, y+d*sin(theta), theta, s)
        term4 = iA1(x+d*cos(theta), y, theta, s)
        ia2 = (term1 + term2 + term3 + term4)/4
        return ia2
#Shorten function name
iA2 = intensityAccum2

#Derivative of iA2 along angle theta.
def dofIA2(x, y, theta, s):
    d = checkAngle(theta)
    return iA2(x, y, theta, s) - iA2(x-d*cos(theta), y-d*sin(theta), pi + theta, s)


thetaPxArray = []
def solveHWProblem(theta, scale, function):
    dir = sys.argv[1][0:-4]
    fileName = "%s/theta%spi_s%s_%s.jpg" % (dir, theta/pi, scale, function.__name__)
    size = cv.cvSize(image.width - 2*scale , image.height - 2*scale)
    theta_image = cv.cvCreateImage(size, cv.IPL_DEPTH_8U, 1)
    #range(s, value): stay s pixels away from all boundaries.
    #print range(scale, image.height -scale)
    for y in range(scale, image.height - scale):
        for x in range(scale, image.width - scale):
            if(function.__name__ == "dofIA2") :
                theta_image[x-scale, y-scale] = function(x, y, theta, scale)/2 + 128
            else:
                theta_image[x-scale, y-scale] = function(x, y, theta, scale)
            #if(image[x, y] > 0 and image[x, y] < 255):
    if not os.path.exists(dir):
        os.mkdir(dir)
    highgui.cvSaveImage(fileName, theta_image)
    print "finished: %s" % fileName

#for i in range(8):
#    solveHWProblem((i*pi)/4, 5)

if __name__ == "__main__":
    main()
