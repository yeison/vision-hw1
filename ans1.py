#!/usr/bin/env python
#Currently this program must be run from the command line.
from opencv import highgui, cv
from math import sin, cos, pi, sqrt, floor
from types import NoneType
from PageCreator import HTMLPage
import os, sys, getopt, string


def main():
    for j in [3, 5, 7]:
        for i in range(8):
            solveHWProblem((i*pi)/4, j, iA1)
            #The image produced from the function call above could be used as
            #a lookup table for the function call below.  This way, the process
            #would run much faster, but with the current implementation the
            #image below would lose 14 pixels from each edge if we were to do that.
            #If performence were a top priority, the function solveHWProblem could
            #be modified.
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
    d = checkAngle(theta)
    for i in range(scale):
        target_x = int(x + i*d*cos(theta))
        target_y = int(y + i*d*sin(theta))
        #The if statements below checks for a case on the edges where
        #rounding to an integer steps outside of the image dimentions.
        if(target_x >= image.width):
            print target_x
            target_x = int(x + floor(i*d*cos(theta)))
        if(target_y >= image.height):
            print target_y
            target_y = int(y + floor(i*d*sin(theta)))
        #print "x: %s" %  int(x + i*cos(theta))
        pxArray.append(image[target_x, target_y])
    return sum(pxArray)/scale
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
def derivativeOfIA2(x, y, theta, s):
    d = checkAngle(theta)
    return iA2(x, y, theta, s) - iA2(x-d*cos(theta), y-d*sin(theta), pi + theta, s)

dofIA2 = derivativeOfIA2

def solveHWProblem(theta, scale, function):
    #An ugly fix until we figure out how to completely index non-square images.
    if(image.width > image.height):
        width = image.height
        height = image.height
    else:
        width = image.width
        height = image.width
    dir = sys.argv[1][0:-4]
    fileName = HTML.insertImage(dir, theta/pi, scale, function.__name__)
    size = cv.cvSize(width - 2*scale , height - 2*scale)
    theta_image = cv.cvCreateImage(size, cv.IPL_DEPTH_8U, 1)
    #range(s, value): stay s pixels away from all boundaries.
    #print range(scale, image.height -scale)
    for x in range(scale-1, (width-1) - scale):
        for y in range(scale-1, (height-1) - scale): 
            if(function.__name__ == "dofIA2") :
                theta_image[x-scale, y-scale] = function(x, y, theta, scale)/2 + 128
            else:
                theta_image[x-scale, y-scale] = function(x, y, theta, scale)
    if not os.path.exists(dir):
        os.mkdir(dir)
    highgui.cvSaveImage(fileName, theta_image)
    print "finished: %s" % fileName


HTML = HTMLPage()
if __name__ == "__main__":
    main()
