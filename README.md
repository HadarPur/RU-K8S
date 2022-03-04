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

## Chosen Topology:
<p align="center">
  <img src="https://github.com/HadarPur/RU-K8S-FinalProject/blob/master/k8s/topology.png" alt="drawing" width="700"/>
</p>
