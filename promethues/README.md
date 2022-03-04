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
4) Install metrics-server-exporter:
```
kubectl apply -f https://raw.githubusercontent.com/olxbr/metrics-server-exporter/master/deploy/00-permissions-metrics-server-exporter.yaml -n kube-system
```
```
kubectl apply -f https://raw.githubusercontent.com/olxbr/metrics-server-exporter/master/deploy/10-deployment-metrics-server-exporter.yaml -n kube-system
```
```
kubectl apply -f https://raw.githubusercontent.com/olxbr/metrics-server-exporter/master/deploy/20-service-metrics-server-exporter.yaml -n kube-system
```

5) Created a metrics-server.yaml:
```
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: metrics-server-exporter
  namespace: kube-system
spec:
  endpoints:
    - interval: 30s
      port: metrics
  namespaceSelector:
    matchNames:
      - kube-system
  selector:
    matchLabels:
      k8s-app: metrics-server-exporter
```
```
kubectl apply -f prometheus/metrics-server-exporter/
```

If you cannot see any data in prometheus, change 20-service-metrics-server-exporter.yaml to:
```
kubectl get service metrics-server-exporter -n kube-system -o yaml
```
```
apiVersion: v1
kind: Service
metadata:
  annotations:
    cloud.google.com/neg: '{"ingress":true}'
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"v1","kind":"Service","metadata":{"annotations":{"prometheus.io/path":"/metrics","prometheus.io/port":"8000","prometheus.io/scrape":"true"},"labels":{"k8s-app":"metrics-server-exporter"},"name":"metrics-server-exporter","namespace":"kube-system"},"spec":{"ports":[{"port":9104,"protocol":"TCP","targetPort":8000}],"selector":{"k8s-app":"metrics-server-exporter"}}}
    prometheus.io/path: /metrics
    prometheus.io/port: "8000"
    prometheus.io/scrape: "true"
  creationTimestamp: "2022-02-26T10:31:26Z"
  labels:
    k8s-app: metrics-server-exporter
  name: metrics-server-exporter
  namespace: kube-system
  resourceVersion: "4270441"
  uid: 13c39822-4dc6-44bf-a060-0dfba9769b25
spec:
  clusterIP: 10.60.4.190
  clusterIPs:
  - 10.60.4.190
  ipFamilies:
  - IPv4
  ipFamilyPolicy: SingleStack
  ports:
  - name: metrics
    port: 8000
    protocol: TCP
    targetPort: 8000
  selector:
    k8s-app: metrics-server-exporter
  sessionAffinity: None
  type: ClusterIP
status:
  loadBalancer: {}
```
```
kubectl apply -f service metrics-server-exporter -n kube-system -o yaml
```

6) Install prometheus-flask-exporter:
```
pip install prometheus-flask-exporter
```
7) Create a service monitor to eche service, for example:
```
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: service-a
  namespace: default
spec:
  endpoints:
    - interval: 30s
      port: metrics
  namespaceSelector:
    matchNames:
      - default
  selector:
    matchLabels:
      app: service-a
```
And change the port name in service a to metrics.

8) Add to app.py the code necessary, examples can be found here: https://github.com/rycus86/prometheus_flask_exporter
9) Run:
```
cd k8s make build
```
```
cd k8s make deploy-services
```
```
kubectl apply -f prometheus/service-monitors-exporter/
```
11) Export the ip for prometheus:
```
export SERVICE_IP=$(kubectl get svc --namespace monitoring monitoring-kube-prometheus-prometheus --template "{{ range (index .status.loadBalancer.ingress 0) }}{{ . }}{{ end }}")
```
8) Get prometheus url:
```
echo "Prometheus URL: http://$SERVICE_IP:9090/"
```

9) Install Istio: https://github.com/HadarPur/RU-K8S-FinalProject/tree/master/promethues/istio

