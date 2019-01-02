from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated

from users import serializers
from users.models import User
from users.serializers import UserSerializer, UserDetailSerializer


# Create your views here.


# GET /user/
class UserDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserDetailSerializer

    # get_queryset: 获取视图所使用的查询集
    # get_object: 从查询集中查询指定的对象，默认根据主键来查

    def get_object(self):
        """返回登录用户"""
        return self.request.user

    # def get(self, request):
    #     """
    #     self.request: request对象
    #     获取登录用户的个人信息:
    #     1. 获取登录用户
    #     2. 将登录用户序列化并返回
    #     """
    #     # 1. 获取登录用户
    #     user = self.get_object()
    #
    #     # 2. 将登录用户序列化并返回
    #     serializer = self.get_serializer(user)
    #     return Response(serializer.data)


# POST /users/
class UserView(CreateAPIView):
    # 指定视图所使用的序列化器类
    serializer_class = UserSerializer

    # def post(self, request):
    #     """
    #     注册用户信息的保存(创建新用户):
    #     1. 获取参数并进行校验(参数完整性，用户名是否存在，手机号格式，手机号是否存在，是否同意协议，两次密码是否一致，短信验证码是否正确)
    #     2. 创建并保存新用户的信息
    #     3. 返回应答，注册成功
    #     """
    #     # 1. 获取参数并进行校验(参数完整性，用户名是否存在，手机号格式，手机号是否存在，是否同意协议，两次密码是否一致，短信验证码是否正确)
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #
    #     # 2. 创建并保存新用户的信息(create)
    #     serializer.save()
    #
    #     # 3. 返回应答，注册成功
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)


# url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),
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
            'username': username,
            'count': count
        }

        return Response(data)


# url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
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