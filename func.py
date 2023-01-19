from rest_framework_simplejwt.tokens import AccessToken

from Company import models as ComModel
from Human import models as HuModel
from Carbon import models as CarMode
from Company import serializer


# 조직 구조를 반환하는 함수
def getStruct(RootCom, HeadCom, result):
    data = ComModel.Department.objects.filter(RootCom=RootCom, BelongCom=HeadCom)
    if type(data) == None:
        return None
    else:
        for Depart in data:
            temp = serializer.ComStructSerializer(Depart.SelfCom)
            temp = temp.data

            if temp["Chief"] != None:
                temp["Chief"] = HuModel.Employee.objects.get(id=temp["Chief"]).Name
            temp["Children"] = []
            result["Children"].append(temp)
            getStruct(RootCom, Depart.SelfCom, result["Children"][-1])


def getChildDepart(RootCom, HeadCom, Children):
    data = ComModel.Department.objects.filter(RootCom=RootCom, BelongCom=HeadCom)
    if type(data) == None:
        return None
    else:
        for Depart in data:
            if type(Depart) == None:
                continue
            Children.append(Depart)
            getChildDepart(RootCom, Depart.SelfCom, Children)


def getChildCom(RootCom, HeadCom, Children):
    data = ComModel.Department.objects.filter(RootCom=RootCom, BelongCom=HeadCom)
    if type(data) == None:
        return None
    else:
        for Depart in data:
            Children.append(Depart.SelfCom)
            getChildDepart(RootCom, Depart.SelfCom, Children)


# jwt 헤더로부터 User의 RootCom을 찾아 반환하는 함수
def getRootViaJWT(token_str):
    access_token = AccessToken(token_str)
    Email = access_token["user_id"]
    RootCom = HuModel.User.objects.get(Email=Email).DetailInfo.RootCom
    return RootCom


# jwt 헤더로부터 User의 BelongCom을 찾아 반환하는 함수
def getBelongViaJWT(token_str):
    access_token = AccessToken(token_str)
    Email = access_token["user_id"]
    BelongCom = HuModel.User.objects.get(Email=Email).DetailInfo.BelongCom
    return BelongCom


# 탄소 데이터를 변경하는 함수
def ChangeCarbon(Kind, Info, Carbon):
    if Kind == "StartDate":
        Carbon.CarbonInfo.StartDate = Info
    elif Kind == "EndDate":
        Carbon.CarbonInfo.EndDate = Info
    elif Kind == "Location":
        Carbon.CarbonInfo.Location = Info
    elif Kind == "Scope":
        Carbon.CarbonInfo.Scope = Info
    elif Kind == "Chief":
        Carbon.CarbonInfo.StartDate = HuModel.Employee.objects.get(
            RootCom=Root, Name=Info
        )
    elif Kind == "StartDate":
        Carbon.CarbonInfo.StartDate = Info
    elif Kind == "StartDate":
        Carbon.CarbonInfo.StartDate = Info


def GetUserRoot(request):
    token_str = request.META.get("HTTP_AUTHORIZATION").split()[1]
    UserRoot = getRootViaJWT(token_str)
    return UserRoot


# 유저의 권환을 확인하는 함수
def CheckUserAuthorization():
    pass
