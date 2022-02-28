
##############################################
#
#
#
#               >>>>>>>
#             /         
#            /
########### /  
# Services # 
########### \ 
#         
#
#
#
#
##############################################
cleanup-services: delete-services

build:
	docker build --no-cache -f Dockerfile -t gcr.io/k8s-fb/k8s-fb/app:latest .
	docker push gcr.io/k8s-fb/k8s-fb/app:latest

deploy-services:
	kubectl apply -f service-a/
	kubectl apply -f service-b/
	kubectl apply -f service-c/
	kubectl apply -f service-d/

delete-services:
	kubectl delete -f service-a/
	kubectl delete -f service-b/
	kubectl delete -f service-c/
	kubectl delete -f service-d/
