
# Create your views here.
# from drf_haystack import serializers
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User

from users.serializers import UserSerializer

# 判断用户是否存在
# url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),


# 用户注册
# 请求方式 POST /users/
# 请求参数 表单 或 json

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
