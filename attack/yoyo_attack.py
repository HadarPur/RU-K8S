import pyfiglet
from locust.log import setup_logging
from yoyo import YoYo

title = pyfiglet.figlet_format("DDOS YoYo Attack", font="bulbhead")

TARGET_AUTOSCALERS = ['service-a-autoscaler','service-b-autoscaler','service-c-autoscaler','service-d-autoscaler']
TARGET_SERVICES = ['service-a','service-b','service-c','service-d']

if __name__ == '__main__':
    print(title)
    setup_logging("INFO", None)
    yoyo = YoYo(TARGET_AUTOSCALERS, TARGET_SERVICES)
    yoyo.start()
