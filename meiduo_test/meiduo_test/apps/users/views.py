from django.shortcuts import render
from rest_framework import status, request
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from users import serializers, constants
from users.models import User, Address
from users.serializers import UserSerializer, UserDetailSerializer, EmailSerializer, AddressSerializer, \
    AddressTitleSerializer


# Create your views here.
# 新增地址的数据

class AddressViewSet(CreateModelMixin,GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer

    def get_queryset(self):
        """返回用户的地址查询集"""
        return self.request.user.addresses.filter(is_deleted=False)

    # POST /addresses
    def create(self, request):
        """
        request.user: 获取登录用户
        保存新增地址的数据：
        1. 接收参数并进行校验(参数完整性，手机号格式)
        2. 创建并保存新增地址数据
        3. 返回应答，地址创建成功
        """
        # 用户地址数据是否超过上限
        count = request.user.addresses.filter(is_deleted=False).count()

        if count > constants.USER_ADDRESS_COUNTS_LIMIT:
            return Response({'message': '保存地址数据已达到上限'}, status=status.HTTP_400_BAD_REQUEST)
        # 调用`CreateModelMixin`扩展类中create方法
        return super() .create(request)
# GET /addresses/

    def list(self, request):
        """
        1. 获取登录用户的所有地址数据
        2. 将用户的地址数据序列并返回
        """
        user = request.user
        # 1. 获取登录用户的所有地址数据
        addresses = self.get_queryset()

        # 2. 将用户的地址数据序列并返回
        serializer = self.get_serializer(addresses, many=True)

        return Response({
            'user_id': user.id, # 用户id
            'default_address_id': user.default_address_id, # 默认地址id
            'limit': constants.USER_ADDRESS_COUNTS_LIMIT, # 地址数量上限
            'addresses': serializer.data, # 地址数据
        })

    # PUT /addresses/(?P<pk>\d+)/
    # def update(self, request, pk):
    #     """
    #     1. 根据pk获取对应的地址数据
    #     2. 获取参数并进行校验
    #     3. 保存修改地址的数据
    #     4. 返回应答，修改成功
    #     """
    #     # 1. 根据pk获取对应的地址数据
    #     address = self.get_object()
    #     # 2. 获取参数并进行校验
    #     serializer = self.get_serializer(address, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #
    #     # 3. 保存修改地址的数据(update)
    #     serializer.save()
    #
    #     # 4. 返回应答，修改成功
    #     return Response(serializer.data)

    # DELETE /addresses/(?P<pk>\d+)/
    def destroy(self, request, pk):
        """
        1. 根据pk获取对应的地址数据
        2. 将地址删除
        3. 返回应答
        """
        # 1. 根据pk获取对应的地址数据
        address = self.get_object()

        # 2. 将地址删除
        address.is_deleted = True
        address.save()

        # 3. 返回应答
        return Response(status=status.HTTP_204_NO_CONTENT)

    # 设为默认地址
    # PUT /addresses / (?P<pk>\d+)/status/
    @action(methods=["put"], detail=True)
    def status(self, request, pk):
        """
              1. 根据pk获取对应的地址数据
              2. 将此地址设置为用户的默认地址
              3. 返回应答
              """

    # 1. 根据pk获取对应的地址数据
        address = self.get_object()

    # 2. 将此地址设置为用户的默认地址
        request.user.default_address_id = address.id

    # 3.返回应答
        return Response({"message": "ok"}, status=status.HTTP_200_OK)

    # 设置地址标题
    # PUT /address/(?P<pk>\d+)/title/
    @action(methods=['put'], detail=True)
    def title(self, request, pk):
        """
        1. 根据pk获取对应的地址数据
        2. 获取title并进行校验
        3. 设置地址标题
        4. 返回应答
        """
        # 1. 根据pk获取对应的地址数据
        address = self.get_object()

        # 2. 获取title并进行校验
        serializer = AddressTitleSerializer(address, data=request.data)
        serializer.is_valid(raise_exception=True)

        # 3. 设置地址标题(update)
        serializer.save()

        # 4. 返回应答
        return Response(serializer.data)

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




