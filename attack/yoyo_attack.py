import numpy as np
import os
import logging
import pyfiglet
  
title = pyfiglet.figlet_format("DDOS YoYo Attack", font = "digital" )

TARGET_AUTOSCALERS = ['service-a-autoscaler','service-b-autoscaler','service-c-autoscaler','service-d-autoscaler']
TARGET_SERVICES = ['service-a','service-b','service-c','service-d']

if __name__ == '__main__':
    setup_logging("INFO", None)
    yoyo = YoYo(TARGET_AUTOSCALERS, TARGET_SERVICES)
    print(title)
    yoyo.start()
