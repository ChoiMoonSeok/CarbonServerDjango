from Company import models as ComModel
from Human import models as HuModel
from Carbon import models as CarMode
from Company import serializer

CarbonCategory = [
    "고정연소",
    "이동연소",
    "탈루배출",
    "폐기물 처리 시설",
    "비료사용",
    "대학소유동물",
    "산림에 의한 흡수",
    "전력",
    "스팀(열)",
    "수도",
    "폐기물",
    "민간업체",
    "통근/통학",
    "출장",
    "위탁운영 차량",
]


# 조직 구조를 반환하는 함수
def getStruct(RootCom, HeadCom, result):
    data = ComModel.Department.objects.filter(RootCom=RootCom, BelongCom=HeadCom)
    if type(data) == None:
        return None
    else:
        for Depart in data:
            temp = serializer.CompanySerializer(Depart.SelfCom)
            temp = temp.data
            temp["Children"] = []
            result["Children"].append(temp)
            getStruct(RootCom, Depart.SelfCom, result["Children"][-1])


def getChildDepart(RootCom, HeadCom, Children):
    data = ComModel.Department.objects.filter(RootCom=RootCom, BelongCom=HeadCom)
    if type(data) == None:
        return None
    else:
        for Depart in data:
            Children.append(Depart)
            getChildDepart(RootCom, Depart.SelfCom, Children)
