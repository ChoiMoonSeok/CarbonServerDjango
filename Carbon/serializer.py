from rest_framework import serializers
from .models import *

# User, Employee 직렬화(객체를 json으로 변환)

class User_EmployeeSerializer(serializers.ModelSerializer): # 모델 전체를 직렬화(json 변환)
    class Meta:
        model = User_Employee
        fields = ['id', 'UID', 'PassWd', 'Name', 'PhoneNum', 'Email', 'Company', 'JobPos', 'IdentityNum']

# Company 직렬화(객체를 json으로 변환)

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'ComName', 'Scope1', 'Scope2', 'Scope3', 'chief']

# Department 직렬화(객체를 json으로 변환)

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'DepartmentName', 'Scope1', 'Scope2', 'Scope3', 'chief', 'depth', 'upper', 'Mother']

# Carbon 직렬화(객체를 json으로 변환)

class CarbonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carbon
        fileds = ['id', 'Content', 'Data', 'unit', 'CarbonEmission', 'StartDate', 'EndData', 'location', 'Scope', 'chief', 'upper', 'Mother']