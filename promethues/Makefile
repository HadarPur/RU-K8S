
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

deploy-service-monitors:
	kubectl apply -f prometheus-flask-exporter/service-monitors-exporter/

delete-services-monitors:
	kubectl delete -f prometheus-flask-exporter/service-monitors-exporter/
