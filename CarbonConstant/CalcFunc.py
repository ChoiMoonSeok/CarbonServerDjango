import Constants

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


# 전력 사용량의 탄소 배출량을 계산하는 함수
def ElecUsage(usage):
    ElecCar = (
        (usage * Constants.Electric.CO2_EF)
        + (usage * Constants.Electric.NH4_EF * Constants.Electric.NH4_MULTIPLY_CON)
        + (usage * Constants.Electric.N2O_EF * Constants.Electric.N2O_MULTIPLY_CON)
    )

    return ElecCar


# 열 사용량
def HeatUsage(usage):
    return usage * Constants.Heat.HEAT_EF


# 수도 사용량
def WaterUsage(usage):
    return usage * Constants.Water.WATER_EF


# 탈루 배출
# def FugitiveUsage(usage, num, type):
#     if type == HFC:
#         Constants.탈루배출.REFRI_HFC_134A_MULTI * R
#     elif type == R_407C:

#     else:
