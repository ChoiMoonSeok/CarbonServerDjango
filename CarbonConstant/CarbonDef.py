import CarbonClass

# 탄소 배출 유형과 숫자 맵핑
CarbonCateLen = 14
CarbonCategories = [
    "고정연소",
    "이동연소",
    "탈루배출",
    "폐기물처리시설",
    "비료사용",
    "대학소유동물",
    "산림에의한흡수",
    "전력",
    "열",
    "수도",
    "폐기물",
    "통근_통학",
    "출장",
    "위탁운영차량",
]
CarbonCateMap = {
    "고정연소": [],
    "이동연소": [],
    "탈루배출": [],
    "폐기물처리시설": [],
    "비료사용": [],
    "대학소유동물": [],
    "산림에의한흡수": [],
    "전력": [],
    "열": [],
    "수도": [],
    "폐기물": [],
    "통근_통학": [],
    "출장": [],
    "위탁운영차량": [],
}

# 클래스 기반으로 각각의 계산 함수 및 상수 생성

Electric = CarbonClass.Electric()  # 전력 사용량

Heat = CarbonClass.Heat()

Water = CarbonClass.Water()

# 고정연소 목록
gas_liquid = 10**-9
solid = 10**-6

CrudeOil = CarbonClass.StationCom(42.2, 73300, 10, 0.6, gas_liquid)
Gasoline = CarbonClass.StationCom(30.3, 69300, 10, 0.6, gas_liquid)
KeroseneInside = CarbonClass.StationCom(34.3, 71900, 10, 0.6, gas_liquid)
KeroseneBoil = CarbonClass.StationCom(34.3, 71900, 10, 0.6, gas_liquid)
Diesel = CarbonClass.StationCom(35.3, 74100, 10, 0.3, gas_liquid)
B_A_Oil = CarbonClass.StationCom(36.4, 74100, 10, 0.6, gas_liquid)
B_B_Oil = CarbonClass.StationCom(38, 77400, 10, 0.6, gas_liquid)
B_C_Oil = CarbonClass.StationCom(39.2, 77400, 10, 0.6, gas_liquid)

Propane = CarbonClass.StationCom(46.3, 63100, 5, 0.1, gas_liquid)
Butane = CarbonClass.StationCom(45.6, 63100, 5, 0.1, gas_liquid)
# 나프탄 = ~~~
Solvent = CarbonClass.StationCom(31, 73300, 10, 0.6, gas_liquid)
AeroGasoline = CarbonClass.StationCom(34.1, 70000, 10, 0.6, gas_liquid)
JetGasoline = CarbonClass.StationCom(34.1, 70000, 10, 0.6, gas_liquid)
JetKerosene = CarbonClass.StationCom(34.1, 71500, 10, 0.6, gas_liquid)

Asphalt = CarbonClass.StationCom(39.2, 80700, 10, 0.3, solid)
Lubricant = CarbonClass.StationCom(37, 73300, 10, 0.6, gas_liquid)

PetCoke = CarbonClass.StationCom(31.6, 97500, 10, 0.6, solid)
# 부생연료 1, 2
NaturalLPG = CarbonClass.StationCom(49.3, 56100, 5, 0.1, gas_liquid)
# LNG
# 도시가스
LocalHardCoal = CarbonClass.StationCom(18.6, 98300, 10, 1.5, solid)
ForeignHardCoalFuel = CarbonClass.StationCom(20.6, 98300, 10, 1.5, solid)
ForeignHardCoalRaw = CarbonClass.StationCom(24.4, 98300, 10, 1.5, solid)
SoftCoalFuel = CarbonClass.StationCom(24.7, 94600, 10, 1.5, solid)
SoftCoalRaw = CarbonClass.StationCom(28.2, 94600, 10, 1.5, solid)
BituminousCoal = CarbonClass.StationCom(21.4, 96100, 10, 1.5, solid)
Cokes = CarbonClass.StationCom(28.9, 107000, 10, 1.5, solid)


# 이동연소 목록
GasolineMove = CarbonClass.MovingCom(30.3, 69300, 25, 8)
DieselMove = CarbonClass.MovingCom(35.3, 74100, 3.9, 3.9)
LPGNaturalMove = CarbonClass.MovingCom(49.3, 63100, 62, 0.2)
LPGCityMove = CarbonClass.MovingCom(39.4, 63100, 62, 0.2)
KeroseneMove = CarbonClass.MovingCom(34.3, 71900, 0, 0)
LubricantMove = CarbonClass.MovingCom(37, 73300, 0.0)
# CNG
LNG = CarbonClass.MovingCom(39.4, 56100, 92, 3)


# 탈루배출
AirCon = CarbonClass.AirCon()
Refri = CarbonClass.Refri()
