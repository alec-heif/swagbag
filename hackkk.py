import urllib2 as urllib
import re


def parseFreebies(url, category):
    #httpstr = string of #httpstr = string of http
    x = urllib.urlopen(url)
    httpstr = x.read()
    x.close()
    #regex for relevant data
    pattern1 = '<img class="alignnone[^<>]*/>[^:]*<p>[^<>]*<a [^<>]*><strong>[^<>]*</strong></a>[^<>]*</p>'
    pattern2 = '(<img class="alignnone[^<>]*/>[^:]*<p>[^<>]*(<a [^<>]*>)?<strong>(<a [^<>]*>)?[^<>]*(</a>)?</strong>(</a>)?[^<>]*</p>)'
    pattern3 = '(<img class="alignnone[^<>]*/>[^:]*<p>[^<>]*(<a [^<>]*>)?<strong>(<a [^<>]*>)?[^<>]*(</a>)?</strong>(</a>)?[^<>]*(<a [^<>]*>[^<>]*</a>)?[^<>]*</p>)'

    items = re.findall(pattern3,httpstr)
    
    #extracting rege+x for tags
    linkex = 'href="[^"]*"'
    descex = 'FREE[^"<]*<'
    imgex = 'src="[^"]*'
    for item in items:
        item_text = ''
        if type(item)==tuple:
            item_text = item[0]
        else:
            item_text = item
        try:
            link = re.findall(linkex,item_text)[0][6:-1]
            info = re.findall(descex,item_text)[0][0:-1]
            img = re.findall(imgex,item_text)[0][5:]
        except:
            pass
        print 
        print link
        print info
        print img
    return

for i in range(1,4):
    parseFreebies('http://hunt4freebies.com/food-samples/page/'+str(i), 'Food')

