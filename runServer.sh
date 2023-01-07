# 도커 컴포즈를 활용하여 자동 배포

# 도커 컨테이너 및 이미지 삭제
docker-compose down

# db_config.py 파일 및 로그 보존
sudo mv config.py ..
sudo mv logs ..
sudo mv .env ..

# db schema migration 파일 유지
sudo mv Carbon/migrations ..
cd ..
sudo mv migrations Car_migrate

cd CarbonServerDjango
sudo mv Company/migrations ..
cd ..
sudo mv migrations Com_migrate

cd CarbonServerDjango
sudo mv Human/migrations ..
cd ..
sudo mv migrations Hu_migrate

# 구형 코드 삭제
sudo rm -r CarbonServerDjango

# 코드 가져오기 
git clone https://github.com/ChoiMoonSeok/CarbonServerDjango.git

# migration 파일 원위치로 돌리기
sudo mv Com_migrate/migrations CarbonServerDjango/Company
sudo mv Car_migrate/migrations CarbonServerDjango/Carbon
sudo mv Hu_migrate/migrations CarbonServerDjango/Human

# 디렉토리로 이동
sudo mv config.py CarbonServerDjango
sudo mv logs CarbonServerDjango
sudo mv .env CarbonServerDjango

cd CarbonServerDjango

# 도커 빌드 및 실행
docker-compose up --build