import requests
import datetime
import time
import logging
import gevent.monkey
from ratelimit import limits, sleep_and_retry
from locust.runners import STATE_SPAWNING, STATE_RUNNING, STATE_CLEANUP
from locust import HttpUser, between, task
from kubernetes import client, config
from dateutil.tz import tzutc
from typing import List
from attacker import Attacker

gevent.monkey.patch_all()


class YoYo(object):
    def __init__(self, autoscalers: List[str], services: List[str]):
        self.autoscaling_status = None
        self.attack_on = None
        self.attack_off = None

        self.auto_scale_api = None
        self.cluster_api = None

        self.auth()
        self.remote_ip = self.get_remote_ip()
        self.create_attackers()
        self.autoscalers = autoscalers
        self.services = services
        self.start_time = datetime.datetime.now(tz=tzutc())
        self.get_autoscaling_status()
        self.response_time = self.get_response_time()

    def auth(self):
        config.load_kube_config()
        self.auto_scale_api = client.AutoscalingV1Api()
        self.cluster_api = client.CoreV1Api()

    def start(self):
        while any(status.current_cpu_utilization_percentage is None for status in self.autoscaling_status):
            time.sleep(1)
            logging.info('Waiting for CPU metrics to initialize')
            self.get_autoscaling_status()

        self.loop()

    def loop(self):
        for index in range(1000000):
            try:
                self.get_autoscaling_status()
                active_pods_count = self.get_active_pods_count()
            except client.exceptions.ApiException:
                self.auth()
                self.get_autoscaling_status()
                active_pods_count = self.get_active_pods_count()
            if self.is_attacking:
                if self.get_average_cpu() <= 76 and active_pods_count > 10:
                    self.attack_on.stop()
            else:
                if active_pods_count == len(self.services) and index > 10:
                    print("we are under attack!")
                    self.attack_on.start()

            self.response_time = self.get_response_time()
            self.log_cluster_status()

    @property
    def is_attacking(self):
        return self.attack_on.environment.runner.state in [STATE_SPAWNING, STATE_RUNNING, STATE_CLEANUP]

    def get_remote_ip(self):
        services = self.cluster_api.list_service_for_all_namespaces()
        for service in services.items:
            if service.metadata.name == 'service-a-svc':
                remote_ip = service.status.load_balancer.ingress[0].ip
                remote_port = service.spec.ports[0].port
                target = f'{remote_ip}:{remote_port}'
                logging.info(f'Found remote IP at {remote_ip}:{remote_port}')
                return target
        raise RuntimeError("Failed to find remote IP")

    def get_autoscaling_status(self):
        namespace = 'default'
        self.autoscaling_status = []
        for name in self.autoscalers:
            api_response = self.auto_scale_api.read_namespaced_horizontal_pod_autoscaler(name, namespace, pretty=True)
            self.autoscaling_status.append(api_response.status)

    def get_nodes_count(self):
        nodes_count = len(list(self.cluster_api.list_node().items))
        return nodes_count

    def get_active_pods_count(self):
        label_selector = f'app in ({",".join(self.services)})'
        all_pods = self.cluster_api.list_pod_for_all_namespaces(label_selector=label_selector).items
        return len([pod for pod in all_pods if pod.status.phase == 'Running'])

    def get_last_scale_time(self):
        latest_scale_time = self.start_time
        for scale_time in (status.last_scale_time for status in self.autoscaling_status):
            if scale_time is not None and scale_time > latest_scale_time:
                latest_scale_time = scale_time
        return latest_scale_time

    def get_current_replicas(self):
        return [status.current_replicas for status in self.autoscaling_status]

    def get_average_cpu(self):
        return sum(self.get_cpu_loads()) / len(self.services)

    def get_cpu_loads(self):
        return [status.current_cpu_utilization_percentage for status in self.autoscaling_status]

    def get_response_time(self):
        url = f'http://{self.remote_ip}/health'
        try:
            response_time = send_probe(url)
        except Exception as e:
            response_time = send_probe(url)
        return response_time

    def log_cluster_status(self):
        stats = {
            'response_time': min(round(self.response_time, 1), 5),
            'active_pods_count': ' '.join(map(str, self.get_current_replicas())),
            'cpu_load': ' '.join(map(str, self.get_cpu_loads())),
            'power': self.attack_off.count + (self.attack_on.count if self.is_attacking else 0)
        }

        logging.info(stats)

    def create_attackers(self):
        class AttackUser(HttpUser):
            host = f"http://{self.remote_ip}"
            wait_time = between(1, 3)

            @task
            def my_task(self):
                body = {
                    "memory_params": {"duration_seconds": 0.2, "kb_count": 50},
                    "cpu_params": {"duration_seconds": 0.001, "load": 0.9}
                }
                self.client.post("/load", json=body)

        self.attack_off = Attacker(AttackUser, 4, 10)
        self.attack_on = Attacker(AttackUser, 24, 1)

@sleep_and_retry
@limits(calls=1, period=1)
def send_probe(url: str):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return 10
        return response.elapsed.total_seconds()
    except requests.ReadTimeout:
        return 10
