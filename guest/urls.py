
from django.contrib import admin
from django.conf.urls import url
from sign import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/$',views.index),
    url(r'^login_action/$',views.login_action),
    url(r'^event_manage/$',views.event_manage),
    url(r'^accounts/login/$',views.index),
    url(r'^$',views.index),
    url(r'^search_name/$',views.search_name),
    url(r'^guest_manage/$',views.guest_manage),
    url(r'^search_realname/$',views.search_realname),
    url(r'^sign_index/(?P<eid>[0-9]+)/$',views.sign_index)
]
