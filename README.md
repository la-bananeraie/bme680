# bme680

## Setup Repo
```
virtualenv env
source env/bin/activate
pip3 install -r requirements.txt
```

## Setup InfluxDb
Metrics are logged here
Default port: 8086
```
// Add influxdb to apt source list
wget -qO- https://repos.influxdata.com/influxdb.key | sudo apt-key add -
source /etc/os-release
echo "deb https://repos.influxdata.com/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/influxdb.list

// Update apt and install influxdb
sudo apt update && sudo apt install -y influxdb

// Start the influx service and set it to run at boot
sudo systemctl unmask influxdb.service
sudo systemctl start influxdb
sudo systemctl enable influxdb.service

// Usage example 
$ influx(db?)
> create database home
> use home

> create user grafana with password '<passwordhere>' with all privileges
> grant all privileges on home to grafana

> show users

user admin
---- -----
grafana true
```

## Setup Grafana
```
// Add Grafana to apt source list
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee /etc/apt/sources.list.d/grafana.list

// Update and install via apt
sudo apt update && sudo apt install -y grafana

// Start service and set it to run at boot
sudo systemctl unmask grafana-server.service
sudo systemctl start grafana-server
sudo systemctl enable grafana-server.service
```

Navigate to http://ipaddress:3000 to see Grafana UI and confirm it's working.

Sample Grafana dash query with InfluxDB as its source data
`SELECT temperature FROM "bme680_data" WHERE $timeFilter`

Based on Simon Hearne's blog posts [here](https://simonhearne.com/2020/pi-influx-grafana/) and [here](https://simonhearne.com/2020/pi-metrics-influx/)
