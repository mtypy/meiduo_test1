from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated

from users import serializers
from users.models import User
from users.serializers import UserSerializer, UserDetailSerializer, EmailSerializer


# Create your views here.

# PUT /emails/verification/?token=<加密用户的信息>
class EmailVerifyView(APIView):
    def put(self, request):
        """
        用户邮箱验证：
        1.获取token(加密用户的信息)并进行校验（token必传，token是否有效）
        2. 设置用户的邮箱验证标记True
        3. 返回应答，邮箱验证成功
        """
        # 1.获取token(加密用户的信息)并进行校验（token必传，token是否有效）
        token = request.query_param.get("token")

        if token is None:
            return Response({"message":"缺少token参数"}, status=status.HTTP_400_BAD_REQUEST)

        # token是否有效
        user = User.check_verify_email_token(token)

        if user is None:
            return Response({'message': '无效的token数据'}, status=status.HTTP_400_BAD_REQUEST)

        # 2. 设置用户的邮箱验证标记True
        user.email_active = True
        user.save()

        # 3. 返回应答，邮箱验证成功
        return Response({"message": "ok"})


# 保存用户邮箱 PUT
class EmailView(UpdateAPIView):
    """保存用户邮箱"""
    permission_classes = [IsAuthenticated]
    serializer_class = EmailSerializer

    def get_object(self):
        return self.request.user

    # def put(self, request):
    #     """
    #     保存登录用户的邮箱:
    #     1. 获取参数并进行校验(email必传，邮箱格式)
    #     2. 设置登录用户的邮箱并给邮箱发送验证邮件
    #     3. 返回应答，邮箱设置成功
    #     """
    #     # 获取登录用户
    #     user = self.get_object()
    #
    #     # 1. 获取参数并进行校验(email必传，邮箱格式)
    #     serializer = self.get_serializer(user, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #
    #     # 2. 设置登录用户的邮箱并给邮箱发送验证邮件(update)
    #     serializer.save()
    #
    #     # 3. 返回应答，邮箱设置成功
    #     return Response(serializer.data)


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


