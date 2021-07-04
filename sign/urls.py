# @Time : 2021/7/1 4:49 下午
# @Author : Bais
# @Email : 17343001493@163.com
# @File : urls.py
from django.conf.urls import url
from sign import views_if
urlpatterns = [
    # ex:/api/add_event/
    url(r'^add_event/', views_if.add_event,name='add_event'),
    # ex:/api/get_event_list/
    url(r'^get_event_list/',views_if.get_event_list,name="get_event_list"),
    # ex:/api/get_event_list/
    url(r'^add_guest',views_if.add_guest,name="add_guest"),
]