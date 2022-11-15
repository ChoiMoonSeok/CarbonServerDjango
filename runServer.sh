# 도커 컨테이너 및 이미지 삭제
sudo docker rm -f $(sudo docker ps -aq)
sudo docker rmi -f $(sudo docker ps -aq)

# db_config.py 파일 보존
sudo mv db_config.py ..

# 디렉토리(코드) 삭제
cd ..
sudo rm -r CarbonServerDjango

# 코드 가져오기 
git clone https://github.com/ChoiMoonSeok/CarbonServerDjango.git

# 디렉토리로 이동
cd mv db_config.py CarbonServerDjango
cd CarbonServerDjango

# 도커 빌드 및 실행
sudo docker build -t carbonserver:0.0 .
sudo docker run -it -v $(pwd):/home carbonserver:0.0