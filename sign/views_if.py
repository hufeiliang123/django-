# @Time : 2021/7/1 4:50 下午
# @Author : Bais
# @Email : 17343001493@163.com
# @File : views_if.py

from django.http import JsonResponse
from sign.models import Event, Guest
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
import time


@csrf_exempt
def add_event(request):  # 添加发布会接口
    eid = request.POST.get('eid', '')
    name = request.POST.get('name', '')
    limit = request.POST.get('limit', '')
    status = request.POST.get('status', '')
    address = request.POST.get('address', '')
    start_time = request.POST.get('start_time', '')
    if eid == '' or name == '' or limit == '' or address == '' or start_time == '':
        return JsonResponse({'status': 10021, "msg": "必填不能为空"})

    result = Event.objects.filter(id=eid)
    print(result)
    if result:
        return JsonResponse({"status": 10022, "msg": "event id already exists"})

    result = Event.objects.filter(name=name)
    if result:
        return JsonResponse({"status": 10023, "msg": "event name already exists"})

    if status == "":
        status = 1
    try:
        Event.objects.create(id=eid, name=name, limit=limit, address=address, status=int(status), start_time=start_time)

    except ValidationError as e:
        error = "start_time format error. It must be in YYYY-MM-DD HH:MM:SS format."
        return JsonResponse({"status": 10024, "msg": error})

    return JsonResponse({"status": 200, "msg": "add event success"})


# 查询发布会接口
@csrf_exempt
def get_event_list(request):
    global event
    eid = request.GET.get('eid', '')
    name = request.GET.get('name', '')

    if eid == '' and name == '':
        return JsonResponse({"status": 10021, "msg": "必填参数不能为空"})

    if eid != '':
        event = dict()

        try:
            result = Event.objects.get(id=eid)
        except ObjectDoesNotExist:
            return JsonResponse({"status": 10022, "msg": "query result is empty!"})

        event["name"] = result.name
        event['limit'] = result.limit
        event['status'] = result.status
        event['address'] = result.address
        event['start_time'] = result.start_time
        return JsonResponse({"status": 200, "msg": "success", "data": event})

    if name != "":
        datas = list()
        results = Event.objects.filter(name__contains=name)
        if results:
            for ret in results:
                event = dict()
                event['name'] = ret.name
                event['limit'] = ret.limitc
                event['status'] = ret.status
                event['address'] = ret.address
                event['start_time'] = ret.start_time
                datas.append(event)
            return JsonResponse({"status": 200, "msg": "success", "data": datas})
        else:
            return JsonResponse({"status": 10022, "msg": "query result is empty!"})


# 添加嘉宾
@csrf_exempt
def add_guest(request):
    eid = request.POST.get("eid", '')  # 关联发布会id
    realname = request.POST.get("realname", '')  # 嘉宾姓名
    phone = request.POST.get("phone", '')  # 嘉宾手机号
    email = request.POST.get("email", '')  # 嘉宾邮箱

    # 判断嘉宾关联的发布会、姓名和手机号均不能为空
    if eid == '' or realname == '' or phone == '':
        return JsonResponse({"status": 10021, "msg": "必填参数不能为空！"})

    # 判断嘉宾关联的发布会是否存在
    result = Event.objects.filter(id=eid)
    if not result:
        return JsonResponse({"status": 10022, "msg": "该发布会不存在"})

    #  判断关联的发布会的状态是否为True
    result = Event.objects.get(id=eid).status
    if not result:
        return JsonResponse({"status": 10023, "msg": "event status is not available"})

    # try:
    #     result = Guest.objects.get(realname=realname)
    #     print(result)
    #     if result:
    #         return JsonResponse({"status": 10024, "msg": "该嘉宾已添加过，请勿重复添加！"})
    # except ObjectDoesNotExist:
    #     # return JsonResponse({"status": 10025, "msg": "您还没添加嘉宾呦！"})
    #     # print('可以继续运行程序')
    #     pass
    result = Guest.objects.filter(realname=realname)
    if result:
        return JsonResponse({"status": 10024, "msg": "该嘉宾已添加过，请勿重复添加！"})
    print(result)

    event_limit = Event.objects.get(id=eid).limit  # 获取发布会限制人数
    guest_limit = Guest.objects.filter(event_id=eid)  # 发布会已添加的嘉宾人数

    if len(guest_limit) >= event_limit:  # 嘉宾数是否大于发布会限制人数
        return JsonResponse({"status": 10024, "msg": "发布会添加人数已达上限！"})

    event_time = Event.objects.get(id=eid).start_time
    etime = str(event_time).split(".")[0]
    timeArray = time.strptime(etime, "%Y-%m-%d %H:%M:%S")
    e_time = int(time.mktime(timeArray))

    now_time = str(time.time())
    ntime = now_time.split(".")[0]
    n_time = int(ntime)

    if n_time >= e_time:  # 当前添加嘉宾的时间是否大于发布会开始的时间
        return JsonResponse({"status": 10025, "msg": "发布会已经开始了.."})
    try:
        Guest.objects.create(realname=realname, phone=int(phone), email=email, sign=0, event_id=int(eid))
    except IntegrityError:
        return JsonResponse({"status": 10026, "msg": "The event guest phone number repeat!"})

    return JsonResponse({"status": 200, "msg": "add guest success!"})
