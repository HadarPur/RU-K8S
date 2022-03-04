from ratelimit import limits, sleep_and_retry
from locust.runners import STATE_SPAWNING, STATE_RUNNING, STATE_CLEANUP
from locust import HttpUser, between, task
from kubernetes import client, config
import requests
import datetime
from dateutil.tz import tzutc
import time
from typing import List, Union
import logging
import gevent.monkey

from .attackerFlow import AttackerFlow
from .regularFlow import RegularFlow

gevent.monkey.patch_all()


class YoYo(object):
    def __init__(self, autoscalers: List[str],services:List[str]) -> None:
        self.authenticate()
        self.remote_ip = self.get_remote_ip()
        self.creates()
        self.autoscalers = autoscalers
        self.services = services
        self.start_time = datetime.datetime.now(tz=tzutc())
        self.query_hpa_api()
        self.response_time = self.get_response_time()

    def creates(self):
        class AttackUser(HttpUser):
            host = f"http://{self.remote_ip}"
            wait_time = between(1, 3)

            @task
            def my_task(self):
                a = {
                    "memory_params": {"duration_seconds": 0.2,"kb_count": 50},
                    "cpu_params": {"duration_seconds": 0.001,"load": 0.9}
                }
                self.client.post("/load", json=a)

        self.reg = RegularFlow(AttackUser, 4, 10)
        self.attack = AttackerFlow(AttackUser, 24, 1)

    def authenticate(self):
        config.load_kube_config()
        self.auto_scale_api = client.AutoscalingV1Api()
        self.cluster_api = client.CoreV1Api()

    def get_remote_ip(self) -> str:
        services = self.cluster_api.list_service_for_all_namespaces()
        for service in services.items:
            if service.metadata.name == 'service-a-svc':
                remote_ip = service.status.load_balancer.ingress[0].ip
                remote_port = service.spec.ports[0].port
                target = f'{remote_ip}:{remote_port}'
                logging.info(f'Found remote IP at {remote_ip}:{remote_port}')
                return target
        raise RuntimeError("Failed to find remote IP")

    def response_time_loop(self) -> None:
        self.response_time = self.get_response_time()

    def get_statuses(self) -> None:
        namespace = 'default'
        self.statuses = []
        for name in self.autoscalers: 
           api_response = self.auto_scale_api.read_namespaced_horizontal_pod_autoscaler(name, namespace, pretty=True)
           self.statuses.append(api_response.status)

    def wait_for_start(self):
        while any(status.current_cpu_utilization_percentage is None for status in self.statuses):
            time.sleep(1)
            logging.info('Waiting for CPU metrics to initialize')
            self.get_statuses()

    def query_hpa_api(self) -> None:
        self.get_statuses()
    
    def get_nodes_count(self):
        nodes_count = len(list(self.cluster_api.list_node().items))
        return nodes_count

    def get_active_pods_count(self) -> int:
        label_selector = f'app in ({",".join(self.services)})'
        all_pods = self.cluster_api.list_pod_for_all_namespaces(
            label_selector=label_selector).items
        return len([pod for pod in all_pods if pod.status.phase == 'Running'])

    def start(self) -> None:
        self.wait_for_start()

    def loop(self, w) -> None:
        # Probe test
        for index in range(1000000):
            self.inner_loop(index)
            self.response_time_loop()
            
            stats = self.get_stats()

            HEADERS = ['response_time', 'active_pods_count', 'cpu_load', 'current_power_of_attack']
            logging.info(dict(zip(HEADERS, stats)))

    @property
    def is_attacking(self) -> bool:
        return self.attack.env.runner.state in [STATE_SPAWNING, STATE_RUNNING, STATE_CLEANUP]

    def finish_attack(self) -> None:
        self.attack.stop()

    def service_count(self) -> int:
        return len(self.services)

    def inner_loop(self, index: int) -> float:
        response_time = self.get_response_time()
        try:
            self.query_hpa_api()
            active_pods_count = self.get_active_pods_count()
        except client.exceptions.ApiException:
            self.authenticate()
            self.query_hpa_api()
            active_pods_count = self.get_active_pods_count()
        # Checking
        if self.is_attacking:
            # Handle attack testing on cool down
            if (self.get_average_cpu_load() <= 76 and active_pods_count > 10):
                self.finish_attack()
        else:
            if active_pods_count == self.service_count() and index > 10:  # and index > 49:
                print("we are under attack!")
                self.attack.start()

        return response_time

    def get_last_scale_time(self) -> datetime.datetime:
        latest_scale_time = self.start_time
        for scale_time in (status.last_scale_time for status in self.statuses):
            if scale_time is not None and scale_time > latest_scale_time:
                latest_scale_time = scale_time
        return latest_scale_time

    def get_current_replicas(self) -> List[int]:
        return [status.current_replicas for status in self.statuses]

    def get_average_cpu_load(self) -> float:
        return sum(self.get_cpu_loads()) / self.service_count()
    
    def get_cpu_loads(self) -> List[float]:
        return [status.current_cpu_utilization_percentage for status in self.statuses]

    def get_stats(self) -> List[Union[int, float, str]]:
        stats = [
            min(round(self.response_time, 1), 5),
            ' '.join(map(str, self.get_current_replicas())),
            ' '.join(map(str, self.get_cpu_loads())),
            self.reg.count + (self.attack.count if self.is_attacking else 0)
        ]
        return stats

    def stop(self) -> None:
        self.attack.stop()
        self.reg.stop()

    def get_response_time(self) -> float:
        url = f'http://{self.remote_ip}/health'
        try:
            response_time = send_probe(url)
        except Exception as e:
            response_time = send_probe(url)
        return response_time

@sleep_and_retry
@limits(calls=1, period=1)
def send_probe(url: str) -> float:
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return 10
        return response.elapsed.total_seconds()
    except requests.ReadTimeout:
        return 10
