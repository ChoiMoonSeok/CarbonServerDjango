from rest_framework_simplejwt.tokens import AccessToken

from Company import models as ComModel
from Human import models as HuModel
from Carbon import models as CarModel
from Company import serializer
from CarbonConstant import CarbonDef


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


def GetUserRoot(request):
    token_str = request.META.get("HTTP_AUTHORIZATION").split()[1]
    UserRoot = getRootViaJWT(token_str)
    return UserRoot


def AddZero(date):
    date = date.split("-")
    for i in range(len(date)):
        if len(date[i]) < 2:
            date[i] = "0{}".format(date[i])

    num = 0
    temp = str()
    for i in date:
        temp += i
        if num != 2:
            temp += "-"
            num += 1
    date = temp
    del temp

    return date


# 소속된 회사를 가져오는 함수
def GetBelong():
    pass


# db에 Carbon 생성
def CreateCarbon(CarbonData, CarTrans, usage, Root, Belong, CarInfo):
    CarModel.Carbon.objects.create(
        CarbonActivity=CarbonData["CarbonData"]["CarbonActivity"],
        CarbonData=usage,
        CarbonUnit=CarbonData["CarbonData"]["CarbonUnit"],
        CarbonTrans=CarTrans,
        RootCom=Root,
        BelongDepart=Belong,
        CarbonInfo=CarInfo,
    )


# db에 CarbonInfo 생성
def CreateCarbonInfo(CarbonData, Root, Type):
    ans = CarModel.CarbonInfo.objects.create(
        StartDate=CarbonData["CarbonData"]["StartDate"],
        EndDate=CarbonData["CarbonData"]["EndDate"],
        Location=CarbonData["CarbonData"]["Location"],
        Scope=CarbonData["CarbonData"]["Scope"],
        Chief=HuModel.Employee.objects.get(
            RootCom=Root, Name=CarbonData["CarbonData"]["Chief"]
        ),
        Category=CarbonDef.CarbonCategories.index(Type),
        Division=str(CarbonData),
    )
    return ans


# 유저의 권환을 확인하는 함수
def CheckUserAuthorization():
    pass
