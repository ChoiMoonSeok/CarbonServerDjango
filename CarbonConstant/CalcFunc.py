from Constants import Electric

# 탄소 배출 유형과 숫자 맵핑
고정연소 = 0
이동연소 = 1
탈루배출 = 2
폐기물처리시설 = 3
비료사용 = 4
대학소유동물 = 5
산림에의한흡수 = 6
전력 = 7
열 = 8
수도 = 9
폐기물 = 10
통근_통학 = 11
출장 = 12
위탁운영차량 = 13


# 전력 사용량의 탄소 배출량을 계산하는 함수
def ElecUsage(usage):
    ElecCar = (
        (usage * Electric.CO2_EF)
        + (usage * Electric.NH4_EF * Electric.NH4_MULTIPLY_CON)
        + (usage * Electric.N2O_EF * Electric.N2O_MULTIPLY_CON)
    )

    return ElecCar
