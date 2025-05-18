import threading
import random
import time
import queue

event_log = []  # Lista global para registrar eventos

class Resource:
    _counter = 0  # Contador de desempate global para la PriorityQueue

    def __init__(self, name):
        self.name = name
        self.lock = threading.Lock()
        self.waiting_queue = queue.PriorityQueue()  # (priority, time, counter, vehicle)
        self.current_vehicle = None
        self.status_lock = threading.Lock()

    def use(self, vehicle):
        with self.status_lock:
            self.current_vehicle = vehicle
            # %H:%M:%S es el formato de hora: Hora (00-23), Minuto (00-59), Segundo (00-59)
            # Ejemplo: 14:35:07
            event_log.append(f"{time.strftime('%H:%M:%S')} - {vehicle.name} (p{vehicle.priority}) está usando {self.name}")
        time.sleep(random.uniform(1, 3))  # Simula el tiempo que el vehículo usa el recurso
        with self.status_lock:
            event_log.append(f"{time.strftime('%H:%M:%S')} - {vehicle.name} ha terminado con {self.name}")
            self.current_vehicle = None
        # Mostrar que el recurso está libre antes de que lo ocupe el siguiente
        event_log.append(f"{time.strftime('%H:%M:%S')} - {self.name} está LIBRE")
        time.sleep(0.5)  # Breve pausa visual para que se vea el estado libre

    def acquire(self, vehicle):
        event_log.append(f"{time.strftime('%H:%M:%S')} - {vehicle.name} (p{vehicle.priority}) está esperando para usar {self.name}")
        entry_time = time.time()
        Resource._counter += 1
        self.waiting_queue.put((-vehicle.priority, entry_time, Resource._counter, vehicle))
        while True:
            with self.lock:
                if not self.waiting_queue.empty():
                    top_priority, top_time, top_counter, top_vehicle = self.waiting_queue.queue[0]
                    if top_vehicle == vehicle:
                        self.waiting_queue.get()
                        self.use(vehicle)
                        break
            time.sleep(0.05)

    def print_status(self):
        pass

# Crear recursos limitados
traffic_lanes = Resource("Carril de tráfico")
train_tracks = Resource("Vía de tren")
runway = Resource("Pista de aterrizaje")
