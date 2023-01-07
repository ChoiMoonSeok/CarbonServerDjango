from .Constants import Electric

# 탄소 배출 유형과 숫자 맵핑
CarbonCateLen = 13
CarbonCategories = [
    "고정연소",
    "이동연소" "탈루배출",
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
        (usage * Electric.CO2_EF)
        + (usage * Electric.NH4_EF * Electric.NH4_MULTIPLY_CON)
        + (usage * Electric.N2O_EF * Electric.N2O_MULTIPLY_CON)
    )

    return ElecCar
