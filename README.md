# YoYo attack on Kubernetes Auto-Scale
Liam Tal, Oved Chitayat, Hadar Pur.

Submitted as final project for the Advanced Topics In IP Networks course, Reichman University, 2022

## Introduction
DDoS is an old attack pattern, and there are well-known solutions for protecting against DDoS attacks. However, in a cloud-native world, applications behave differently, and attackers are finding ways to exploit this behavior.

In this work, we will demonstrate the YoYo attack - a burst attack which deliberately targets auto scaling of VMs in cloud platforms.
This work is based on a research that was made in the Past by Mr. Ronen Ben David and ours truly Anat Bremler-Barr.
* We used gcp environment with k8s to build the clusters, nodes, podes and services from scratch, integrated with Istio as a victim.
* We used a VM with Ubuntu OS, based on Daniel’s attack to make sure we will continue that same work as an attacker.

To visualize the attack, we used Grafana with Prometheus queries.

## Auto scaling in Google Cloud Platform
### Google Cloud
Google Cloud Platform (GCP), offered by Google, is a suite of cloud computing services that runs on the same infrastructure that Google uses internally for its end-user products, such as Google Search, Gmail, Google Drive, and YouTube. Alongside a set of management tools, it provides a series of modular cloud services including computing, data storage, data analytics and machine learning.

### Auto scaling
Auto-scaling is a cloud computing service feature that automatically adds or removes compute resources depending upon actual usage. Each cloud solution comes with its own auto-scaling engine: Heat in Openstack, autoscaler in Google Cloud, Azure Autoscale in Microsoft Azure and auto-scaling in Amazon Elastic Compute Cloud (Amazon EC2). 

In each of these systems the underlying algorithm lets the cloud customer, referred to in our work as the user, to define a scaling criterion and the corresponding thresholds for overload and underload. 

### Auto scaling - GCP
Google cloud scaling is always adaptive. 
The user sets the target criterion value, e.g., target CPU utilization of 75%, and the autoscaler makes scaling decisions proportionally and maintains that level without the user having to set rules. 

It is assumed that Google uses a machine learning algorithm for the adaptive scaling.

## Let’s talk Kubernetes	
### What is Kubernetes?	
Kubernetes is a portable, extensible, open-source platform for managing containerized workloads and services, that facilitates both declarative configuration and automation. It has a large, rapidly growing ecosystem. Kubernetes services, support, and tools are widely available.

The name Kubernetes originates from Greek, meaning helmsman or pilot. K8s as an abbreviation results from counting the eight letters between the "K" and the "s".

### Why k8s?
Containers are a good way to bundle and run your applications. In a production environment, you need to manage the containers that run the applications and ensure that there is no downtime. For example, if a container goes down, another container needs to start. Wouldn't it be easier if this behavior was handled by a system?
That's how Kubernetes comes to the rescue! Kubernetes provides you with a framework to run distributed systems resiliently. It takes care of scaling and failover for your application, provides deployment patterns, and more. 

### Auto Scaling - K8S 
Kubernetes is designed for scalability, providing many features that enable applications and the host infrastructure to scale in and out. You can specify metrics that influence automated scaling (autoscaling) processes, including demand and efficiency.
Kubernetes supports the following autoscaling types:
* Vertical pod autoscaler (VPA) - automatically decreases or increases the resource limits on a certain pod.
* Horizontal pod autoscaler (HPA) - automatically decreases or increases the number of pod instances.
* Cluster autoscaler (CA) - automatically decreases or increases the number of nodes within a certain node pool according to pod scheduling.

## Istio
### What is Istio?
Istio is a service mesh—a modernized service networking layer that provides a transparent and language-independent way to flexibly and easily automate application network functions. It is a popular solution for managing the different microservices that make up a cloud-native application. 

Istio service mesh also supports how those microservices communicate and share data with one another.

## Chosen Topology
<p align="center">
  <img src="https://github.com/HadarPur/RU-K8S-FinalProject/blob/master/k8s/topology.png" alt="drawing" width="800"/>
</p>

## We’re under Attack
### DDoS Attacks
DDoS attack is when an attacker/s attempt to make it impossible for a service to be delivered.

This can be achieved by preventing access to virtually anything: servers, devices, services, networks, applications, and even specific transactions within applications. 

Generally, these attacks work by drowning a system with requests for data. This could be sending a web server so many requests to serve a page that it crashes under the demand, or it could be a database being hit with a high volume of queries. 

The result is that available internet bandwidth, CPU and RAM capacity becomes overwhelmed.

The impact could range from a minor annoyance from disrupted services to experiencing entire websites, applications, or even entire business taken offline.

