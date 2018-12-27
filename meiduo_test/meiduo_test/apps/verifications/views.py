import random

from django.shortcuts import render
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


from verifications import constants

# Create your views here.

# 获取redis链接
# from redis import StrictRedis
# redis_conn = StrictRedis(host=<ip>, port=<port>, db=<db>)

# 获取日志器
import logging
logger = logging.getLogger('django')


# GET /sms_codes/(?P<mobile>1[3-9]\d{9})/
class SMSCodeView(APIView):
    def get(self, request, mobile):
        """
        短信验证码的获取:
        1. 随机生成6位数字作为短信验证码
        2. 在redis中保存短信验证码的内容，以`mobile`为key，以`验证码内容`为value
        3. 使用云通讯发送短信验证码
        4. 返回应答，发送成功
        """

        # 获取给`mobile`发送短信标记
        redis_conn = get_redis_connection('verify_codes')  # StrictRedis对象

        send_flag = redis_conn.get('send_flag_%s' % mobile)  # None

        if send_flag:
            return Response({'message': '发送短信过于频繁'}, status=status.HTTP_400_BAD_REQUEST)

        # 1. 随机生成6位数字作为短信验证码
        sms_code = '%06d' % random.randint(0, 999999) # 000010

        # 2. 在redis中保存短信验证码的内容，以`mobile`为key，以`验证码内容`为value
        redis_conn = get_redis_connection('verify_codes')  # StrictRedis对象



        # redis_conn.set('<key>', '<value>', '<expries>')
        # redis_conn.setex('<key>', '<expries>', '<value>')

        redis_conn.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)

        redis_conn.setex('send_flag_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL,1)
        # 3. 使用云通讯发送短信验证码
        expires = constants.SMS_CODE_REDIS_EXPIRES // 60
        # try:
        #     res = CCP().send_template_sms(mobile, [sms_code, expires], constants.SEND_SMS_TEMP_ID)
        # except Exception as e:
        #     logger.error('发送短信异常: %s' % e)
        #     return Response({'message': '短信发送异常'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        #
        # if res != 0:
        #     # 发送短信失败
        #     return Response({'message': '短信发送失败'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # 4. 返回应答，发送成功
        return Response({'message': 'OK'})
