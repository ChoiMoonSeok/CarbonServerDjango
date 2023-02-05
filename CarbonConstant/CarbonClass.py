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
        return eq


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


# 혜미 누나한테 질문
class Animal:
    N20_EF_Dic = {
        "혐기성늪": 0,
        "액체/슬러지": 0.0005,
        "고체저장": 0.0005,
        "건조부지": 0.02,
        "목장/방목": None,
        "일일살포": 0,
        "소화조": 0,
        "연료로사용": None,
        "WithLitter": 0.001,
        "WithoutLitter": 0.001,
    }

    MS_Type = {
        "혐기성늪": None,
        "액체/슬러지": None,
        "고체저장": None,
        "건조부지": None,
        "목장/방목": None,
        "일일살포": None,
        "소화조": None,
        "연료로사용": None,
        "기타": None,
        "WithLitter": None,
        "WithoutLitter": None,
    }

    def __init__(self, CH4_EF_장내발효, CH4_EF_분뇨관리, Nex, Nrate, TAM):
        self.CH4_EF_장내발효 = CH4_EF_장내발효
        self.CH4_EF_분뇨관리 = CH4_EF_분뇨관리
        self.Nex = Nex
        self.Nrate = Nrate
        self.TAM = TAM

    def CO2_EQ(self, MS, nums):

        self.N2O_EF = self.N20_EF_Dic[MS]
        self.MS = self.MS_Type[MS]
        if self.CH4_EF_장내발효 == None:
            Ch4_In = 0
        else:
            Ch4_In = self.CH4_EF_장내발효 * nums
        Ch4_excretion = self.CH4_EF_분뇨관리 * nums

        if self.Nex == None:
            self.Nex = self.Nrate * self.TAM / 1000 * 365

        if self.N2O_EF == None:
            return (Ch4_excretion + Ch4_In) * 21

        if MS == None:
            N2O_excretion = nums * self.Nex * self.N2O_EF * 44 / 28 * (10**-3)
        else:
            N2O_excretion = (
                nums * self.Nex * self.MS * self.N2O_EF * 44 / 28 * (10**-3)
            )

        ans = (Ch4_excretion + Ch4_In) * 21 + N2O_excretion * 310

        return ans


class DairyCow(Animal):
    MS_Type = {
        "혐기성늪": 4,
        "액체/슬러지": 38,
        "고체저장": 0,
        "건조부지": 0,
        "목장/방목": 20,
        "일일살포": 29,
        "소화조": 2,
        "연료로사용": 7,
        "기타": 0,
        "WithLitter": None,
        "WithoutLitter": None,
    }


class Beef(Animal):
    MS_Type = {
        "혐기성늪": 0,
        "액체/슬러지": 0,
        "고체저장": 0,
        "건조부지": 46,
        "목장/방목": 50,
        "일일살포": 2,
        "소화조": 0,
        "연료로사용": 2,
        "기타": 0,
        "WithLitter": None,
        "WithoutLitter": None,
    }


class Pig(Animal):
    MS_Type = {
        "혐기성늪": 0,
        "액체/슬러지": 40,
        "고체저장": 0,
        "건조부지": 54,
        "목장/방목": 0,
        "일일살포": 0,
        "소화조": 0,
        "연료로사용": 7,
        "기타": 0,
        "WithLitter": None,
        "WithoutLitter": None,
    }


class Chicken_Lay(Animal):
    MS_Type = {
        "혐기성늪": 0,
        "액체/슬러지": None,
        "고체저장": None,
        "건조부지": None,
        "목장/방목": None,
        "일일살포": None,
        "소화조": None,
        "연료로사용": None,
        "기타": None,
        "WithLitter": 0,
        "WithoutLitter": 100,
    }


class Lamb_Horse_Deer_Rabbit(Animal):
    MS_Type = {
        "혐기성늪": 0,
        "액체/슬러지": 0,
        "고체저장": 0,
        "건조부지": 0,
        "목장/방목": 100,
        "일일살포": 0,
        "소화조": 0,
        "연료로사용": 0,
        "기타": 0,
        "WithLitter": None,
        "WithoutLitter": None,
    }


class Turkey_Duck_Goose_OtherChicken(Animal):
    MS_Type = {
        "혐기성늪": None,
        "액체/슬러지": None,
        "고체저장": None,
        "건조부지": None,
        "목장/방목": None,
        "일일살포": None,
        "소화조": None,
        "연료로사용": None,
        "기타": None,
        "WithLitter": 100,
        "WithoutLitter": 0,
    }


# 폐기물처리시설 소각
class Burning:
    OF = 1
    N2O_EF = None

    BurningTech = {
        "연속식 - 고정상": 0.0002,
        "연속식 - 유동상": 0,
        "준연속식 - 고정상": 0.006,
        "준연속식 - 유동상": 0.188,
        "회분식(배치형) - 고정상": 0.06,
        "회분식(배치형) - 유동상": 0.237,
    }

    def __init__(self, dm, CF, FCF):
        self.dm = dm
        self.CF = CF
        self.FCF = FCF

    def CO2_EQ(self, usage, kind):

        CO2 = usage

        if self.dm != None:
            CO2 *= self.dm
        if self.CF != None:
            CO2 *= self.CF
        if self.FCF != None:
            CO2 *= self.FCF

        CO2 = CO2 * self.OF * 44 / 12

        CH4 = usage * self.BurningTech[kind] * (10**-3)
        N2O = usage * self.N2O_EF * (10**-3)

        ans = CO2 + CH4 * 21 + N2O * 310

        return ans


class BurningIndividual(Burning):
    N2O_EF = 39.8


class BurningCom(Burning):
    N2O_EF = 113.19


class BurningComSludge(Burning):
    N2O_EF = 408.41


class BurningComWaste(Burning):
    N2O_EF = 113.19


# 하수처리
class FoulWater:
    CH4_EF = 0.01532
    N2O_EF = 0.005

    def CO2_EQ(self, usage, BODIN, BODOUT, TNIN, TNOUT, R):
        CH4 = ((BODIN - BODOUT) * (10**-3) * usage * self.CH4_EF - R) * (10**-3)
        N2O = (TNIN - TNOUT) * usage * self.N2O_EF * 44 / 28 * (10**-6)

        return CH4 * 21 + N2O * 310


# 폐수처리
class WaterWaste:
    EF = 0.2

    def CO2_EQ(self, usage, CODIN, CODOUT, R):
        CH4 = ((CODIN - CODOUT) * usage * self.EF - R) * (10**-6)

        return CH4 * 21


# 생물학적
class BioWaste:
    pass


# 매립
class Digging:
    pass