### YoYo Attack
In the Yo-Yo attack the attacker oscillates between the on-attack phase and the off-attack phase. 
* In the on-attack phase, the attacker sends a burst of traffic that causes the auto-scaling mechanism to perform a scale up. 
* In the off-attack phase, the attacker stops sending the excess traffic. This second phase takes place when the attacker identifies that the scale up has occurred (all machines are up and the service is fully functional) and continues until the attacker determines that scale down has occurred. 

And so on.

## Experiments Results
### Experiments
For our research we knew that we should show only the istio experiment, but we thought that by adding the “before” results could be a value of comparison and shed some more light regarding this project.

Data:
* user count - which is Total number of users to start.
* spawn rate - which is the number of users to spawn per second.

### Experiment #1 without Istio
Starting from:
* 3 nodes
* 1 pod per service.


Regular flow contains user_count = 4 and spawn_rate = 10.

Attacker flow contains user_count = 24 and spawn_rate = 1.

### Results
#### CPU Utilization vs Response time (All services)
<p align="center">
  <img src="https://github.com/HadarPur/RU-K8S-FinalProject/blob/master/promethues/queries/experiment1-03-03-20-38-22-18/Screen%20Shot%202022-03-03%20at%2022.16.21.png" alt="drawing" width="800"/>
</p>

#### CPU Utilization vs Response time (Per service)
<p align="center">
  <img src="https://github.com/HadarPur/RU-K8S-FinalProject/blob/master/promethues/queries/experiment1-03-03-20-38-22-18/Screen%20Shot%202022-03-03%20at%2022.17.41.png" alt="drawing" width="800"/>
    <img src="https://github.com/HadarPur/RU-K8S-FinalProject/blob/master/promethues/queries/experiment1-03-03-20-38-22-18/Screen%20Shot%202022-03-03%20at%2022.17.56.png" alt="drawing" width="800"/>
</p>
<p align="center">
  <img src="https://github.com/HadarPur/RU-K8S-FinalProject/blob/master/promethues/queries/experiment1-03-03-20-38-22-18/Screen%20Shot%202022-03-03%20at%2022.18.17.png" alt="drawing" width="800"/>
    <img src="https://github.com/HadarPur/RU-K8S-FinalProject/blob/master/promethues/queries/experiment1-03-03-20-38-22-18/Screen%20Shot%202022-03-03%20at%2022.18.33.png" alt="drawing" width="800"/>
</p>

#### Pods vs Nodes
<p align="center">
  <img src="https://github.com/HadarPur/RU-K8S-FinalProject/blob/master/promethues/queries/experiment1-03-03-20-38-22-18/Screen%20Shot%202022-03-03%20at%2022.16.51.png" alt="drawing" width="800"/>
</p>

#### Power vs time
<p align="center">
  <img src="https://github.com/HadarPur/RU-K8S-FinalProject/blob/master/promethues/queries/experiment1-03-03-20-38-22-18/Screen%20Shot%202022-03-03%20at%2022.17.15.png" alt="drawing" width="800"/>
</p>

### Experiment #2 with Istio
### Results

## Conclusions and Future work
### Conclusions
### Future work
* First of all we can try and test our experiment on different clouds, in the original article it is AWS based, while ours is GCP based so we can recommend our next subject of experiment to be tested on Azure.
* Second, would be optimizing the attack - whether by trying to find the best hyperparameters, or maybe even by reconstructing the attack from scratch with new futuristic technologies.
* Lastly, we would recommend on a better distribution of the load-forwarding to a smarter one and by doing it we could test the efficiency and correctness of this attack.


## Bibliography
* https://kubernetes.io
* DDoS attack on cloud auto-scaling mechanisms - https://ieeexplore.ieee.org/abstract/document/8057010?casa_token=GaTR6Nr4W2EAAAAA:EjkVSELqh43O2MxwAy-3AYaZmqIoee-oVzjcVOCgD9ut29K1bd5WMFD7c-LO4ZtPKAmoiLRkcn2_
* https://hakin9.org/kubernetes-ddos-dangers-of-k8s-auto-scaling/ 
* Kubernetes Auto-Scaling: YoYo attack vulnerability and mitigation - https://arxiv.org/abs/2105.00542
* https://cloud.google.com/
* Sample project of DDoS attack on Kubernetes - https://github.com/danibachar/Kubernetes
* Scripts, Makefile, AAPI explanation and Deployments YAMLs ready to use - https://github.com/danibachar/kube-multi-cluster-managment/tree/main/koss-application-testing
* https://prometheus.io/docs/prometheus/latest/getting_started/
* https://github.com/olxbr/metrics-server-exporter
* https://github.com/rycus86/prometheus_flask_exporter

