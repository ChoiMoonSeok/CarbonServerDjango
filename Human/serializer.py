from rest_framework import serializers
from . import models

# Employee 직렬화(객체를 json으로 변환)


class EmployeeSerializer(serializers.ModelSerializer):  # 모델 전체를 직렬화(json 변환)
    class Meta:
        model = models.Employee
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):  # 모델 전체를 직렬화(json 변환)
    class Meta:
        model = models.User
        fields = "__all__"
