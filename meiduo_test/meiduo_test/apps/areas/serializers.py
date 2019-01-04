import serializers as serializers
from rest_framework import serializers

from areas.models import Area


class AreaSerializer(serializers.ModelSerializer):
    """地区序列化器类"""

    class Meta:
        model = Area
        fields = ("id", "name")


class SubAreaSerializer(serializers.ModelSerializer):
    """地区序列化器类"""
    subs = AreaSerializer(label="下级地区", many=True)  # 下级地区嵌套序列化

    class Meta:
        model = Area
        fields = ("id", "name", "subs")