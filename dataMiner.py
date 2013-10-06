# coding:utf-8
import urllib2 as urllib
import re
import traceback
import json


#dictionary to enforce consistency for things that are categorized differently sometimes
catOverides = {'supplements': 'Health and Hygiene', 'haircare': 'Beauty', 'drugs': 'Health and Hygiene', 'toiletries': 'Health and Hygiene', 'skincare': 'Beauty'}
#server host name
hostName = 'http://18.189.51.151:8888/'

def parseFreebies(url, category):
    #httpstr = string of #httpstr = string of http
    x = urllib.urlopen(url+'?thissitecachespoorly=true')
    httpstr = x.read()
    x.close()

    #regex for relevant data
    pattern = '(<img class="alignnone[^<>]*>[^:]*<p>[^<>]*(<a [^<>]*>)?<strong>(<a [^<>]*>)?[^<>]*(</a>)?</strong>(</a>)?[^<>]*(<a [^<>]*>[^<>]*</a>)?[^<>]*</p>)'
    items = re.findall(pattern,httpstr)

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
            if whatsit != -1:
                item['type'] = whatsit
                if whatsit in catOverides:
                    item['category'] = catOverides[whatsit]
            data = {'urls':urls, 'item': item, 'name': info[5:]}
            response = insertDataMiner(data)
        except Exception as e:
            print e
            print traceback.format_exc()
            continue
        # if whatsit == -1:
        #     print
        #     print '~~~~~~~~~~~~~~~MISSING TYPE FOR THIS THING~~~~~~~~~~~~~~~~~~'
        #     print link
        #     print info
        #     print img
        # else:
        #     print
        #     print info
        #     print whatsit
    return

def parseFSF(url, category):
    #httpstr = string of #httpstr = string of http
    x = urllib.urlopen(url)
    httpstr = x.read()
    x.close()
    #regex for relevant data
    pattern = '(<div class="post-\d+ [^<>]*>[^!]*![^!]*![^!]*<p>)[^<]*(<img class="alignnone[^<>]*>[^:]*<p>[^<>]*(<a [^<>]*>)?(<strong>)?(<a [^<>]*>)?[^<>]*(</a>)?(</strong>)?(</a>)?[^<>]*(<a [^<>]*>[^<>]*</a>)?[^<>]*</p>)'
    items = re.findall(pattern,httpstr)
    #extracting regex for tags
    linkex = 'href="[^"]*"'
    #only match samples
    descex = '>[^<]*ample[^"<]*</a'
    imgex = 'src="[^"]*'
    for item in items:
        #check for expiration
        if item[0].find('expired')!=-1:
            continue
        item_text = ''

        if type(item)==tuple:
            item_text = item[1]
        else:
            item_text = item
        try:
            #add item
            link = re.findall(linkex,item_text)[0]
            info = re.findall(descex,item_text)[0].replace('Free ','')[1:-3]
            img = re.findall(imgex,item_text)[0]
            #dumb edge case this site has
            if info.find('ample')==0:
                info = 'S'+info
            whatsit = findType(info,category)
            #create json object
            urls = {'link':link,'img':img}
            item = {'category':category}
            if whatsit != -1:
                item['type'] = whatsit
                if whatsit in catOverides:
                    item['category'] = catOverides[whatsit]
            data = {'urls':urls, 'item': item, 'name': info[5:]}
            response = insertDataMiner(data)
        except Exception as e:
            # print e
            # print traceback.format_exc()
            continue
        # if whatsit == -1:
        #     print
        #     print '~~~~~~~~~~~~~~~MISSING TYPE FOR THIS THING~~~~~~~~~~~~~~~~~~'
        #     print link
        #     print info
        #     print img
        # else:
        #     print
        #     print info
        #     print whatsit
        #     print img
    return


def findType(description, category):
    #None for no type found
    if category == 'Food and Drink':
        return findFood(description)
    if category == 'Beauty':
        return findBeauty(description)
    if category == 'Health and Hygiene':
        return findHealth(description)
    return -1

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
    return -1    
    

