#!/usr/bin/env python
from opencv import highgui
from opencv import cv
from math import sin, cos
import sys, getopt

#Scale
s = 3
printArrayI = []
printArray0 = []

image = highgui.cvLoadImage("circle.jpg", highgui.CV_LOAD_IMAGE_GRAYSCALE)


def setScale(scale):
    s = scale

#myX and myY represent the calling pixel's location.
def getPixelValues(x, y, theta, scale):
#Pixel value array
    pxArray = []
    sum = 0
    for i in range(scale):
        #print "x: %s" %  int(x + i*cos(theta))
        pxArray.append(image[int(x + i*cos(theta)), int(y + i*sin(theta))])
    #There's probably an easy way to average an array in py
    for i in range(scale):
        sum += pxArray[i]
    return (sum/s)


#For theta = 0
setScale(7)
size = cv.cvSize(image.width, image.height)
theta0_image = cv.cvCreateImage(size, cv.IPL_DEPTH_8U, 1)
for y in range(image.height):
    for x in range(image.width - s):
        theta0_image[x, y] =  getPixelValues(x, y, 0, s)
        if(image[x, y] > 0 and image[x, y] < 255):
            printArrayI.append( image[x, y])
            printArray0.append( theta0_image[x, y] ) 



highgui.cvSaveImage("theta0.jpg", theta0_image)
