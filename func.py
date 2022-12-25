from Company import models as ComModel
from Human import models as HuModel
from Carbon import models as CarMode

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
def put_struct(result, Company):
    if Company["upper"] == None:
        result["Children"].append(Company)
        return 0
    elif result["depth"] == Company["depth"] - 1:
        if result["id"] == Company["upper"]:
            result["Children"].append(Company)
        else:
            return 0
    else:
        if len(result["Children"]) != 0:
            for i in range(len(result["Children"])):
                temp = result["Children"][i]
                put_struct(temp, Company)
        else:
            if result["id"] == Company["upper"]:
                result["Children"].append(Company)
            else:
                return 0


def getChildCom(RootCom, HeadCom, Children):
    data = ComModel.Department.objects.filter(RootCom=RootCom, BelongCom=HeadCom)
    if type(data) == None:
        return None
    else:
        for Depart in data:
            Children.append(Depart.SelfCom)
            getChildCom(RootCom, Depart.SelfCom, Children)
