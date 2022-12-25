conda activate tf
cd
cd venv/DjangoENV/bin
source activate
cd
cd projects/CarbonServerDjango

volName=CarbonVol # 데이터가 저장된 볼륨의 이름
dockerName=CarbonDB # mysql docker의 이름

# docker volume ls -q

# if [ "$volName" = "$?" ]; then
#     docker ps 
#     if [ ""]