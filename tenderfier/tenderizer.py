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
    img_hash = m.hexdigest()
    filename = "{}.jpg".format(img_hash)

    if not CONN.get(img_hash):
        id = CONN.llen('tenders')
        tender = {}

        tender['img'] = file_name
        tender['source'] = link
        tender['hash'] = img_hash
        tender['id'] = id

        CONN.set(id, tender)
        CONN.set(img_hash, True)
        CONN.rpush('tenders', img_hash)
        with open("".join([settings.IMG_LOCATION, filename]), "wb") as f:
            f.write(img_file)
