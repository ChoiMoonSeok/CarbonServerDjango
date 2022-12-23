from django.db import models

# 회사의 모든고용인을 저장하는 테이블


class Employee(models.Model):
    Name = models.TextField()  # 문자열
    PhoneNum = models.TextField()  # 문자열
    Email = models.EmailField()  # email 필드
    RootCom = models.ForeignKey(  # 외래키 가장 위에 있는 회사
        "Company", on_delete=models.CASCADE
    )  # 고용인이 다니는 회사의 루트 회사(지주 회사)
    BelongCom = models.ForeignKey(
        "Department", on_delete=models.CASCADE, null=True, blank=True
    )  # 고용인이 다니는 회사
    JobPos = models.TextField()  # 직위
    IdentityNum = models.TextField()  # 사번


# 회원가입한 유저를 저장하는 테이블


class User(models.Model):
    UID = models.CharField(max_length=10, primary_key=True)  # 회원가입한 ID
    PassWd = models.CharField(max_length=10, unique=True)  # 회원가입한 비밀번호
    DetailInfo = models.ForeignKey("Employee", on_delete=models.CASCADE)
    Authorization = models.IntegerField(null=True, blank=True)  # 접근 권한


# 회원사를 저장하는 테이블


class Company(models.Model):
    ComName = models.TextField()  # 사명
    Scope1 = models.IntegerField()
    Scope2 = models.IntegerField()
    Scope3 = models.IntegerField()
    Chief = models.ForeignKey(
        "Employee",
        related_name="ChiefCom",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )  # 대표자
    Depth = models.IntegerField()  # 깊이
    Admin = models.ForeignKey(  # 관리자
        "Employee",
        related_name="AdminCom",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    Classification = models.TextField(null=True, blank=True)
    Description = models.TextField(null=True, blank=True)
    Location = models.TextField(null=True, blank=True)


# 부서명을 저장하는 테이블


class Department(models.Model):
    RootCom = models.ForeignKey(
        "Company", related_name="RootCom", on_delete=models.CASCADE, null=True
    )  # root 노드
    BelongCom = models.ForeignKey(
        "Company",
        related_name="BelongCom",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )  # 바로 위 노드
    SelfCom = models.ForeignKey(
        "Company",
        related_name="SelfCom",
        on_delete=models.CASCADE,
    )


# 탄소 사용량을 저장하는 테이블


class Carbon(models.Model):
    CarbonActivity = models.TextField()  # 탄소가 발생된 활동의 이름
    CarbonData = models.FloatField()  # 발생된 탄소량
    CarbonUnit = models.TextField()  # 탄소량의 단위
    CarbonTrans = models.FloatField()  # kg 단위로 환산한 탄소량
    RootCom = models.ForeignKey(
        "Company", related_name="RootComCarbon", on_delete=models.CASCADE, null=True
    )  # root 노드
    BelongCom = models.ForeignKey(
        "Company", related_name="BelongComCarbon", on_delete=models.CASCADE, null=True
    )
    CarbonInfo = models.ForeignKey("CarbonInfo", on_delete=models.SET_NULL, null=True)


# 탄소 사용량의 정보를 저장하는 테이블
class CarbonInfo(models.Model):
    StartDate = models.DateField()  # 활동의 시작일
    EndDate = models.DateField()  # 활동의 종료일
    Location = models.TextField()  # 활동의 위치
    Scope = models.IntegerField()  # 탄소 배출 단계
    Chief = models.ForeignKey(
        "Employee", related_name="ChiefCarbonInfo", on_delete=models.SET_NULL, null=True
    )  # 관리자
    Category = models.IntegerField()  # 탄소 배출 원인과 숫자를 매핑 ex) 고정연소, 이동연소
    Division = models.TextField()  # 구분 : 저장 형태 {건물명 : '', 설비명:'', 연료정보:'', 연료량:''}
