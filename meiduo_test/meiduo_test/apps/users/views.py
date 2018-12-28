from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response

from rest_framework.views import APIView

# 判断用户是否存在
# url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),
from users.models import User


class UsernameCountView(APIView):
    """
       用户名数量
       """

    def get(self, request, username):
        """
        获取指定用户名数量

        """
        count = User.objects.filter(username=username).count()

        data = {
            "usename": username,
            "count": count

        }
        return Response(data)

# 判断手机号是否存在
# url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.Mc55bileCountView.as_view()),


class MobileCountView(APIView):
    """
    手机号数量
    """

    def get(self, request, mobile):
        """
        获取指定手机号数量
        """
        count = User.objects.filter(mobile=mobile).count()

        data = {
            'mobile': mobile,
            'count': count
        }

        return Response(data)