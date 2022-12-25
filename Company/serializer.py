from rest_framework import serializers
from . import models


# Company 직렬화(객체를 json으로 변환)


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        fields = "__all__"


# Department 직렬화(객체를 json으로 변환)


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Department
        fields = "__all__"
