# 도커 컴포즈를 활용하여 자동 배포

# 도커 컨테이너 및 이미지 삭제
sudo docker-compose down

# db_config.py 파일 및 로그 보존
sudo mv config.py ..
sudo mv /logs/Server.log ..

# 디렉토리(코드) 삭제
cd ..
sudo rm -r CarbonServerDjango

# 코드 가져오기 
git clone https://github.com/ChoiMoonSeok/CarbonServerDjango.git

# 디렉토리로 이동
sudo mv config.py CarbonServerDjango
sudo mv Server.log CarbonServerDjango/logs
cd CarbonServerDjango

# 도커 빌드 및 실행
sudo docker-compose up --build