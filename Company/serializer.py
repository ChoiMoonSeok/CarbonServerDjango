from rest_framework import serializers
from . import models


# Company 직렬화(객체를 json으로 변환)
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        fields = "__all__"


# 조직도 직렬화
class ComStructSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        exclude = ["Classification", "Description", "Location"]


# Department 직렬화(객체를 json으로 변환)
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Department
        fields = "__all__"
