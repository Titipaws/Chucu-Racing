import socket  # Biblioteca para manejar sockets
import json  # Biblioteca para manejar datos en formato JSON

SERVER_IP = "127.0.0.1"
PORT = 12345

# Crear un socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bucle infinito para enviar datos al servidor y recibir la respuesta
while True:
    # Solicitar datos al usuario
    ignition_time = input("Tiempo de ignición (ms): ")
    boost_pressure = input("Boost pressure (psi): ")
    afr = input("AFR (Relación aire-combustible): ")
    final_time = input("Tiempo final del carro (segundos): ")

    # Crear un diccionario con los datos ingresados
    data = {
        "Ignition Time": float(ignition_time),
        "Boost Pressure": float(boost_pressure),
        "AFR": float(afr),
        "Final Time": float(final_time)
    }

    # Enviar los datos al servidor en formato JSON codificado en bytes
    client_socket.sendto(json.dumps(data).encode("utf-8"), (SERVER_IP, PORT))
    print("Datos enviados al servidor.")

    # Recibir datos en broadcast desde el servidor
    data, _ = client_socket.recvfrom(4096)  # Esperar respuesta del servidor
    received_data = json.loads(data.decode("utf-8"))  # Decodificar JSON

    print("Broadcast recibido:")
    if "datos" in received_data:
        print("Datos enviados:", received_data["datos"])
    if "analisis" in received_data:
        print("Análisis de los datos:", received_data["analisis"])
        
    
