import re
import hashlib
import urllib2
import sys
sys.path.append("../")
from tenders import *
import settings

response = urllib2.urlopen("http://www.flickr.com/search/?q=chicken%20tenders")
html = response.read()

pics = re.findall('(http://[^"]*\.jpg)', html)

for link in pics:
    img = urllib2.urlopen(link)
    img_file = img.read()
    m = hashlib.md5(img_file)
    img_hash = m.hexdigest()[:5]
    filename = "{}.jpg".format(img_hash)

    if not_tendered(img_hash):
        tender = {}
        tender['img'] = filename
        tender['source'] = link
        tender['id'] = img_hash

        add_tender(tender)
        with open("".join([settings.IMG_LOCATION, filename]), "wb") as f:
            f.write(img_file)
