from django.shortcuts import render

# Create your views here.
# GET /oauth/qq/authorization/?next=<登陆之后跳转页面的地址>
from rest_framework.response import Response
from rest_framework.views import APIView

from oauth.utils import OAuthQQ


class QQAuthUserView(APIView):
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

