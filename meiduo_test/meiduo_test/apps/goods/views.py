from django.shortcuts import render
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import OrderingFilter
from drf_haystack.viewsets import HaystackViewSet

from goods.models import SKU
from goods.serializers import SKUSerializer, SKUIndexSerializer


# Create your views here.


# /skus/search/?text=<key>
class SKUSearchViewSet(HaystackViewSet):
    # 指定索引类对应模型类
    index_models = [SKU]

    # 全文检索框架搜索出结果之后，会使用指定的序列化器类对搜索结果进行序列化
    # 每个搜索结果对象中都包含两个属性：
    # text: 索引字段内容
    # object: 搜索出模型对象(此处应该商品对象)
    serializer_class = SKUIndexSerializer


# GET /categories/(?P<category_id>\d+)/skus/?ordering=<排序字段>
class SKUListView(ListAPIView):
    serializer_class = SKUSerializer
    # queryset = SKU.objects.filter(category_id=category_id)

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return SKU.objects.filter(category_id=category_id)

    # def get(self, request, category_id):
    #     """
    #     self.kwargs: 字典，保存从url地址中提取的所有命名参数
    #     获取第三级分类SKU商品的数据:
    #     1. 根据`category_id`获取第三级分类SKU商品的数据
    #     2. 将SKU商品的数据序列化并返回
    #     """
    #     # 1. 根据`category_id`获取第三级分类SKU商品的数据
    #     skus = self.get_queryset()
    #
    #     # 2. 将SKU商品的数据序列化并返回
    #     serializer = self.get_serializer(skus, many=True)
    #     return Response(serializer.data)

    # 排序设置
    filter_backends = [OrderingFilter]
    # 指定排序字段
    ordering_fields = ('create_time', 'price', 'sales')
