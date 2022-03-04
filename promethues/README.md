# Grafana + Prometheus integration
1) Install helm:
```
curl https://baltocdn.com/helm/signing.asc | sudo apt-key add -
```
```
sudo apt-get install apt-transport-https --yes
```
```
echo "deb https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
```
```
sudo apt-get update
```
```
sudo apt-get install helm
```
2) Add bitnami using helm:
```
helm repo add bitnami https://charts.bitnami.com/bitnami
```
3) Install kube-prometheus via bitnami:

```
helm upgrade --install monitoring bitnami/kube-prometheus -n monitoring --create-namespace --set alertmanager.enabled=false,prometheus.persistence.enabled=true,prometheus.service.type=LoadBalancer,prometheus.resources.requests.cpu=30m,prometheus.resources.requests.memory=512Mi,exporters.node-exporter.enabled=false,kubelet.enabled=false,kubeApiServer.enabled=false,kubeControllerManager.enabled=false,kubeScheduler.enabled=false,coreDns.enabled=false,kubeProxy.enabled=false

```
4) Install metrics-server-exporter: https://github.com/HadarPur/RU-K8S-FinalProject/tree/master/promethues/metrics-server-exporter
5) Install prometheus-flask-exporter: https://github.com/HadarPur/RU-K8S-FinalProject/tree/master/promethues/prometheus-flask-exporter

6) Install Istio: https://github.com/HadarPur/RU-K8S-FinalProject/tree/master/promethues/istio

7) Export the ip for prometheus:
```
export SERVICE_IP=$(kubectl get svc --namespace monitoring monitoring-kube-prometheus-prometheus --template "{{ range (index .status.loadBalancer.ingress 0) }}{{ . }}{{ end }}")
```
8) Get prometheus url:
```
echo "Prometheus URL: http://$SERVICE_IP:9090/"
```


