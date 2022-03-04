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
