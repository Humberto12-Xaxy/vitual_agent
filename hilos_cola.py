import threading
import queue

# Crear una cola compartida
shared_queue = queue.Queue()

# Función para el primer hilo
def producer_thread():
    for i in range(5):
        shared_queue.put(i)  # Coloca elementos en la cola
        print(f"Productor: {i}")

# Función para el segundo hilo
def consumer_thread():
    while True:
        data = shared_queue.get()  # Obtiene elementos de la cola
        if data is None:
            break
        print(f"Consumidor: {data}")

# Crear los hilos
producer = threading.Thread(target=producer_thread)
consumer = threading.Thread(target=consumer_thread)

# Iniciar los hilos
producer.start()
consumer.start()

# Esperar a que los hilos terminen
producer.join()

# Indicar al consumidor que termine cuando no haya más elementos
shared_queue.put(None)
consumer.join()

print("Finalizado")



