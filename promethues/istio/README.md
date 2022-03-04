# Istio integration

## Install Istio:
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
