from BeautifulSoup import BeautifulSoup, Tag, NavigableString
from math import pi
import os

class HTMLPage:
    def insertImage(self, original, angle, scale, function):
        soup = self.soup
        table = Tag(soup, "table")
        tr = Tag(soup, "tr")
        td = Tag(soup, "td")
        img = Tag(soup, "img")
        
        if not soup.find(id=function): 
            soup.body.insert(0, table)
            table['id'] = function
            heading = NavigableString(function)
            h2 = Tag(soup, "h2")
            h2.insert(0, heading)
            table.insert(0, h2)

        function_scale = "function:%s_scale:%s" % (function, scale) 
        if not soup.find(id=function_scale):
            soup.find(id=function).insert(0, tr)
            tr['id'] = function_scale
            scaleString = NavigableString("%s" % scale)
            h3 = Tag(soup, "h2")
            h3.insert(0, scaleString)
            soup.find(id=function).insert(0, h3)
            
        scale_angle = "%s-%s" % (function_scale, angle)
        if not soup.find(id=scale_angle):
            soup.find(id=function_scale).insert(0, td)
            td['id'] = scale_angle
            tr['th'] = scale_angle

        td.insert(0, img)
        fileName = "%s/theta%spi_s%s_%s.jpg" % (original, angle, scale, function)
        img['src'] = fileName
        
        pageName = "%s.html" % original
        file = open(pageName, 'w')
        file.write(soup.prettify())
        file.close()

        return fileName


    def __init__(self):
        file = open("template", 'r')
        html = file.read()
        self.soup = BeautifulSoup(html)
