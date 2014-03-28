import re
import hashlib
import urllib2
import sys
sys.path.append("../")
from tenders import *

response = urllib2.urlopen("http://www.flickr.com/search/?q=chicken%20tenders")
html = response.read()

files = re.findall('(http://[^"]*\.jpg)', html)

for item in files:
    img = urllib2.urlopen(item)
    img_file = img.read()
    m = hashlib.md5(img_file)
    img_hash = m.hexdigest()
    if not CONN.get(img_hash):
        CONN.set(img_hash, True)
    with open("images/{}.jpg".format(img_hash), "wb") as f:
        f.write(img_file)
