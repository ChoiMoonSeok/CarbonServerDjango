from . import CarbonClass

# 탄소 배출 유형과 숫자 맵핑
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
    "폐기물처리시설(매립)",
    "폐기물처리시설(소각)",
    "폐기물처리시설(하수처리)",
    "폐기물처리시설(생물학적)",
    "폐기물처리시설(폐수)",
]
CarbonCateLen = len(CarbonCategories)


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
LubricantMove = CarbonClass.MovingCom(37, 73300, 0, 0)
# CNG
LNG = CarbonClass.MovingCom(39.4, 56100, 92, 3)


# 탈루배출
AirCon = CarbonClass.AirCon()
Refri = CarbonClass.Refri()

# 비료 사용
LimeFert = CarbonClass.LimeFert()
UreaFert = CarbonClass.UreaFert()

# 산림
HardWood = CarbonClass.HardWood()
SoftWood = CarbonClass.SoftWood()
Mixed = CarbonClass.Mixed()

# 페기물
Landfill = CarbonClass.Waste(517)
SolidWasteBio = CarbonClass.Waste(97.6)
Burning = CarbonClass.Waste(1052.40)
Sewage = CarbonClass.Waste(0.0285)
WasteWater = CarbonClass.Waste(0.0123)
NightSoil = CarbonClass.Waste(18.9)

# 대학소유동물
육성우 = CarbonClass.DairyCow(61.813, 19.953, 63.71, None, 450)
착유우 = CarbonClass.DairyCow(106.69, 19.953, 63.71, None, 350)
송아지 = CarbonClass.Beef(39.191, 0.621, 28.75, None, 350)
번식우 = CarbonClass.Beef(48.979, 0.621, 28.75, None, 350)
비육우 = CarbonClass.Beef(50.712, 0.621, 28.75, None, 350)
돼지 = CarbonClass.Pig(1.5, 0.183, 8.16, None, 70)
산란계 = CarbonClass.Chicken_Lay(None, 0.022, 0.147, None, 1.62)
육계 = CarbonClass.Turkey_Duck_Goose_OtherChicken(None, 0.016, 0.087, None, 0.71)
기타닭 = CarbonClass.Turkey_Duck_Goose_OtherChicken(None, 0.019, 0.117, None, 1.165)
면양 = CarbonClass.Lamb_Horse_Deer_Rabbit(8, 0.28, None, 1.17, 48.5)
산양 = CarbonClass.Lamb_Horse_Deer_Rabbit(5, 0.2, None, 1.37, 38.5)
말 = CarbonClass.Lamb_Horse_Deer_Rabbit(18, 2.34, None, 0.46, 377)
칠면조 = CarbonClass.Turkey_Duck_Goose_OtherChicken(None, 0.09, None, 0.74, 6.8)
오리 = CarbonClass.Turkey_Duck_Goose_OtherChicken(None, 0.03, None, 0.83, 2.7)
사슴 = CarbonClass.Lamb_Horse_Deer_Rabbit(20, 0.22, None, 1.17, 120)
토끼 = CarbonClass.Lamb_Horse_Deer_Rabbit(0.2297, 0.08, 8.1, None, 1.6)
거위 = CarbonClass.Turkey_Duck_Goose_OtherChicken(None, 0.03, None, 0.83, 2.7)

CarbonCateMap = {
    "고정연소": {
        "원유": CrudeOil,
        "휘발유": Gasoline,
        "실내등유": KeroseneInside,
        "보일러등유": KeroseneBoil,
        "경유": Diesel,
        "B-A유": B_A_Oil,
        "B-B유": B_B_Oil,
        "B-C유": B_C_Oil,
        "프로판": Propane,
        "부탄": Butane,
        "용제": Solvent,
        "항공용가솔린": AeroGasoline,
        "제트용가솔린": JetGasoline,
        "제트용등유": JetKerosene,
        "아스팔트": Asphalt,
        "윤활유": Lubricant,
        "석유코크": PetCoke,
        "천연가스": NaturalLPG,
        "국내무연탄": LocalHardCoal,
        "수입무연탄(연료용)": ForeignHardCoalFuel,
        "수입무연탄(원료용)": ForeignHardCoalRaw,
        "유연탄(연료용)": SoftCoalFuel,
        "유연탄(원료용)": SoftCoalRaw,
        "아역청탄": BituminousCoal,
        "코크스": Cokes,
    },
    "이동연소": {
        "휘발유": GasolineMove,
        "경유": DieselMove,
        "천연가스": LPGNaturalMove,
        "도시가스": LPGCityMove,
        "등유": KeroseneMove,
        "윤활유": LubricantMove,
        "LNG": LNG,
    },
    "탈루배출": {"에어컨": AirCon, "냉장고": Refri},
    "폐기물처리시설": {},
    "비료사용": {"석회질비료": LimeFert, "요소비료": UreaFert},
    "대학소유동물": {
        "육성우": 육성우,
        "착유우": 착유우,
        "송아지": 송아지,
        "번식우": 번식우,
        "비육우": 비육우,
        "돼지": 돼지,
        "산란계": 산란계,
        "육계": 육계,
        "기타닭": 기타닭,
        "면양": 면양,
        "산양": 산양,
        "말": 말,
        "칠면조": 칠면조,
        "오리": 오리,
        "사슴": 사슴,
        "토끼": 토끼,
        "거위": 거위,
    },
    "산림에의한흡수": {"침엽수": HardWood, "활엽수": SoftWood, "혼효림": Mixed},
    "전력": {"전력": Electric},
    "열": {"열": Heat},
    "수도": {"수도": Water},
    "폐기물": {
        "매립": Landfill,
        "고형폐기물의생물학적처리": SolidWasteBio,
        "소각": Burning,
        "하수": Sewage,
        "폐수": WasteWater,
        "분뇨": NightSoil,
    },
    "통근_통학": {},
    "출장": {},
    "위탁운영차량": {},
}
