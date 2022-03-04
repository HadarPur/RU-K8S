
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
cleanup-services: delete-services-monitors

deploy-services:
	kubectl apply -f prometheus-flask-exporter/service-monitors-exporter/

delete-services:
	kubectl delete -f prometheus-flask-exporter/service-monitors-exporter/
