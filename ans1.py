#!/usr/bin/env python
from opencv import highgui, cv
from math import sin, cos, pi, sqrt
import sys, getopt


image = highgui.cvLoadImage("circle.jpg", highgui.CV_LOAD_IMAGE_GRAYSCALE)

#Determines if the angle is diagonal from the origin.
def checkAngle(theta):
    if((theta*2)/pi == int((theta*2)/pi)):
        return 1
    else:
        return sqrt(2) 


def getPixelValues(x, y, theta, scale):
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
iA1 = intensityAccum1 = getPixelValues

def intensityAccum2(x, y, theta, s):
    d = checkAngle(theta)
    if(d == 1):
        return 1/4*(iA1(x, y, theta, s) + iA1(x+d*cos(theta), y+d*sin(theta), theta, s) + iA1(x-d*sin(theta), y+d*cos(theta), theta, s) + iA1(x+d*sin(theta), y-d*sin(theta), theta, s))
    else:
        return 1/4*(iA1(x, y, theta, s) + iA1(x+d*cos(theta), y+d*sin(theta), theta, s) + iA1(x, y+d*sin(theta), theta, s) + iA1(x+d*cos(theta), y, theta, s))

iA2 = intensityAccum2

def solveHWProblem(theta, scale, function):
    fileName = "theta%s_s%s_%s.jpg" % (theta, scale, function)
    size = cv.cvSize(image.width - 2*scale , image.height - 2*scale)
    theta_image = cv.cvCreateImage(size, cv.IPL_DEPTH_8U, 1)
    #range(s, value): stay s pixels away from all boundaries.
    #print range(scale, image.height -scale)
    for y in range(scale, image.height - scale):
        for x in range(scale, image.width - scale):
            theta_image[x-scale, y-scale] =  function(x, y, theta, scale)
            #if(image[x, y] > 0 and image[x, y] < 255):

    
    highgui.cvSaveImage(fileName, theta_image)

#for i in range(8):
#    solveHWProblem((i*pi)/4, 5)


solveHWProblem(0, 3, iA2)
