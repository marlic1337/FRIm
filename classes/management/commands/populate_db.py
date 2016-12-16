import re
import bs4 as bs
from urllib2 import urlopen
from classes.models import Predmet

sauce = urlopen('https://urnik.fri.uni-lj.si/timetable/fri-2016_2017-zimski-drugi-teden/').read()
soup = bs.BeautifulSoup(sauce, "html.parser")  # lxml

predmeti = False
tempID = ""
tempName = ""

for h2 in soup.find_all(['h2', 'a']):
    # contents = "".join(str(item) for item in h2.contents)
    if predmeti:
        # print(h2.get_text('a'))
        tempID = h2.get_text('a')
        tempID = tempID.rsplit()[-1]
        tempName = h2.get_text('a')
        tempName = tempName.replace(tempID, '')
        tempID = tempID.strip("()")

        sauce2 = urlopen('https://urnik.fri.uni-lj.si/timetable/fri-2016_2017-zimski-drugi-teden/allocations?subject=' + tempID).read()
        soup2 = bs.BeautifulSoup(sauce2, "html.parser")
        bvsOrUni = soup2.findAll("a", {"class": "group"})
        predmet = Predmet(predmet_id=tempID, predmet_name=tempName)

        for a in bvsOrUni:
            if "BVS" in a.get_text('a'):
                predmet.predmet_category = "VSS"
                #print("VSS")
                break
            elif "BUN" in a.get_text('a'):
                predmet.predmet_category = "UNI"
                #print("UNI")
                break
            elif "BM" in a.get_text('a'):
                predmet.predmet_category = "MAG"
                #print("MAG")
                break

        predmet.save()
        #print(tempID)
        #print(tempName)
    if "Predmeti" in h2:
        predmeti = True
