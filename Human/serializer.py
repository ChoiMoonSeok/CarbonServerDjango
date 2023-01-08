from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from Human import models as HuModel
from Company import models as ComModel
from Company import serializer as ComSerial

# Employee 직렬화(객체를 json으로 변환)


class EmployeeSerializer(serializers.ModelSerializer):  # 모델 전체를 직렬화(json 변환)
    BelongCom = ComSerial.DepartmentSerializer()
    BelongCom = BelongCom.data["DepartmentName"]

    class Meta:
        model = HuModel.Employee
        exclude = ["RootCom"]


class UserSerializer(serializers.ModelSerializer):  # 모델 전체를 직렬화(json 변환)
    class Meta:
        model = HuModel.User
        fields = "__all__"


class SignUpSerializer(serializers.ModelSerializer):
    DetailInfo = EmployeeSerializer()

    class Meta:
        model = HuModel.User
        fields = "__all__"


class MyTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data["Email"] = self.user.Email
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data
