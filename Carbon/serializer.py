from rest_framework import serializers

from . import models
from Company import models as ComModel
from Company import serializer as ComSerial


class CarbonInfoSerializer(serializers.ModelSerializer):  # carbonInfo 모델을 json으로 변환
    class Meta:
        model = models.CarbonInfo
        fields = "__all__"


class CarbonSerializer(serializers.ModelSerializer):  # carbon 모델을 json으로 변환
    class Meta:
        model = models.Carbon
        exclude = ["RootCom", "BelongCom", "CarbonInfo"]


class CarbonTotalSerializer(serializers.ModelSerializer):
    CarbonInfo = CarbonInfoSerializer()
    RootCom = ComSerial.CompanySerializer()
    BelongCom = ComSerial.CompanySerializer()

    class Meta:
        model = models.Carbon
        fields = "__all__"
