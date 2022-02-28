
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
	kubectl apply -f service-monitors-exporter/

delete-services-monitors:
	kubectl delete -f service-monitors-exporter/
