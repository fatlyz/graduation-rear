#对数据库的增删改查
from calendar import month
from .models import *
from .pachong import *
from datetime import date
def update_user_up(user,searchname):#更新的同时判断如果是新用户则插入
    User.objects.get(username = user).update(tag = 1)
    ups = []
    flag = 0
    check =  user_up.objects.all()
    for i in check:
        if i.username == user :
            flag = 1
    if flag:
        flag1 = 0
        old_user_up = user_up.objects.get(username = user)
        for i in old_user_up.name:
            ups.append(i)
            if i == searchname:
                flag1 = 1
        if flag1 == 0:
            ups.append(searchname)
        else: 
            return 0
        user_up.objects.filter(username = user).update(name = ups)
    else:
        ups.append(searchname)
        create = user_up(username = user,name = ups)
        create.save()
    User.objects.get(username = user).update(tag = 0)
    return 1

def getold_upinfo(search_name,search_up,order):
    res = {}
    uid = search_uid(search_up)
    upinfo = search_up_info(uid)
    update_user_up(search_name,upinfo['name'])
    print(upinfo['name'])
    if not up_info.objects.filter(name = upinfo['name']):
        nosql = '数据库中没有信息，请先更新数据'
        return nosql
    else:
        res = take_upinfo(upinfo['name'],order)
    return res

def save_upinfo(uid,upinfo,videoinfo,order):
    if order == 'click':
        old_upinfo = up_info.objects.all()
        flag = 0
        fansflag = 0
        datein = date(year = date.today().year,month = date.today().month,day = date.today().day)
        for i in old_upinfo:
            if i.name == upinfo['name']:
                flag = 1    #标识upinfo表里面有改up往期信息，则进行更新
                break
        if flag:  #更新操作
            
            datefan = datefans(fannum = upinfo['fans'],date = datein)
            newfansinfo = []
            for i in up_info.objects.get(name = upinfo['name']).fansinfo:
                if datein != i.date:
                    newfansinfo.append(i)
                else :
                    newfansinfo.append(datefan)
                    fansflag = 1 
            if fansflag: newfansinfo.append(datefan)
            up_info.objects.get(name = upinfo['name']).update( fansinfo = newfansinfo,clickvideoinfo = videoinfo)
        else:
            datefan = datefans(fannum = upinfo['fans'],date = datein)
            newfansinfo = []
            newfansinfo.append(datefan)
            up_info(uid = uid,name =upinfo['name'],avtar =upinfo['avtar'],up_sign =upinfo['sign'],fansinfo =newfansinfo,clickvideoinfo = videoinfo).save()
        print('更新成功')
        return 1
    else:
        old_upinfo = up_info.objects.all()
        flag = 0
        datein = date(year = date.today().year,month = date.today().month,day = date.today().day)
        for i in old_upinfo:
            if i.name == upinfo['name']:
                flag = 1    #标识upinfo表里面有改up往期信息，则进行更新
                break
        if flag:  #更新操作
            
            datefan = datefans(fannum = upinfo['fans'],date = datein)
            newfansinfo = []
            for i in up_info.objects.get(name = upinfo['name']).fansinfo:
                    newfansinfo.append(i)
            newfansinfo.append(datefan)
            up_info.objects.get(name = upinfo['name']).update( fansinfo = newfansinfo,updatevideoinfo = videoinfo)
        else:
            datefan = datefans(fannum = upinfo['fans'],date = datein)
            newfansinfo = []
            newfansinfo.append(datefan)
            up_info(uid = uid,name =upinfo['name'],avtar =upinfo['avtar'],up_sign =upinfo['sign'],fansinfo =newfansinfo,updatevideoinfo = videoinfo).save()
        print('更新成功')
        return 1


def take_upinfo(upname,order):
    if order == 'click':
        res = {}
        takeinfo = {}
        info =  up_info.objects.get(name = upname)
        res['uid'] = info['uid']
        res['name'] = info['name']
        res['avtar'] = info['avtar']
        res['up_sign'] = info['up_sign']
        res['fansinfo'] = []
        res['videoinfo'] = []
        for i in info['fansinfo']:
            takeinfo = {}
            datee = str(i['date'])
            takeinfo['date'] = datee
            takeinfo['fannum'] = i['fannum']
            res['fansinfo'].append(takeinfo)
        for i in info['clickvideoinfo']:
            takeinfo = {}
            takeinfo['title'] = i['title']
            takeinfo['play'] = i['play']
            takeinfo['url'] = i['url']
            takeinfo['img'] = i['img']
            takeinfo['like'] = i['like']
            takeinfo['coin'] = i['coin']
            takeinfo['favorite'] = i['favorite']
            takeinfo['tag'] = i['tag']
            res['videoinfo'].append(takeinfo)
        return res
    else:
        res = {}
        takeinfo = {}
        info =  up_info.objects.get(name = upname)
        res['uid'] = info['uid']
        res['name'] = info['name']
        res['avtar'] = info['avtar']
        res['up_sign'] = info['up_sign']
        res['fansinfo'] = []
        res['videoinfo'] = []
        for i in info['fansinfo']:
            takeinfo = {}
            datee = str(i['date'])
            takeinfo['date'] = datee
            takeinfo['fannum'] = i['fannum']
            res['fansinfo'].append(takeinfo)
        for i in info['updatevideoinfo']:
            takeinfo = {}
            takeinfo['title'] = i['title']
            takeinfo['play'] = i['play']
            takeinfo['url'] = i['url']
            takeinfo['img'] = i['img']
            takeinfo['like'] = i['like']
            takeinfo['coin'] = i['coin']
            takeinfo['favorite'] = i['favorite']
            takeinfo['tag'] = i['tag']
            res['videoinfo'].append(takeinfo)
        return res

def getuserup(username):
    uplist = []
    for i in user_up.objects.get(username = username).name:
        uplist.append(i)
    return uplist