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
        
        if not soup.find(id=original): 
            soup.body.insert(0, table)
            table['id'] = original

        name_angle = "%s%s" % (original, angle) 
        if not soup.find(id=name_angle):
            soup.find(id=original).insert(0, tr)
            tr['id'] = name_angle
            
        angle_scale_function = "%s-%s%s" % (name_angle, scale, function)
        if not soup.find(id=angle_scale_function):
            soup.find(id=name_angle).insert(0, td)
            td['id'] = angle_scale_function

        td.insert(0, img)
        fileName = "%s/theta%spi_s%s_%s.jpg" % (original, angle, scale, function)
        img['src'] = fileName
        
        file = open(self.pageName, 'w')
        file.write(soup.prettify())
        file.close()

        return fileName


    def newHtml(self, pageName):
        file = open(pageName, 'w')
        html = "\
<html>\n\
  <head>\n\
  </head>\n\
  <body>\n\
  </body>\n\
</html>"
        file.write(html)
        file.close()

    def __init__(self, pageName="vishw1.html"):
        self.pageName = pageName
        if not os.path.exists(pageName):
           self.newHtml(pageName)
        file = open(pageName, 'r')
        html = file.read()
        file.close()
        self.soup = BeautifulSoup(html)
