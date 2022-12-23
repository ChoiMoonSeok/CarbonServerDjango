from rest_framework import serializers
from .models import *

# Employee 직렬화(객체를 json으로 변환)


class EmployeeSerializer(serializers.ModelSerializer):  # 모델 전체를 직렬화(json 변환)
    class Meta:
        model = Employee
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):  # 모델 전체를 직렬화(json 변환)
    class Meta:
        model = User
        fields = "__all__"


# Company 직렬화(객체를 json으로 변환)


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


# Department 직렬화(객체를 json으로 변환)


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


# Carbon 직렬화(객체를 json으로 변환)


class CarbonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carbon
        fields = "__all__"


class CarbonInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarbonInfo
        fields = "__all__"
