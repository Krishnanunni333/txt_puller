cp ../requirements.txt requirements.txt

docker build -t krishnanunni333/store-full-server:v0.1 . --no-cache

rm requirements.txt