import re

from django.contrib.auth.backends import ModelBackend

from users.models import User


def jwt_response_payload_handler(token, user=None, request=None ):
    """自定义jwt认证成功返回数据"""
    return {
        "token": token,
        "user_id": user.id,
        "username": user.username
    }


def get_user_by_account(account):
    """account: 用户名或手机"""
    try:
        if re.match(r'^1[3-9]\d{9}$', account):
            # 根据手机号查询用户
            user = User.objects.get(mobile = account)
        else:
            # 根据用户名查询用户
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        # 用户不存在
        return None
    else:
        return user


# 自定Django认证后端类
class UsernameMobileAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        """username: 用户名或手机号"""

        # 1. 根据`用户名`或`手机号`查询用户
        user = get_user_by_account(username)

        # 2. 校验用户密码，如果密码登录，返回user
        if user and user.check_password(password):
            # 账户密码正确
            return user
