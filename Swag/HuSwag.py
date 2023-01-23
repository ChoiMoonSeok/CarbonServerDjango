from drf_yasg import openapi

Email = openapi.Schema(
    type=openapi.TYPE_STRING,
    description="문자열 형태\n\
            로그인 할 유저의 email 주소\n\
            ex) 홍길동 유저가 회원가입시 email에 hong@gnu.ac.kr을 입력했다면\
                hong@gnu.ac.kr 을 입력",
)

password = openapi.Schema(
    type=openapi.TYPE_STRING,
    description="문자열 형태\n\
            로그인 할 유저의 비밀번호\n\
            ex) 홍길동 유저가 회원가입시 비밀번호로 1234를 입력했다면\
                1234 를 입력",
)

Name = openapi.Schema(
    type=openapi.TYPE_STRING,
    description="문자열 형태\n\
            로그인 할 유저의 비밀번호\n\
            ex) 홍길동 유저가 회원가입시 비밀번호로 1234를 입력했다면\
                1234 를 입력",
)

PhoneNum = openapi.Schema(
    type=openapi.TYPE_STRING,
    description="문자열 형태\n\
            고요인의 전화번호\n\
            ex) 홍길동 유저의 전화번호가 1234라면\
                1234 를 입력",
)

JobPos = openapi.Schema(
    type=openapi.TYPE_STRING,
    description="문자열 형태\n\
            고용인의 직위\n\
            ex) 홍길동이 부장이라면\
                부장 을 입력",
)

IdentityNum = openapi.Schema(
    type=openapi.TYPE_STRING,
    description="문자열 형태\n\
            고용인의 사번\n\
            ex) 홍길동의 사번이 1234라면\
                1234 를 입력",
)

Authorization = openapi.Schema(
    type=openapi.TYPE_STRING,
    description="문자열 형태\n\
            고용인의 접근 권한\n\
            ex) 홍길동의 사번이 1234라면\
                1234 를 입력",
)

RootCom = openapi.Schema(
    type=openapi.TYPE_STRING,
    description="문자열 형태\n\
            고용인이 소속된 회사의 모회사\n\
            ex) 홍길동이 삼성전자 소속이라면\
                삼성전자의 모회사인 삼성을 입력",
)

BelongCom = openapi.Schema(
    type=openapi.TYPE_STRING,
    description="문자열 형태\n\
            고용인이 소속된 회사\n\
            ex) 홍길동이 삼성전자 소속이라면\
                삼성전자를 입력",
)

Employee = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "Name": Name,
        "PhoneName": PhoneNum,
        "JobPos": JobPos,
        "IdentityNum": IdentityNum,
        "Authorization": Authorization,
        "RootCom": RootCom,
        "BelongCom": BelongCom,
    },
)
