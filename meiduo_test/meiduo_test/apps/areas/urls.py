from django.conf.urls import url

from areas import views

urlpatterns = [
    # url(r'^index/', admin.index),
    url(r'^areas/$', views.AreasView.as_view())
]
