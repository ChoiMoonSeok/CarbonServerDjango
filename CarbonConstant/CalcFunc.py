from Constants import Electric

# 전력 사용량의 탄소 배출량을 계산하는 함수
def ElecUsage(usage):
    ElecCar = (
        (usage * Electric.CO2_EF)
        + (usage * Electric.NH4_EF * Electric.NH4_MULTIPLY_CON)
        + (usage * Electric.N2O_EF * Electric.N2O_MULTIPLY_CON)
    )

    return ElecCar
