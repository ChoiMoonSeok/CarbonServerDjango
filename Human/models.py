from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
)  # 로그인 기능을 구현하기 위해 상속받는 모델
from django.contrib.auth.models import PermissionsMixin

# 회사의 모든고용인을 저장하는 테이블


class Employee(models.Model):
    Name = models.TextField()  # 문자열
    PhoneNum = models.TextField()  # 문자열
    RootCom = models.ForeignKey(  # 외래키, 가장 위에 있는 회사
        "Company.Company", on_delete=models.CASCADE, null=True, blank=True
    )  # 고용인이 다니는 회사의 루트 회사(지주 회사)
    BelongCom = models.ForeignKey(
        "Company.Department", on_delete=models.CASCADE, null=True, blank=True
    )  # 고용인이 다니는 회사
    JobPos = models.TextField()  # 직위
    IdentityNum = models.TextField()  # 사번
    Authorization = models.IntegerField(null=True, blank=True)  # 접근 권한


# 회원 가입 관리


class UserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, Email, password):
        if not Email:
            raise ValueError("Please enter a Email")
        if not password:
            raise ValueError("Please enter a password")

        User = self.model(
            Email=self.normalize_email(Email),
        )
        User.set_password(password)
        User.save(using=self._db)
        return User

    def create_superuser(self, Email, password):
        if not Email:
            raise ValueError("Please enter a Email")
        if not password:
            raise ValueError("Please enter a password")

        User = self.create_user(Email, password=password)

        User.is_superuser = True
        User.save(using=self._db)
        return User


# 회원가입한 유저를 저장하는 테이블


class User(AbstractBaseUser, PermissionsMixin):  # 로그인 구현을 위해 AbstractBaseUser를 상속
    Email = models.EmailField(primary_key=True)  # email 필드
    DetailInfo = models.ForeignKey(
        "Human.Employee", on_delete=models.CASCADE, null=True
    )

    objects = UserManager()

    USERNAME_FIELD = "Email"

    def __str__(self):
        return self.Email

    @property
    def is_staff(self):
        return self.is_superuser
