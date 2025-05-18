import threading
from recursos import traffic_lanes, train_tracks, runway

class Vehicle(threading.Thread):
    def __init__(self, name, resource, priority=1):
        threading.Thread.__init__(self)
        self.name = name
        self.resource = resource
        self.priority = priority

    def run(self):
        # El vehículo intentará usar el recurso
        self.resource.acquire(self)
        # Visualización en tiempo real tras usar el recurso
        self.resource.print_status()
