import random

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

        send_flag = redis_conn.get('send_flag_%s' % mobile) # None

        if send_flag:
            return Response({'message': '发送短信过于频繁'}, status=status.HTTP_400_BAD_REQUEST)

        # 1. 随机生成6位数字作为短信验证码
        sms_code = '%06d' % random.randint(0, 999999) # 000010
        logger.info('短信验证码内容为: %s' % sms_code)

        # 2. 在redis中保存短信验证码的内容，以`mobile`为key，以`验证码内容`为value
        # redis_conn.set('<key>', '<value>', '<expries>')
        # redis_conn.setex('<key>', '<expries>', '<value>')

        # 创建redis管道对象
        pl = redis_conn.pipeline()

        # 向管道中添加命令
        pl.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        # 设置给`mobile`发送短信标记
        pl.setex('send_flag_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)

        # 一次性执行管道中所有命令
        pl.execute()

        # 3. 使用云通讯发送短信验证码
        expires = constants.SMS_CODE_REDIS_EXPIRES // 60

        # # 发出发送短信的任务消息
        from celery_tasks.sms.tasks import send_sms_code
        send_sms_code.delay(mobile, sms_code, expires)

        # 4. 返回应答，发送成功
        return Response({'message': 'OK'})
