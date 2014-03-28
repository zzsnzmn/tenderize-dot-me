import re
import urllib2

response = urllib2.urlopen("http://www.flickr.com/search/?q=chicken%20tenders")
html = response.read()

files = re.findall('(http://[^"]*\.jpg)', html)

for item in enumerate(files):
    with open("images/{}.jpg".format(item[0]), "wb") as f:
        image = urllib2.urlopen(item[1])
        f.write(image.read())
