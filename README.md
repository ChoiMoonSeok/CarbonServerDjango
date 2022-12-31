# carbon-footprint 프로젝트의 서버

# 서버 실행 방법
## 1. 우분투 20.04 환경을 준비합니다.
## 2. 해당 환경에 docker와 docker-compose를 설치합니다.
## 3. 이 깃허브에서 코드를 git clone "repository" 하여 가져옵니다.
## 4. 코드가 저장된 디렉토리에서 bash runServer.sh를 실행합니다.
## 5. 해당 서버에 접속하여 제대로 동작하는지 확인합니다.
이 서버의 경우 Api 서버이며, ~서버 ip/{사용자가 설정한 포트 번호}/swagger로 이동하면 Api에 관한 설명을 확인할 수 있습니다.

## 서버 실행 시 주의 사항
.env 파일과 config.py 보안 상의 이유로 파일이 제공되지 않습니다. 본인의 원하는 형태로 작성하여 주십시요.

## config.py 예시
SECRET_KEY = "본인이 선택한 비밀 암호화 키"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "mysql에서 본인이 생성한 데이터베이스의 이름",
        "USER": "root",
        "PASSWORD": "본인이 선택한 비밀번호",
        "HOST": "db"
    }
}


## .env 예시
MYSQL_ROOT_PASSWORD="본인이 설정한 mysql의 루트 비밀번호"
DB_VOLUME="데이터를 저장할 볼륨 이름"
CARBON_PORT=본인이 사용할 포트 번호

# Api 명세 및 사용법
## 조직설계
~서버ip주소/Organization/<회사명>의 형태로 서버에 질의합니다. 해당 Api는 입력받은 회사(단 여기서 회사는 반드시 가장 높은 회사, 지주회사와 같은 회사이어야 합니다.) 및 연결 자회사들을 모두 찾아 계층 형태로 만들어 반환합니다. 즉 조직도를 반환합니다. 

## Preview
~서버ip주소/Preview/<회사명>의 형태로 서버에 질의합니다. 해당 Api는 입력받은 회사 혹은 부서의 모든 연결 자회사의 탄소 배출량을 합하여 보여줍니다.


## PreviewInfo
~서버ip주소/PreviewInfo/<회사명>의 형태로 서버에 질의합니다. 해당 Api는 사용자가 원하는 형태로 부서, 회사명 등 메타 데이터를 수정할 수 있습니다. 


## 조직설계 사용자
~서버ip주소/User/<회사명>의 형태로 서버에 질의합니다. 해당 Api는 입력한 회사와 해당 회사의 모든 연결 자회사의 직원들을 모두 반환합니다.


## 탄소배출 측정

