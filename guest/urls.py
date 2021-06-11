
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
]
