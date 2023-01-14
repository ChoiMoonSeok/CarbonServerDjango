import json

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

from . import models as CarModel
from Human import models as HuModel
from Company import models as ComModel
from . import serializer
import func


class CarbonEmissionQuery(APIView):

    permission_classes = (IsAuthenticated,)  # 로그인 검증

    @swagger_auto_schema(
        operation_summary="요청한 회사의 모든 탄소 배출원을 반환하는 Api",
        responses={404: "입력한 회사가 존재하지 않음", 201: "API가 정상적으로 실행 됨"},
    )
    def get(self, request, Depart, format=None):
        """{Depart}를 통해 입력 받은 회사의 이름을 바탕으로, 해당 회사의 모든 탄소 배출원을 반환합니다.\n
        해당 회사의 탄소 배출 뿐만 아니라 해당 회사의 자회사, 부서의 탄소 배출원도 모두 포함합니다.\n
        하단의 Description에 탄소 배출원을 알고 싶은 회사의 사명을 입력하면 됩니다.\n
        탄소 배출원 예) 홍길동 교수님 출장, 탄소 배출량 20"""

        token_str = request.META.get("HTTP_AUTHORIZATION").split()[1]
        UserRoot = func.getRootViaJWT(token_str)

        try:  # 요청받은 회사가 루트가 아닌 경우
            Root_id = ComModel.Department.objects.get(
                DepartmentName=Depart  # 로그인이 구현된 이후에는 사용자의 root와 비교
            )
        except ComModel.Department.DoesNotExist:  # 요청받은 회사가 루트인 경우
            try:
                Root_id = ComModel.Company.objects.get(ComName=Depart)
            except ComModel.Company.DoesNotExist:  # 요청받은 회사가 존재하지 않는 경우
                return Response(
                    "This Company/Department doesn't exist.",
                    status=status.HTTP_404_NOT_FOUND,
                )

        # 요청받은 회사가 루트인 경우
        if type(Root_id) == ComModel.Company:

            data = CarModel.Carbon.objects.filter(RootCom=Root_id)
            serial = serializer.CarbonSerializer(data, many=True)

            return Response(serial.data, status=status.HTTP_201_CREATED)

        else:  # 요청 받은 회사가 루트, 모회사가 아닌 경우
            Coms = [Root_id]
            func.getChildDepart(Root_id.RootCom, Root_id.SelfCom, Coms)

            CarbonList = []

            for Com in Coms:

                temp = CarModel.Carbon.objects.filter(BelongDepart=Com)
                serial = serializer.CarbonSerializer(temp, many=True)
                CarbonList += serial.data

            return Response(CarbonList, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="탄소 배출 원인 Api", request_body=serializer.CarbonSerializer
    )
    def post(self, request, Depart, format=None):
        """
        탄소 사용량 데이터 입력하는 Api
        """

        token_str = request.META.get("HTTP_AUTHORIZATION").split()[1]
        UserRoot = func.getRootViaJWT(token_str)

        UserBelong = func.getBelongViaJWT(token_str)
