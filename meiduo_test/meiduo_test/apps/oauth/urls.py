from django.conf.urls import url

from oauth import views

urlpatterns = [
    url(r'^qq/authorization/$', views.QQAuthUserView.as_view()),
]
