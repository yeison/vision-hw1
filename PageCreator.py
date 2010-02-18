from BeautifulSoup import BeautifulSoup, Tag, NavigableString
import os

class HTMLPage:
    

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
        soup = BeautifulSoup(self.html)
        print soup('td')[2]
            

page = HTMLPage()
