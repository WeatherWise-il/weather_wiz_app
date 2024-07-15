FROM grafana/grafana:11.0.0
WORKDIR /etc/grafana/provisioning/dashboards
COPY ./provisioning/dashboards /etc/grafana/provisioning/dashboards
WORKDIR /the/workdir/path
COPY ./provisioning/datasources /etc/grafana/provisioning/datasources