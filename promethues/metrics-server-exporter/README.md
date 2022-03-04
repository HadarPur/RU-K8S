# Metrics server exporter Integration
## Install metrics-server-exporter:
```
kubectl apply -f https://raw.githubusercontent.com/olxbr/metrics-server-exporter/master/deploy/00-permissions-metrics-server-exporter.yaml -n kube-system
```
```
kubectl apply -f https://raw.githubusercontent.com/olxbr/metrics-server-exporter/master/deploy/10-deployment-metrics-server-exporter.yaml -n kube-system
```
```
kubectl apply -f https://raw.githubusercontent.com/olxbr/metrics-server-exporter/master/deploy/20-service-metrics-server-exporter.yaml -n kube-system
```

Created a metrics-server.yaml:
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
