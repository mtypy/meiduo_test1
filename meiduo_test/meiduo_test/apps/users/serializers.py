import re

from django_redis import get_redis_connection
from rest_framework import serializers

from goods.models import SKU
from users import constants
from users.models import User, Address


# User.objects.create()
class UserSerializer(serializers.ModelSerializer):
    """用户序列化器类"""
    password2 = serializers.CharField(label='重复密码', write_only=True)
    sms_code = serializers.CharField(label='短信验证码', write_only=True)
    allow = serializers.CharField(label='是否同意协议', write_only=True)
    token = serializers.CharField(label='JWT token', read_only=True)

    class Meta:
        model = User
        # read_only = True
        fields = ('id', 'username', 'password', 'mobile', 'password2', 'sms_code', 'allow', 'token')

        extra_kwargs = {
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }

    # 参数完整性，用户名是否存在，手机号格式，手机号是否存在，是否同意协议，两次密码是否一致，短信验证码是否正确
    def validate_mobile(self, value):
        # 手机号格式
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式不正确')

        # 手机号是否存在
        res = User.objects.filter(mobile=value).count()

        if res > 0:
            raise serializers.ValidationError('手机号已存在')

        return value

    def validate_allow(self, value):
        # 是否同意协议
        if value != 'true':
            raise serializers.ValidationError('请同意协议')

        return value

    def validate(self, attrs):
        """
        attrs: 字典，传入data数据
        """
        # 两次密码是否一致
        password = attrs['password']
        password2 = attrs['password2']

        if password != password2:
            raise serializers.ValidationError('两次密码不一致')

        # 短信验证码是否正确
        mobile = attrs['mobile']

        # 从redis中获取真实的短信验证码
        redis_conn = get_redis_connection('verify_codes')

        real_sms_code = redis_conn.get('sms_%s' % mobile) # bytes

        if not real_sms_code:
            raise serializers.ValidationError('短信验证码已失效')

        # 对比短信验证码
        sms_code = attrs['sms_code'] # str

        if real_sms_code.decode() != sms_code:
            raise serializers.ValidationError('短信验证码错误')

        return attrs

    def create(self, validated_data):
        """创建并保存新用户的信息"""
        # validated_data: 反序列化校验之后的数据
        # 清除无用的数据
        del validated_data['password2']
        del validated_data['sms_code']
        del validated_data['allow']

        # 创建新用户
        user = User.objects.create_user(**validated_data)

        # 由服务器生成一个jwt token字符串，保存用户的身份信息
        from rest_framework_jwt.settings import api_settings

        # 生成payload载荷
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        # 生成jwt token
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        # 生成jwt token
        token = jwt_encode_handler(payload)

        # 给user对象增加属性token，保存生成jwt token数据
        user.token = token

        return user


class UserDetailSerializer(serializers.ModelSerializer):
    """用户的序列化器类"""
    class Meta:
        model = User
        fields = ('id', 'username', 'mobile', 'email', 'email_active')


class EmailSerializer(serializers.ModelSerializer):
    """邮箱序列化器类"""
    class Meta:
        model = User
        fields = ('id', 'email')

        extra_kwargs = {
            'email': {
                'required': True
            }
        }

    def update(self, instance, validated_data):
        # 设置登录用户的邮箱
        email = validated_data['email']
        instance.email = email
        instance.save()

        # TODO: 并给邮箱发送验证邮件
        # 验证链接地址: http://www.meiduo.site:8080/success_verify_email.html?token=<加密用户信息>
        verify_url = instance.generate_verify_email_url()

        # 发出发送邮件的任务消息
        # send_mail()
        from celery_tasks.email.tasks import send_verify_email
        send_verify_email.delay(email, verify_url)

        return instance


class AddressSerializer(serializers.ModelSerializer):
    """地址序列化器类"""
    province_id = serializers.IntegerField(label='省id')
    city_id = serializers.IntegerField(label='市id')
    district_id = serializers.IntegerField(label='区县id')
    province = serializers.StringRelatedField(label='省名称', read_only=True)
    city = serializers.StringRelatedField(label='市名称', read_only=True)
    district = serializers.StringRelatedField(label='区县名称', read_only=True)

    class Meta:
        model = Address
        exclude = ('user', 'is_deleted', 'create_time', 'update_time')

    def valdate_mobile(self, value):
        # 手机号格式
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式不正确')

        return value

    def create(self, validated_data):
        # 创建并保存新增地址数据
        user = self.context['request'].user
        validated_data['user'] = user

        # 调用`ModelSerializer`中的create方法完整地址创建
        return super().create(validated_data)


class AddressTitleSerializer(serializers.ModelSerializer):
    """
    地址标题
    """
    class Meta:
        model = Address
        fields = ('title',)


class HistorySerializer(serializers.Serializer):
    """浏览记录序列化器类"""
    sku_id = serializers.IntegerField(label='商品id', min_value=1)

    def validate_sku_id(self, value):
        # sku_id对应的商品是否存在
        try:
            SKU.objects.get(id=value)
        except SKU.DoesNotExist:
            raise serializers.ValidationError('商品不存在')

        return value

    def create(self, validated_data):
        """在redis中保存登录用户的浏览记录"""
        # 获取redis链接
        redis_conn = get_redis_connection('histories')

        # 获取登录用户
        user = self.context['request'].user

        history_key = 'history_%s' % user.id

        sku_id = validated_data['sku_id']
        # 1. 去重：如果用户已经浏览过该商品，将商品的id从redis列表中移除
        redis_conn.lrem(history_key, 0, sku_id)

        # 2. 保持有序：将用户最新浏览的商品id添加到列表的最左侧
        redis_conn.lpush(history_key, sku_id)

        # 3. 截取：只保留用户最新浏览的几个商品的id
        redis_conn.ltrim(history_key, 0, constants.USER_BROWSING_HISTORY_COUNTS_LIMIT - 1)

        return validated_data








