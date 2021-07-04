from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event, Guest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

def index(request):
    return render(request, 'index.html')


# 登录动作

def login_action(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        # if username == "admin" and password == "admin123":
        if user is not None:
            auth.login(request, user)  # 登录
            response = HttpResponseRedirect('/event_manage/')
            # response.set_cookie('user', username, 3600)  # 添加浏览器cookie
            request.session['user'] = username  # 将session 信息记录到浏览器
            return response
        else:
            return JsonResponse({"status": 10001, "msg": "用户名或密码错误 !"})
            # return render(request, 'index.html', {'error': 'username or password error !'})


# 发布会管理
@login_required
def event_manage(request):
    # username = request.COOKIES.get('user', '')  # 读取浏览器cookie
    username = request.session.get('user', '')  # 读取浏览器session
    event_list = Event.objects.all()
    return render(request, 'event_manage.html', {"user": username, "events": event_list})


# 发布会名称搜索
@login_required
def search_name(request):
    username = request.session.get('user', '')
    print(username)
    search_name = request.GET.get('name', "")
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, "event_manage.html", {"user": username, "events": event_list})


# 嘉宾管理
@login_required
def guest_manage(request):
    username = request.session.get('user', '')
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list, 10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'guest_manage.html', {"user": username, "guests": contacts})


# 嘉宾搜索
@login_required
def search_realname(request):
    username = request.session.get('user', '')
    search_realname = request.GET.get('realname', "")
    guest_list = Guest.objects.filter(realname__contains=search_realname)
    return render(request, "guest_manage.html", {"user": username, "guests": guest_list})


# 签到页面
@login_required
def sign_index(request, eid):
    print("---1------")
    event = get_object_or_404(Event, id=eid)
    print("---2------")
    return render(request, 'sign_index.html', {'event': event})


# 签到功能
@login_required
def sign_index_action(request, eid):
    print('----3-----')
    event = get_object_or_404(Event, id=eid)
    print('----4-----')
    phone = request.POST.get('phone', '')
    print(phone)
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, 'sign_index.html', {
            "event": event, 'hint': "phone error"})

    result = Guest.objects.filter(phone=phone, event_id=eid)
    if not result:
        return render(request, 'sign_index.html', {
            'event': event, 'hint': 'event id or phone error'})

    result = Guest.objects.filter(phone=phone, event_id=eid)
    if result.sign:
        return render(request, 'sign_index.html', {
            'event': event, 'hint': 'user has signed!'})

    else:
        Guest.objects.filter(phone=phone, event_id=eid).update(sign='1')
        return render(request, 'sign_index.html', {'event': event,
                                                   "hint": 'sign success!',
                                                   'guest': result

                                                   })


# 退出登录
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/index')
