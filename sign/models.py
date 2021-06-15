from django.db import models


# 发布会表
class Event(models.Model):
    name = models.CharField(max_length=100)
    limit = models.IntegerField()
    status = models.BooleanField()
    address = models.CharField(max_length=200)
    start_time = models.DateTimeField('event_time')
    create_time = models.DateTimeField(auto_now=True)  # 创建时间，自动获取当前时间

    def __str__(self):
        return self.name


# 嘉宾表
class Guest(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)  # 关联发布会id
    realname = models.CharField(max_length=64)  # 姓名
    phone = models.CharField(max_length=16)
    email = models.EmailField()
    sign = models.BooleanField()  # 签到状态
    create_time = models.DateTimeField(auto_now=True)  # 创建时间，自动获取当前时间


class Meta:
    unique_together = ('event', 'phone')


def __str__(self):
    return self.realname
