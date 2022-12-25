from rest_framework import serializers
from . import models

# Carbon 직렬화(객체를 json으로 변환)


class CarbonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Carbon
        exclude = ["RootCom", "BelongCom", "CarbonInfo"]


class CarbonInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CarbonInfo
        fields = "__all__"
