# 전력 사용량의 탄소 발생량을 계산하기 위한 상수 목록
class Electric:

    CO2_EF = 0.4653
    NH4_EF = 0.0054
    N2O_EF = 0.0027
    MULTIPLY_CON_NH = 21
    MULTIPLY_CON_N2O = 310

    def CO2_EQ(self, usage):
        eq = (
            (usage * self.CO2_EF)
            + (usage * self.NH4_EF * self.MULTIPLY_CON_NH)
            + (usage * self.N2O_EF * self.MULTIPLY_CON_N2O)
        )

        return eq


# 열 사용량을 계산하는 클래스
class Heat:
    HEAT_EF = 0.2498  # EF(tCO2eq/Gj)

    def CO2_EQ(self, usage):
        eq = usage * self.HEAT_EF

        return eq


# 물 사용량을 계산하는 클래스
class Water:

    WATER_EF = 332  # (gCO2eq/m^3)

    def CO2_EQ(self, usage):
        eq = usage * self.WATER_EF * (10**-6)


# 고정 연소에 대한 값을 저장하는 클래스
class StationCom:
    MULTIPLY_CON_CH = 21
    MULTIPLY_CON_N2O = 310
    EMISSION_EF = 1

    def __init__(self, HEAT_VAL, C02_EF, CH4_EF, N2O_EF, STATE_CON):
        self.HEAT_VAL = HEAT_VAL
        self.CO2_EF = C02_EF
        self.CH4_EF = CH4_EF
        self.N2O_EF = N2O_EF
        self.STATE_CON = STATE_CON

    def CO2_EQ(self, usage):
        eq = (
            usage
            * self.STATE_CON
            * self.HEAT_VAL
            * self.EMISSION_EF
            * (
                self.CO2_EF
                + self.CH4_EF * self.MULTIPLY_CON_CH
                + self.N2O_EF * self.MULTIPLY_CON_N2O
            )
        )
        return eq


# 이동연소를 저장하는 클래스
class MovingCom:
    MULTIPLY_CON_CH = 21
    MULTIPLY_CON_N2O = 310
    STATE_CON = 10**-9

    def __init__(self, HEAT_VAL, C02_EF, CH4_EF, N2O_EF):
        self.HEAT_VAL = HEAT_VAL
        self.CO2_EF = C02_EF
        self.CH4_EF = CH4_EF
        self.N2O_EF = N2O_EF

    def CO2_EQ(self, usage):
        eq = (
            usage
            * self.STATE_CON
            * self.HEAT_VAL
            * (
                self.CO2_EF
                + self.CH4_EF * self.MULTIPLY_CON_CH
                + self.N2O_EF * self.MULTIPLY_CON_N2O
            )
        )
        return eq


# 탈루배출에 관한 내용을 저장하는 클래스
# 변경 사항에 따라 어떻게 달라진건지 질문 필요
class FugitiveEmission:
    HFC_134_A_X = 0.3
    HFC_134_A_GWP = 1300
    R_407C_X = 5.5
    R_410A_X = 5.5
    R_407C_GWP = 1525.5
    R_410A_GWP = 1725

    def CO2_EQ(self, usage, nums):
        pass


class AirCon(FugitiveEmission):
    def CO2_EQ(self, usage, nums, kind):
        if kind == 407:
            eq = usage * (self.R_407C_X / 100) * nums * self.R_407C_GWP
        else:
            eq = usage * (self.R_410A_X / 100) * nums * self.R_410A_GWP
        return eq


class Refri(FugitiveEmission):
    def CO2_EQ(self, usage, nums):
        eq = usage * (self.HFC_134_A_X / 100) * nums
        return eq


class Fertilizer:
    석회고토_EF = 130
    석회석_EF = 120
    패화석_EF = 120
    요소비료_EF = 200
    질소질비료_EF = 12.5

    def CO2_EQ(self):
        pass


class LimeFert(Fertilizer):
    def CO2_EQ(self, usage, kind):
        if kind == "석회고토":
            eq = usage * self.석회고토_EF * 44 / 12
        elif kind == "석회석":
            eq = usage * self.석회석_EF * 44 / 12
        else:
            eq = usage * self.패화석_EF * 44 / 12

        return eq


class UreaFert(Fertilizer):
    def CO2_EQ(self, usage):
        eq = usage * self.요소비료_EF * 44 / 12
        return eq


class NitroFert(Fertilizer):  # 질문 후 작성
    def CO2_EQ(self):
        return super().CO2_EQ()


class Forest:
    침엽수_Gw = 4
    활엽수_Gw = 4
    혼효림_Gw = 4
    침엽수_CF = 510
    활엽수_CF = 480
    혼효림_CF = 470
    침엽수_R = 0.28
    활엽수_R = 0.47
    혼효림_R = 0.345
    조림_Bw = 20
    손실_Bw = 120

    def CO2_EQ(self, area):
        pass


class SoftWood(Forest):
    def CO2_EQ(self, area, kind):
        if kind == "임야면적":
            eq = area * self.침엽수_Gw * self.침엽수_CF * (1 + self.침엽수_R) * 44 / 12
        elif kind == "조림면적":
            eq = area * self.조림_Bw * self.침엽수_CF * (1 + self.침엽수_R) * 44 / 12
        else:
            eq = -area * self.손실_Bw * self.침엽수_CF * (1 + self.침엽수_R) * 44 / 12
        return eq


class HardWood(Forest):
    def CO2_EQ(self, area, kind):
        if kind == "임야면적":
            eq = area * self.활엽수_Gw * self.침엽수_CF * (1 + self.활엽수_R) * 44 / 12
        elif kind == "조림면적":
            eq = area * self.조림_Bw * self.침엽수_CF * (1 + self.활엽수_R) * 44 / 12
        else:
            eq = -area * self.손실_Bw * self.침엽수_CF * (1 + self.활엽수_R) * 44 / 12
        return eq


class Mixed(Forest):
    def CO2_EQ(self, area, kind):
        if kind == "임야면적":
            eq = area * self.혼효림_Gw * self.침엽수_CF * (1 + self.혼효림_R) * 44 / 12
        elif kind == "조림면적":
            eq = area * self.조림_Bw * self.침엽수_CF * (1 + self.혼효림_R) * 44 / 12
        else:
            eq = -area * self.손실_Bw * self.침엽수_CF * (1 + self.혼효림_R) * 44 / 12
        return eq


class Waste:
    def __init__(self, EF):
        self.EF = EF

    def CO2_EQ(self, usage):
        eq = usage * self.EF * (10**-3)
        return eq
