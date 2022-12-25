from django.db import models

# 회사의 모든고용인을 저장하는 테이블


class Employee(models.Model):
    Name = models.TextField()  # 문자열
    PhoneNum = models.TextField()  # 문자열
    Email = models.EmailField()  # email 필드
    RootCom = models.ForeignKey(  # 외래키 가장 위에 있는 회사
        "Company.Company", on_delete=models.CASCADE, null=True, blank=True
    )  # 고용인이 다니는 회사의 루트 회사(지주 회사)
    BelongCom = models.ForeignKey(
        "Company.Department", on_delete=models.CASCADE, null=True, blank=True
    )  # 고용인이 다니는 회사
    JobPos = models.TextField()  # 직위
    IdentityNum = models.TextField()  # 사번


# 회원가입한 유저를 저장하는 테이블


class User(models.Model):
    UID = models.CharField(max_length=10, primary_key=True)  # 회원가입한 ID
    PassWd = models.CharField(max_length=10, unique=True)  # 회원가입한 비밀번호
    DetailInfo = models.ForeignKey("Human.Employee", on_delete=models.CASCADE)
    Authorization = models.IntegerField(null=True, blank=True)  # 접근 권한
