import requests
from urllib import parse
import json
import uuid
import time
import cv2
import numpy as np

vcookie = ''

def genuid():
    return str(uuid.uuid4()).replace('-', '')[0:20]

def gentimecode():
    return str(time.time()).replace('.', '')[0:15]

def replchars(strn):
    vstring = strn
    vstring.replace('%20', '+').replace('%22', '%5C%22').replace('%0A', '%5Cn')
    return vstring

def defaultheader():
    vheader = {
        'User-Agent' : ('Mozilla/5.0 (Windows NT 10.0;Win64; x64)\AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98\Safari/537.36'), 
        'accept' : ('application/json'), 
        'accept-encoding' : ('gzip, deflate, br'), 
        'accept-language' : ('ko'), 
        'content-type' : ('application/x-www-form-urlencoded; charset=UTF-8'), 
        'referer' : ('https://story.kakao.com/'), 
        'x-kakao-apilevel' : ('49'), 
        'x-kakao-deviceinfo' : ('web:d;-;-'), 
        'x-kakao-vc' : (genuid()), 
        'x-requested-with' : ('XMLHttpRequest'), 
        'cookie' : (vcookie), 
    } 
    return vheader

def writeheader(lent):
    vheader = {
        'User-Agent' : ('Mozilla/5.0 (Windows NT 10.0;Win64; x64)\AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98\Safari/537.36'), 
        'accept' : ('application/json'), 
        'accept-encoding' : ('gzip, deflate, br'), 
        'accept-language' : ('ko'), 
        'content-type' : ('application/x-www-form-urlencoded; charset=UTF-8'), 
        'content-length' : (str(len(lent))), 
        'referer' : ('https://story.kakao.com/'), 
        'x-kakao-apilevel' : ('49'), 
        'x-kakao-deviceinfo' : ('web:d;-;-'), 
        'x-kakao-vc' : (genuid()), 
        'x-requested-with' : ('XMLHttpRequest'), 
        'cookie' : (vcookie), 
    } 
    return vheader

def loadimg(iurl):
    request_headers = {
        'content-type' : ('image/jpeg')
    } 
    response = requests.get(iurl,headers = request_headers)
    if response.status_code == 200:
        img = np.asarray(bytearray(response.content), dtype='uint8')
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
        return img
    else:
        return None

def writestr(scontent,pr='F',ca=True,mr=False,sh=True,loc=None,url=None):
    string = replchars(parse.quote(json.dumps(scontent)))
    locstr = ''
    urlstr = ''
    if loc is not None:
        locstr = '&location_tag=' + replchars(parse.quote(json.dumps(loc)))
    if url is not None:
        urlstr = '&media_type=scrap&scrap_content=' + replchars(parse.quote(json.dumps(url)))
    postdata = 'content='+string+'&permission='+pr+'&comment_all_writable='+str(ca).lower()+'&is_must_read='+str(mr).lower()+'&enable_share='+str(sh).lower()+urlstr+locstr
    request_headers = writeheader(postdata)
    request_url = "https://story.kakao.com/a/activities?_="+gentimecode()
    response = requests.post(request_url, data=postdata, headers = request_headers)
    if response.status_code == 200:
        return json.loads(response.text)['sid']
    else:
        return None
    
def deletestr(sid):
    request_url = "https://story.kakao.com/a/activities/"+sid+'?_='+gentimecode()
    response = requests.delete(request_url,headers = defaultheader())
    if response.status_code == 200:
        return True
    else:
        return False
    
def setstr(sid,pr,ca=True,mr=False,sh=True):
    postdata = 'permission='+pr+'&enable_share='+str(sh).lower()+'&comment_all_writable='+str(ca).lower()+'&is_must_read='+str(mr).lower()
    request_headers = writeheader(postdata)
    request_url = "https://story.kakao.com/a/activities/"+sid+"?_="+gentimecode()
    response = requests.put(request_url, data=postdata, headers = request_headers)
    if response.status_code == 200:
        return json.loads(response.text)['sid']
    else:
        return None

def isloged():
    request_url = "https://story.kakao.com/a/settings/profile?_="+gentimecode()
    response = requests.get(request_url,headers = defaultheader())
    if response.status_code == 200:
        return True
    else:
        return False

def getinvite():
    request_url = "https://story.kakao.com/a/invitations?_="+gentimecode()
    response = requests.get(request_url,headers = defaultheader())
    vcontent = json.loads(response.text)
    invts = []
    for val in vcontent:
        if val['type'] == 'received':
            invts.append(val)
    return invts

