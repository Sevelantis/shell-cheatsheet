docker run --rm -d --name node_exporter --net="host" --pid="host" -v "$PWD/:/host/" quay.io/prometheus/node-exporter:latest --path.rootfs=/host

#set ip address to 'hostname -I' in Prometheus/prometheus.yml

docker run --rm -d --name prometheus -p 9090:9090 -v $PWD/Prometheus/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus

docker run --rm -d --name=grafana -p 3456:3000 grafana/grafana

# HOW TO RUN
# note - cd into lab7/ dir
docker build -t flask-app:first Application/
docker run --rm -itd -p 5000:5000 --name flask-app flask-app:first 
