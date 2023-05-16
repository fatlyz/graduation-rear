from ctypes.wintypes import tagRECT
from wsgiref import headers
import requests,json,time
#根据uid爬取b站up主信息api：  粉丝数：resp['data']['card']['fans'] 头像：resp['data']['card']['face'] 名字：resp['data']['card']['name']
#https://api.bilibili.com/x/web-interface/card?mid={uid}
#根据搜索字段找到uid 
#https://api.bilibili.com/x/web-interface/search/all/v2?keyword=杰克影视
# 若搜索到用户 则：直接在用户字典里面提取，不然在视频数据里面提取
# if resp['data']['result'][7]['data']:
#     uid = resp['data']['result'][7]['data'][0]['mid']
# else:
#     uid = resp['data']['result'][10]['data'][0]['mid']
#若视频数据里面也没有，那么从新api里面获取
# up视频播放的api:https://api.bilibili.com/x/space/arc/search?mid=120032580&ps=30&tid=0&pn=1&keyword=&order=click&jsonp=jsonp
#  mid为uid,ps为一页的视频数，order=[click(按播放量排序)，pubdate(按最新更新排序)]
# 根据视频aid查看相应视频数据:https://api.bilibili.com/archive_stat/stat?aid=626339509
# aid:视频aid  view:播放量   danmaku:弹幕数  favorite：收藏数  coin:投币数 like:点赞数  
def search_uid(search_name): #根据用户搜索字段搜搜up主的uid
    url = 'https://api.bilibili.com/x/web-interface/search/all/v2?keyword='+search_name
    head = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0"
    }
    resp = requests.get(url, headers = head)
    resp = resp.json()  #将json转为字典
    uid = 0
    if resp['data']['result'][7]['data']:
        uid = resp['data']['result'][7]['data'][0]['mid']
    else :
        if resp['data']['result'][10]['data']:
            uid = resp['data']['result'][10]['data'][0]['mid']
        else :
            url = 'https://api.bilibili.com/x/web-interface/search/type?__refresh__=true&_extra=&context=&page=1&page_size=36&order=&duration=&from_source=&from_spmid=333.337&platform=pc&highlight=1&single_column=0&keyword='+search_name+'&category_id=&search_type=bili_user&order_sort=0&user_type=0&dynamic_offset=0&preload=true&com2co=true'
            resp = requests.get(url, headers = head)
            resp = resp.json()
            uid = resp['data']['result'][0]['mid']
    return uid



def search_up_info(uid): #根据uid搜索up的信息,返回的是一个包括up主名字，头像url，粉丝数，个人介绍的字典
    url = 'https://api.bilibili.com/x/web-interface/card?mid=' + str(uid)
    head = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0"
    }
    resp = requests.get(url, headers = head)
    resp = resp.json()  #将json转为字典
    targetdict = {}
    targetdict['name'] = resp['data']['card']['name']
    targetdict['avtar'] = resp['data']['card']['face']
    targetdict['fans'] = resp['data']['card']['fans']
    targetdict['sign'] = resp['data']['card']['sign']
    return targetdict



#返回的是一个数组，数组的每个元素都包括一个视频的视频链接，视频标题，封面图片链接，播放量，点赞数，投币量和收藏量
def search_aid_videoinfo(uid,ps,order): #根据uid和用户自己定义的数据查询up视频aid以便于查取视频具体信息
    #该api已包含视频播放量，还需手动添加like:点赞量，coin:硬币数量，favorite:收藏数量
    url = 'https://api.bilibili.com/x/space/arc/search?mid='+str(uid)+'&pn=1&ps='+str(ps)+'&order='+order+'&index=1&jsonp=jsonp'
    head = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0"
    }
    resp = requests.get(url, headers = head)
    resp = resp.json()  #将json转为字典 里面有bvid负责存储bv号，视频url为https://www.bilibili.com/video/BV13v411A71s
    list = resp['data']['list']['vlist']
    res = []
    for i in list: 
        target = {}
        target['url'] = 'https://www.bilibili.com/video/' + i['bvid']
        target['title'] = i['title']
        target['img'] = i['pic']
        target['play'] = i['play']
        otherinfo = search_other_info(i['aid'])
        target['favorite'] = otherinfo['favorite']
        target['coin'] = otherinfo['coin']
        target['like'] = otherinfo['like']
        target['tag'] = 0
        res.append(target)
    return  res




def search_other_info(aid): #搜索视频额外信息
    url = 'https://api.bilibili.com/archive_stat/stat?aid=' + str(aid)
    head = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0"
    }
    
    resp = requests.get(url, headers = head)
    resp = resp.json()
    target = {}
    target['favorite'] = resp['data']['favorite']
    target['coin'] = resp['data']['coin']
    target['like'] = resp['data']['like']
    return target