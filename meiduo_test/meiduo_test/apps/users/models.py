from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSSerializer
from itsdangerous import BadData
# Create your models here.


# 用户模型类
from users import constants


class User(AbstractUser):
    """用户模型类"""
    mobile = models.CharField(max_length=11, verbose_name='手机号')
    email_active = models.BooleanField(default=False, verbose_name="邮箱验证状态")

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def generate_verify_email_url(self):
        """生成用户的邮箱验证链接地址"""
        # 组织数据
        data = {
            "id": self.id,
            "email": self.email
        }

        # 进行加密
        serializer = TJWSSerializer(secret_key=settings.SECRET_KEY, expires_in=constants.VERIFY_EMAIL_TOKEN_EXPIRES)
        token = serializer.dumps(data).decode()

        # 拼接链接地址
        verify_url = 'http://www.meiduo.site:8080/success_verify_email.html?token=' + token
        return verify_url


    @staticmethod
    def check_verify_email_token(token):
        """
        token: 加密用户的信息
        """
        # 进行解密
        serializer = TJWSSerializer(secret_key=settings.SECRET_KEY)

        try:
            data = serializer.load(token)
        except BadData:
            # 解密失败
            return None
        else:
            # 解密成功
            id = data.get("id")
            email = data.get("email")

            # 查询用户
            try:
                user = User.objects.get(id=id, email=email)

            except User.DoesNotExist:
                return None
            else:
                return user
