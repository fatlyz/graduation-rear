from ast import dump
import json
from sre_constants import SUCCESS
from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.
from .pachong import *
import json
from django.core import serializers
from .oprate import *
# ne - 不相等
# lt - 小于
# lte - 小于等于
# gt - 大于
# gte - 大于等于
# not - 取反
# in - 值在列表中
# nin - 值不在列表中
# mod - 取模
# all - 与列表的值相同
# size - 数组的大小
# exists - 字段的值存在
def login(request):#登录功能
    if request.method == 'POST':
        user = request.POST.get('username')
        password = request.POST.get('password')
    if request.method == 'GET':
        user = request.GET.get('username')
        password = request.GET.get('password')
    for i in User.objects:
        if user == i.username:
            if password == i.password:
                print ('登录成功')
                return HttpResponse(1)
            else:
                print ('用户密码输入错误')
                return HttpResponse('密码错误，请重新输入')
            break
    print ('用户未注册')
    return HttpResponse('用户未注册，请先注册')
    
    

def register(request):  #注册操作
    if request.method == 'POST':
        user = request.POST.get('username')
        password = request.POST.get('password')
    if request.method == 'GET':
        user = request.GET.get('username')
        password = request.GET.get('password')
    check = User.objects.all()
    for i in check:
        if user == i.username:
            return HttpResponse('该用户名已被注册')
    users = User(username = user,password = password,tag = 0)
    users.save()
    return HttpResponse(1)

def search(request):
    #根据前端传的数据（数据包括用户名和所搜索up名）进行爬虫搜索，爬取成功则加入数据库
    if request.method == 'POST':                #获取搜索头
        search_name = request.POST.get('username')
        search_up = request.POST.get('uptest')
        order = request.POST.get('order')
    if request.method == 'GET':
        search_name = request.GET.get('username')
        search_up = request.GET.get('uptest')
        order = request.GET.get('order')
    uid = search_uid(search_up)
    upinfo = search_up_info(uid)
    update_user_up(search_name,upinfo['name'])#update_user_up()函数返回是1则修改添加成功，0则表示搜索对象在搜索列表里
        
    videoinfo = search_aid_videoinfo(uid,10,'click')
    # save——upinfo()函数的功能是根据uid和已经爬取到的upinfo来进行数据的存储
    save_upinfo(uid,upinfo,videoinfo,'click') #这个函数处理up信息个up视频信息
    videoinfo = search_aid_videoinfo(uid,10,'update')
    # save——upinfo()函数的功能是根据uid和已经爬取到的upinfo来进行数据的存储
    save_upinfo(uid,upinfo,videoinfo,'update')
    res = take_upinfo(upinfo['name'],order)
    res = json.dumps(res,ensure_ascii=False)
    return HttpResponse(res)

def getinfo(request):   #从数据库中取未更新数据
    if request.method == 'POST':                #获取搜索头
        search_name = request.POST.get('username')
        search_up = request.POST.get('uptest')
        order = request.POST.get('order')
        # search_order = request.POST.get('order')
    if request.method == 'GET':
        search_name = request.GET.get('username')
        search_up = request.GET.get('uptest')
        order = request.GET.get('order')
    res = getold_upinfo(search_name,search_up,order)
    res = json.dumps(res,ensure_ascii=False)
    return HttpResponse(res)

def getuplist(request):
    if request.method == 'POST':                
        name = request.POST.get('username')
    if request.method == 'GET':
        name = request.GET.get('username')
    res = getuserup(name)
    res = json.dumps(res,ensure_ascii=False)
    return HttpResponse(res)