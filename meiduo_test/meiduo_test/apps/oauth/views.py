from django.shortcuts import render

# Create your views here.
# GET /oauth/qq/authorization/?next=<登陆之后跳转页面的地址>
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from oauth.models import OAuthQQUser
from oauth.utils import OAuthQQ


#  GET /oauth/qq/user/?code=<code>
class QQAuthUserView(APIView):
    def get(self, request):
        """
        获取qq登陆用户的openid并处理
        1.获取code并校验 （code必传）
        2.获取qq登陆用户的openid
            2.1 根据code 请求qq服务器获取access_token
            2.2 根据access_token请求qq服务器获取openid
        3.根据openid判断是否绑定过本网站的用户
            3.1 如果已绑定，直接生成jwt token并返回
            3.2 如果未绑定，将openid加密并返回

        """

        # 1.获取code并校验 （code必传）
        code = request.query_params.get("code")  # None
        if code is None:
            return Response({"message": "缺少code参数"}, status=status.HTTP_400_BAD_REQUEST)

        # 2.获取qq登陆用户的openid
        oauth = OAuthQQ()

        # 2.1根据code请求qq服务器获取access_token
        access_token = oauth.get_access_token(code)
        # 2.2根据access_token请求qq服务器获取openid
        openid = oauth.get_openid(access_token)

        # 3.根据openid判断是否绑定过本网站的用户
        try:
            qq_user = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            # 3.2如果未绑定，将openid加密并返回
            secret_openid = oauth.generate_save_user_token(openid)
            return Response({"access_token": secret_openid})

        else:
            # 3.1 如果已绑定，直接生成jwt token并返回
            user = qq_user.user

            # 由服务器生成一个jwt token字符串，保存用户的身份信息
            from rest_framework_jwt.settings import api_settings

            # 生成payload载荷
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            # 生成jwt token
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            payload = jwt_payload_handler(user)
            # 生成jwt token
            token = jwt_encode_handler(payload)

            response_data = {
                "user_id": user.id,
                "user_name": user.name,
                "token": token
            }


class QQAuthURLView(APIView):
    def get(self, request):
        """
         获取QQ登陆网址：
         1. 获取next (可以不传)
         2. 组织qq登陆网址和参数
         3. 返回QQ登陆网址
         """
        # 1. 获取next (可以不传)
        request.query_params.get("next", "/")  # 如果没有传 默认跳转到“/”

        # 2. 组织qq登陆网址和参数
        oauth = OAuthQQ(state=next)
        login_url = oauth.get_login_url()

        # 3. 返回QQ登陆网址
        return Response({"login_url": login_url})
