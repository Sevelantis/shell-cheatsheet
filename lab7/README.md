# App
Simple flask REST API dockerised application. Includes generating logs and visualising logs using:
 - docker, docker-compose
 - python flask
 - fluent-bit
 - Loki (Grafana plugin)
 - Grafana (visual logs representation)

# Stack
1. Flask receives GET request
2. Flask 'logging' module prints necessary info to stdout
3. fluent-bit INPUT is stdout (24224) and OUTPUT - loki's local ip_address:port
4. Loki as Grafana plugin passes info to Grafana
5. Grafana enables to filter and visualise the logs.

# HOW TO RUN
```
git clone https://github.com/Sevelantis/SO2/
```
```
cd SO2/lab7/
```
```
docker-compose up -d --build
```
App is being hosted:
```
curl 127.0.0.1:5000
```
or open browser and type - you will see REST API's possible URLs & functionalities
```
127.0.0.1:5000
```
Open Grafana in browser and login with default L/P
```
127.0.0.1:3000
admin
admin
admin
admin
```
![Alt text](/readme-files/1.png?raw=true "a")

![Alt text](/readme-files/2.png?raw=true "b")

![Alt text](/readme-files/3.png?raw=true "c")

![Alt text](/readme-files/4.png?raw=true "d")

Now press -> 'Log browser, if everything is fine there should show up job(1)
Now press -> 'fluent-bit' -> Show Logs, set refresh 5s, if nothings happens -> update manually, unset 'wrap lines' for clarity

**Example api commands**
```
curl 127.0.0.1:5000/pow/4^7
curl 127.0.0.1:5000/factorial/9
curl 127.0.0.1:5000/sqrt/1234567
```
quit (-v to delete volumes -> manually configure Grafana)
```
docker-compose down -v
```
Clear all, all images (can be pulled back again, but consider using this command if your internet is slow)
```
docker rmi -f $(docker images -a -q)
```
check docker processes
```
docker ps
```
check volumes
```
docker volume ls
```