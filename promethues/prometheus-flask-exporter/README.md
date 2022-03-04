# Prometheus flask exporter Integration

## Install prometheus-flask-exporter:

```
pip install prometheus-flask-exporter
```

Create a service monitor to eche service, for example:
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

## App.py
Add to app.py the code necessary, examples can be found here: https://github.com/rycus86/prometheus_flask_exporter

Run:
```
cd k8s make build
```
```
cd k8s make deploy-services
```
```
kubectl apply -f prometheus/service-monitors-exporter/
```