def findBeauty(description):
    beauty = description.lower()
    if beauty.find('fragrance') != -1:
        return 'fragrance'

    if beauty.find('shamp') != -1 or beauty.find('conditioner') != -1 or beauty.find('hair') != -1 or beauty.find('curls') != -1:
        return 'haircare' 

    if beauty.find('cream') != -1 or beauty.find('lotion') != -1 or beauty.find('serum') != -1 or beauty.find('skin') != -1 or beauty.find('balm') != -1:
        return 'skincare'

    if beauty.find('lipstick') != -1:
        return 'cosmetics'
    
    if beauty.find('supplement') != -1:
        return 'supplement'

    if beauty.find('body wash') != -1:
        return 'toiletries'

    if health.find('relief') != -1:
        return 'drugs'

    return -1

def findHealth(description):
    health = description.lower()
    if health.find('protein') != -1 or health.find('muscle') != -1:
        return 'protein'

    if health.find('fish oil') != -1 or health.find('krill oil') != -1 or \
    health.find('vitamin') != -1 or health.find('supplement') != -1 or health.find('emergen-c') != -1 or health.find('airborn') != -1:
        return 'supplements'
    
    if health.find('shamp') != -1 or health.find('conditioner') != -1 or health.find('hair') != -1 or health.find('color') != -1 or health.find('fructis') != -1:
        return 'haircare' 

    if health.find('contact') != -1 or health.find('eye') != -1:
        return 'eyes'

    if health.find('pregnancy') != -1 or health.find('tampon') != -1 or health.find ('pad') != -1 or health.find('tena') != -1 or health.find('kotex') != -1 or health.find('feminine') != -1:
        return 'for her'

    if health.find('skincare') != -1:
        return 'skincare'

    if health.find('toothpaste') != -1 or health.find('soap') != -1 or health.find('body wash') != -1:
        return 'toiletries'

    if health.find('relief') != -1 or health.find('antacid') != -1 or health.find('tums') != -1 or health.find('pain') != -1:
        return 'drugs'
    return -1

def insertDataMiner(dictionary):
    req = urllib.Request(hostName+'freebieDataMiner')
    req.add_header('Content-Type', 'application/json')
    response = urllib.urlopen(req, json.dumps(dictionary))
    print 'inserted'
    return response

# for i in range(1,6):
#     print 'PAGE ' + str(i)
#     parseFSF('http://www.freestufffinder.com/free-skin-products/page'+str(i),'Beauty')
#     parseFSF('http://www.freestufffinder.com/free-food/page'+str(i),'Food and Drink')
# parseFSF('http://www.freestufffinder.com/free-feminine-products/', 'Health and Hygiene')
# parseFSF('http://www.freestufffinder.com/free-feminine-products/page/2', 'Health and Hygiene')


#SCRAPING

for i in range(1,6):
    print 'PAGE ' + str(i)
    parseFreebies('http://hunt4freebies.com/food-samples/page/'+str(i), 'Food and Drink')
    parseFreebies('http://hunt4freebies.com/fragrancebeauty-samples/page/'+str(i), 'Beauty')
    parseFreebies('http://hunt4freebies.com/health-hygiene-samples/page/'+str(i), 'Health and Hygiene')



##test scripts    
# hostname/bags/name
# let content be {'name': name, 'bag': ['abc', '123']}
# use name 'NOMMMMM'
# and then name 'foo'

def insertTest(name):
    d = {'name': name, 'bag': ['abc','123']}
    req = urllib.Request(hostName+'bags/'+name)
    req.add_header('Content-Type', 'application/json')
    response = urllib.urlopen(req, json.dumps(d))
    print response.data
# insertTest('NOMMMMM')
# insertTest('foo')
def deleteTest(name):
    req = urllib.Request(hostName+'bags/'+name)
    req.get_method = lambda: 'DELETE'
    response = urllib.urlopen(req)
    print response.info()
# deleteTest('NOMMMMM')
# deleteTest('foo')