import urllib2 as urllib
import re
import traceback
import json

#dictionary to enforce consistency for things that are categorized differently sometimes
catOverides = {'supplements': 'Health & Hygiene', 'haircare': 'Health & Hygiene'}
#server host name
hostName = 'http://18.111.93.186:8888/'

def parseFreebies(url, category):
    #httpstr = string of #httpstr = string of http
    x = urllib.urlopen(url+'?thissitecachespoorly=true')
    httpstr = x.read()
    x.close()

    #regex for relevant data
    pattern1 = '<img class="alignnone[^<>]*/>[^:]*<p>[^<>]*<a [^<>]*><strong>[^<>]*</strong></a>[^<>]*</p>'
    pattern2 = '(<img class="alignnone[^<>]*/>[^:]*<p>[^<>]*(<a [^<>]*>)?<strong>(<a [^<>]*>)?[^<>]*(</a>)?</strong>(</a>)?[^<>]*</p>)'
    pattern3 = '(<img class="alignnone[^<>]*>[^:]*<p>[^<>]*(<a [^<>]*>)?<strong>(<a [^<>]*>)?[^<>]*(</a>)?</strong>(</a>)?[^<>]*(<a [^<>]*>[^<>]*</a>)?[^<>]*</p>)'
    
    items = re.findall(pattern3,httpstr)

    #extracting regex for tags
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
            #add item
            link = re.findall(linkex,item_text)[0][6:-1]
            info = re.findall(descex,item_text)[0][0:-1]
            img = re.findall(imgex,item_text)[0][5:]
            whatsit = findType(info,category)
            urls = {'link':link,'img':img}
            item = {'category':category}
            if whatsit != None:
                item['type'] = whatsit
                if whatsit in catOverides:
                    item['category'] = catOverides[whatsit]
            data = {'urls':urls, 'item': item, 'name': info[5:]}
            print data
            print insertDB(data)
        except Exception as e:
            print e
            print traceback.format_exc()
            continue
        if whatsit == None:
            print
            print '~~~~~~~~~~~~~~~MISSING TYPE FOR THIS THING~~~~~~~~~~~~~~~~~~'
            print link
            print info
            print img
        print
        print info
        print whatsit
    return

def findType(description, category):
    #None for no type found
    if category == 'Food & Drink':
        return findFood(description)
    if category == 'Beauty':
        return findBeauty(description)
    if category == 'Health & Hygiene':
        return findHealth(description)


def findFood(description):
    food = description.lower()
    if food.find('coffee') != -1 or food.find('latte') != -1:
        return 'coffee'

    if food.find('sweetener') != -1:
        return 'sweetener'

    if food.find('water') != -1 or food.find('juice') != -1 or food.find('shake') != -1 or food.find('powder') != -1:
        return 'beverage'

    if food.find('vitamin') != -1:
        return 'supplements'

    if food.find(' bar') != -1 or food.find(' chips') != -1 or food.find('yogurt') != -1:
        return 'snacks'

    if food.find('seasoning') != -1:
        return 'seasoning'

    if food.find('tea') != -1 or food.find('snapple') != -1:
        return 'tea'

    #cereal? yoghurt?
    
    

def findBeauty(description):
    beauty = description.lower()
    if beauty.find('fragrance') != -1:
        return 'fragrance'

    if beauty.find('shampoo') != -1 or beauty.find('conditioner') != -1 or beauty.find('hair') != -1 or beauty.find('curls') != -1:
        return 'haircare' 

    if beauty.find('cream') != -1 or beauty.find('lotion') != -1 or beauty.find('serum') != -1:
        return 'skincare'

    if beauty.find('lipstick') != -1:
        return 'cosmetics'

def findHealth(description):
    health = description.lower()
    if health.find('protein') != -1 or health.find('muscle') != -1:
        return 'protein'

    if health.find('fish oil') != -1 or health.find('krill oil') != -1 or \
    health.find('vitamin') != -1 or health.find('supplement') != -1 or health.find('emergen-c') != -1 or health.find('airborn') != -1:
        return 'supplements'
    
    if health.find('shampoo') != -1 or health.find('conditioner') != -1 or health.find('hair') != -1:
        return 'haircare' 

    if health.find('contact') != -1 or health.find('eye') != -1:
        return 'eyes'

    if health.find('tampon') != -1 or health.find ('pad') != -1 or health.find('tena') != -1:
        return 'for her'

def insertDB(dictionary):
    req = urllib.Request(hostName+'freebieDataMiner')
    req.add_header('Content-Type', 'application/json')
    response = urllib.urlopen(req, json.dumps(dictionary))
    return response


for i in range(1,3):
    print 'PAGE ' + str(i)
    parseFreebies('http://hunt4freebies.com/food-samples/page/'+str(i), 'Food & Drink')
    parseFreebies('http://hunt4freebies.com/fragrancebeauty-samples/page/'+str(i), 'Beauty')
    parseFreebies('http://hunt4freebies.com/health-hygiene-samples/page/'+str(i), 'Health & Hygiene')