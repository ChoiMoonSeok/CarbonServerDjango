# Carbon

## 참고 사항
- __init__.py, apps.py 의 경우는 Django에서 자동으로 생성 및 관리하는 파일이므로 코드를 편집할 이유는 없음
- admin.py는 models에서 정의한 데이터베이스 스키마를 관리자 페이지에 등록하는 파일

## models.py
- 탄소 사용 내역을 저장하는 테이블을 정의
- Carbon과 CarbonInfo 테이블로 구성
- Carbon과 CarbonInfo는 외래키로 연결 됨

## serializer.py
- models에서 정의한 테이블에서 쿼리한 데이터를 변환하는 파일
- django orm의 경우 쿼리한 데이터를 django 고유의 객체(QuerySet)로 생성 및 저장
- QuerySet을 일반적인 형태의 json으로 변환하는 함수를 정의하는 파일

## urls.py
- views.py에서 정의한 함수들을 실행시킬 url을 지정하는 파일

## views.py
- urls.py에서 지정받은 url에서 실행시킬 함수를 지정하는 파일
- 실질적인 코드의 작성의 대부분 해당 파일에 작성