def getprofile(uid):
    request_url = "https://story.kakao.com/a/profiles/" + uid + "?profile_only=true&_=" + gentimecode()
    response = requests.get(request_url,headers = defaultheader())
    vcontent = json.loads(response.text)
    if response.status_code == 200:
        return vcontent
    else:
        return None

def acceptinvite(uid):
    postdata = 'inviter_id='+uid+'&has_profile=true'
    request_headers = writeheader(postdata)
    request_url = "https://story.kakao.com/a/invitations/accept?_="+gentimecode()
    response = requests.post(request_url, data=postdata, headers = request_headers)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return None

def getfeed():
    request_url = "https://story.kakao.com/a/feeds?ag=false&_="+gentimecode()
    response = requests.get(request_url,headers = defaultheader())
    if response.status_code == 200:
        return json.loads(response.text)['feeds']
    return None

def hasnewfeed():
    request_url = "https://story.kakao.com/a/notifications/new_count?notice_since=&_="+gentimecode()
    response = requests.get(request_url,headers = defaultheader())
    vfeed = json.loads(response.text)
    if response.status_code != 200:
        return False
    return vfeed['has_new_feed']

def writecomment(path,content,deco=''):
    targetid = path.replace('.', '/')
    string = replchars(parse.quote(json.dumps(content)))
    decostring = replchars(parse.quote(deco))
    postdata = 'text='+decostring+'&decorators='+string
    request_headers = writeheader(postdata)
    request_url = "https://story.kakao.com/a/activities/"+targetid+"/comments?_="+gentimecode()
    response = requests.post(request_url, data=postdata, headers = request_headers)
    if response.status_code == 200:
        return True
    return False

def sharecontent(fid,scontent,pr='F',ca='true',mr='false',sh='true',loc=None):
    string = replchars(parse.quote(json.dumps(scontent)))
    locstr = ''
    if loc is not None:
        locstr = '&location_tag=' + replchars(parse.quote(json.dumps(loc)))
    postdata = 'content='+string+'&permission='+pr+'&comment_all_writable='+ca+'&is_must_read='+mr+'&enable_share='+sh+locstr
    request_headers = writeheader(postdata)
    request_url = 'https://story.kakao.com/a/activities/'+fid+'/share?_='+gentimecode()
    response = requests.post(request_url, data=postdata, headers = request_headers)
    if response.status_code == 200:
        return json.loads(response.text)['sid']
    else:
        return None

def addemotion(fid,emot):
    emcode = ['like','good','pleasure','sad','cheerup']
    postdata = 'emotion='+emcode[emot]
    request_headers = writeheader(postdata)
    request_url = 'https://story.kakao.com/a/activities/'+fid+'/like?_='+gentimecode()
    response = requests.post(request_url, data=postdata, headers = request_headers)
    if response.status_code == 200:
        return True
    return False

def getfriend():
    request_headers = defaultheader()
    request_url = "https://story.kakao.com/a/friends?_=" + gentimecode()
    response = requests.get(request_url,headers = request_headers)
    if response.status_code == 200:
        return json.loads(response.text)['profiles']
    return None

def remfriend(uid):
    request_headers = defaultheader()
    request_url = "https://story.kakao.com/a/friends/" + uid + "?_=" + gentimecode()
    response = requests.delete(request_url,headers = request_headers)
    return response.status_code

def setstatus(string):
    postdata = 'status_message='+replchars(parse.quote(string))
    request_headers = writeheader(postdata)
    request_url = 'https://story.kakao.com/a/settings/profile/status_message?_='+gentimecode()
    response = requests.put(request_url, data=postdata, headers = request_headers)
    if response.status_code == 200:
        return True
    return False

def followuser(uid):
    postdata = 'profile_id='+uid
    request_headers = writeheader(postdata)
    request_url = 'https://story.kakao.com/a/profiles/'+uid+'/follow?_='+gentimecode()
    response = requests.post(request_url, data=postdata, headers = request_headers)
    if response.status_code == 200:
        return True
    return False

def unfollowuser(uid):
    postdata = 'profile_id='+uid
    request_headers = writeheader(postdata)
    request_url = 'https://story.kakao.com/a/profiles/'+uid+'/unfollow?_='+gentimecode()
    response = requests.post(request_url, data=postdata, headers = request_headers)
    if response.status_code == 200:
        return True
    return False
