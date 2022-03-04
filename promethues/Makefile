
##############################################
#
#
#
#               >>>>>>>
#             /         
#            /
########### /  
# Monitors # 
########### \ 
#         
#
#
#
#
##############################################
cleanup-services: delete-services

deploy-services:
	kubectl apply -f prometheus-flask-exporter/service-monitors-exporter/
	kubectl apply -f metrics-server-exporter/

delete-services:
	kubectl delete -f prometheus-flask-exporter/service-monitors-exporter/
	kubectl delete -f metrics-server-exporter/

