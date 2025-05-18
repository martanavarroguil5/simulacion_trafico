from recursos import traffic_lanes, train_tracks, runway, event_log
from vehicle import Vehicle
import time
import os
import threading
import tkinter as tk
import random

# Crea una lista de vehículos con tipo y prioridad aleatorios
def create_vehicles(num=20):
    tipos = [
        ("Coche", traffic_lanes),
        ("Tren", train_tracks),
        ("Avión", runway)
    ]
    vehicles = []
    for i in range(num):
        tipo, recurso = random.choice(tipos)
        nombre = f"{tipo} {i+1}"
        prioridad = random.randint(1, 5)
        vehicles.append(Vehicle(nombre, recurso, priority=prioridad))
    return vehicles

# Actualiza la interfaz gráfica con el estado de los recursos
def update_gui(resource_labels):
    recursos = [traffic_lanes, train_tracks, runway]
    for i, res in enumerate(recursos):
        if res.current_vehicle:
            resource_labels[i]["text"] = f"{res.name}: OCUPADO por {res.current_vehicle.name}"
            resource_labels[i]["bg"] = "red"
        else:
            resource_labels[i]["text"] = f"{res.name}: LIBRE"
            resource_labels[i]["bg"] = "green"

# Función principal: lanza los hilos y la interfaz gráfica
def main():
    vehicles = create_vehicles(num=15)  # Cambia el número de vehículos aquí
    for vehicle in vehicles:
        vehicle.start()  # Inicia cada hilo de vehículo

    # Configura la ventana de Tkinter
    root = tk.Tk()
    root.title("Simulación de Recursos de Tráfico")
    resource_labels = []
    for res in [traffic_lanes, train_tracks, runway]:
        lbl = tk.Label(root, text=f"{res.name}: LIBRE", width=40, height=2, bg="green", font=("Arial", 14))
        lbl.pack(pady=5)
        resource_labels.append(lbl)
    status_label = tk.Label(root, text="Simulación en curso...", font=("Arial", 12))
    status_label.pack(pady=10)

    # Bucle que actualiza la GUI cada 200 ms
    def gui_update_loop():
        update_gui(resource_labels)
        if any(v.is_alive() for v in vehicles):
            root.after(200, gui_update_loop)
        else:
            update_gui(resource_labels)
            status_label["text"] = "Simulación finalizada."

    gui_update_loop()
    root.mainloop()  # Inicia el bucle principal de la interfaz

if __name__ == "__main__":
    main()
