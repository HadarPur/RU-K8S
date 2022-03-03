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

9) Install Istio:
```
curl -L https://istio.io/downloadIstio | sh -
```
Run ```istioctl``` command and see if the command works, if not go to the documentation to export the command: https://istio.io/latest/docs/setup/getting-started/#download

Run
```
kubectl
```
You should see:
```
NAME              		STATUS   	  AGE
default           		Active   		13d
kube-node-lease  		  Active   		13d
kube-public       		Active   		13d
kube-system       		Active   		13d
monitoring        		Active   		8d
```

Run 
```
istioctl install
```

Run ```kubectl get ns``` again and you should see istio-system:
```
NAME              		STATUS   	AGE
default           		Active   		13d
istio-system      		Active  		92s
kube-node-lease  		  Active   		13d
kube-public       		Active   		13d
kube-system       		Active   		13d
monitoring        		Active   		8d
```

Run ```kubectl get pod -n istio-system``` to see the active pods:
```
NAME                                    					READY   	STATUS    RESTARTS      AGE
istio-ingressgateway-7997ddf9d8-tn5zz  	          1/1     	Running   	0          	87s
istiod-6cf87bf5d-xcx9s                 			      1/1    	  Running   	0          	104s
```

Run:
```
cd k8s
```
```
make build
```
```
make deploy-services
```
```
kubectl label namespace default istio-injection=enabled
```
```
make cleanup-services
```
```
make build
```
```
make deploy-services
```

Run:
```
kubectl get pod
```
Wait for all the pods to be at status running with 2/2:

```
NAME                                      READY   STATUS    RESTARTS   AGE
grafana-agent-755b69744d-qwl4w            1/1     Running   0          10h
ksm-kube-state-metrics-7d8f59c464-wpsxn   1/1     Running   0          10h
service-a-688867984-7lxzw                 2/2     Running   0          114s
service-b-6b45f7df6d-qlt5k                2/2     Running   0          112s
service-c-79bc6557dd-wntvj                2/2     Running   0          111s
service-d-757c6b7dd4-6qlsf                2/2     Running   0          110s
```
