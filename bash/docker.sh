# Start a docker container based on the latest image.
docker run --name cities -itd  \
  -v /home/jeff/of/cities:/mnt \
  ofiscal/tax.co:latest
  # -p 7777:8888 -h 127.0.0.1    \

docker exec -it cities bash
cd mnt

docker stop cities && docker rmi cities
