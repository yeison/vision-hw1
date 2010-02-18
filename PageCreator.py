from BeautifulSoup import BeautifulSoup, Tag, NavigableString
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
            
        angle_scale_function = "%s%s%s" % (name_angle, scale, function)
        if not soup.find(id=angle_scale):
            soup.find(id=name_angle).insert(0, td)
            td['id'] = angle_scale_function

        td.insert(0, img)
        


    def newHtml(self, pageName):
        file = open(pageName, 'w')
        html = "\
<html>\n\
  <head>\n\
  </head>\n\
  <body>\n\
    <table>\n\
      <td id=row0></td>\n\
      <td id=row1></td>\n\
      <td id=row2></td>\n\
      <td id=row3></td>\n\
      <td id=row4></td>\n\
      <td id=row5></td>\n\
      <td id=row6></td>\n\
      <td id=row7></td>\n\
    </table>\n\
  </body>\n\
</html>"
        file.write(html)
        file.close()

    def __init__(self, pageName="vishw1.html"):
        if not os.path.exists(pageName):
           self.newHtml(pageName)
        self.file = open(pageName, 'rw')
        self.html = self.file.read()
        self.soup = BeautifulSoup(self.html)
        img = Tag(self.soup, "img")
        img['src'] = "http//word"
        self.soup('td')[2].insert(0, img)
        img = Tag(self.soup, "img")
        self.soup('td')[2].insert(0, img)
        this = "str1"
        that = "str2"
        print "%s%s" % (this, that)
        

            

page = HTMLPage()
