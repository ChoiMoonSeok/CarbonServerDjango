from django.db import models

# 회원사를 저장하는 테이블


class Company(models.Model):
    ComName = models.TextField()  # 사명
    Scope1 = models.IntegerField()
    Scope2 = models.IntegerField()
    Scope3 = models.IntegerField()
    Chief = models.ForeignKey(
        "Human.Employee",
        related_name="ChiefCom",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )  # 대표자
    Admin = models.ForeignKey(  # 관리자
        "Human.Employee",
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
    DepartmentName = models.TextField(default=None)
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
    Depth = models.IntegerField()  # 깊이
