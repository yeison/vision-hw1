#!/usr/bin/env python
from opencv import highgui
from opencv import cv
from math import sin, cos
from math import pi
from math import sqrt
import sys, getopt


image = highgui.cvLoadImage("circle.jpg", highgui.CV_LOAD_IMAGE_GRAYSCALE)


#myX and myY represent the calling pixel's location.
def getPixelValues(x, y, theta, scale):
#Pixel value array
    pxArray = []
    sum = 0
    if((theta*2)/pi == int((theta*2)/pi)):
        d = 1
    else:
        d = sqrt(2) 
    
    for i in range(scale):
        #print "x: %s" %  int(x + i*cos(theta))
        pxArray.append(image[int(x + i*d*cos(theta)), int(y + i*d*sin(theta))])
    #There's probably an easy way to average an array in py
    for i in range(scale):
        sum += pxArray[i]
    return (sum/scale)


def solveHWProblem(theta, scale):
    fileName = "theta%s_s%s.jpg" % (theta, scale)
    size = cv.cvSize(image.width - 2*scale , image.height - 2*scale)
    theta_image = cv.cvCreateImage(size, cv.IPL_DEPTH_8U, 1)
    #range(s, value): stay s pixels away from all boundaries.
    #print range(scale, image.height -scale)
    for y in range(scale, image.height - scale):
        for x in range(scale, image.width - scale):
            theta_image[x-scale, y-scale] =  getPixelValues(x, y, theta, scale)
            #if(image[x, y] > 0 and image[x, y] < 255):

    
    highgui.cvSaveImage(fileName, theta_image)

for i in range(8):
    solveHWProblem((i*pi)/4, 5)
