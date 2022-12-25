from django.db import models


# 탄소 사용량을 저장하는 테이블


class Carbon(models.Model):
    CarbonActivity = models.TextField()  # 탄소가 발생된 활동의 이름
    CarbonData = models.FloatField()  # 발생된 탄소량
    CarbonUnit = models.TextField()  # 탄소량의 단위
    CarbonTrans = models.FloatField()  # kg 단위로 환산한 탄소량
    RootCom = models.ForeignKey(
        "Company.Company",
        related_name="RootComCarbon",
        on_delete=models.CASCADE,
        null=True,
    )  # root 노드
    BelongCom = models.ForeignKey(
        "Company.Company",
        related_name="BelongComCarbon",
        on_delete=models.CASCADE,
        null=True,
    )
    CarbonInfo = models.ForeignKey("CarbonInfo", on_delete=models.SET_NULL, null=True)


# 탄소 사용량의 정보를 저장하는 테이블
class CarbonInfo(models.Model):
    StartDate = models.DateField()  # 활동의 시작일
    EndDate = models.DateField()  # 활동의 종료일
    Location = models.TextField()  # 활동의 위치
    Scope = models.IntegerField()  # 탄소 배출 단계
    Chief = models.ForeignKey(
        "Human.Employee",
        related_name="ChiefCarbonInfo",
        on_delete=models.SET_NULL,
        null=True,
    )  # 관리자
    Category = models.IntegerField()  # 탄소 배출 원인과 숫자를 매핑 ex) 고정연소, 이동연소
    Division = models.TextField()  # 구분 : 저장 형태 {건물명 : '', 설비명:'', 연료정보:'', 연료량:''}
