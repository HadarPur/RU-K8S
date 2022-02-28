# Prometheus Queries
1) CPU Utilization vs Response Time:

Service A CPU Utilization:
```
sum(kube_metrics_server_pods_cpu{pod_container_name=~"service-a.*"} * 10e-8 / 0.14) / count(kube_pod_status_ready{pod=~"service-a.*",condition="true"})
```
Service B CPU Utilization:
```
sum(kube_metrics_server_pods_cpu{pod_container_name=~"service-b.*"} * 10e-8 / 0.14) / count(kube_pod_status_ready{pod=~"service-b.*",condition="true"})
```
Service C CPU Utilization:
```
sum(kube_metrics_server_pods_cpu{pod_container_name=~"service-c.*"} * 10e-8 / 0.14) / count(kube_pod_status_ready{pod=~"service-c.*",condition="true"})
```
Service D CPU Utilization:
```
sum(kube_metrics_server_pods_cpu{pod_container_name=~"service-d.*"} * 10e-8 / 0.14) / count(kube_pod_status_ready{pod=~"service-d.*",condition="true"})
```
Response Time:
```
avg(rate(flask_http_request_duration_seconds_sum{method="POST",path=~".*/load",status="200"}[1m])/rate(flask_http_request_duration_seconds_count{method="POST",path=~".*/load",status="200"}[1m]))*1000
```
2) Pods vs nodes:

Pods:
```
kube_endpoint_address_available{endpoint=~".*svc"}
```
Nodes:
```
sum(kube_node_status_condition{condition="Ready", status="true"})
```
3) Power vs Time:

Power:
```
sum(increase(flask_http_request_total{method="POST", status="200"}[30m]))
```
