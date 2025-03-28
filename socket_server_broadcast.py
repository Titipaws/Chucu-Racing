import socket
import json
import time

def analyze_data(data_list):
    """
    Función de análisis que calcula promedios y emite un comentario 
    basado en el valor promedio de AFR.
    """
    try:
        num_entries = len(data_list)
        avg_ignition = sum(float(d["Ignition Time"]) for d in data_list) / num_entries
        avg_boost = sum(float(d["Boost Pressure"]) for d in data_list) / num_entries
        avg_afr = sum(float(d["AFR"]) for d in data_list) / num_entries
        avg_final = sum(float(d["Final Time"]) for d in data_list) / num_entries
        
        # Comentario simple para AFR (valor teórico: 14.7 es normal)
        if avg_afr < 14.7:
            afr_comment = "Mezcla rica"
        elif avg_afr > 14.7:
            afr_comment = "Mezcla pobre"
        else:
            afr_comment = "AFR normal"
        
        return {
            "Promedio Tiempo de Ignición": avg_ignition,
            "Promedio Boost Pressure": avg_boost,
            "Promedio AFR": avg_afr,
            "Promedio Tiempo Final": avg_final,
            "Comentario AFR": afr_comment
        }
    except Exception as e:
        return {"error": "No se pudo realizar el análisis", "detalle": str(e)}

# Configuración del servidor
HOST = "127.0.0.1"
PORT = 12345
BROADCAST_IP = "255.255.255.255"
BUFFER_SIZE = 4096

# Crear un socket UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Asignar el socket a la dirección y puerto especificados
server_socket.bind((HOST, PORT))

# Habilitar el modo de broadcast en el socket
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

print(f"Servidor en espera de datos en {HOST}:{PORT}...")

data_storage = []  # Lista para almacenar todos los mensajes recibidos

while True:
    # Recibe datos de algún cliente (máximo BUFFER_SIZE bytes)
    data, addr = server_socket.recvfrom(BUFFER_SIZE)
    
    try:
        # Decodificar los datos recibidos desde JSON
        data = json.loads(data.decode("utf-8"))
        
        data_storage.append(data)
        
        # Mostrar los datos recibidos en la consola del servidor
        print(f"Datos recibidos de {addr}: {data}")
               
        # Realizar el análisis AI de los datos acumulados
        analysis_result = analyze_data(data_storage)
        
        # Crear el mensaje de broadcast que incluye los datos y el análisis
        broadcast_message = {
            "datos": data,
            "analisis": analysis_result
        }
   
        # Crear un nuevo socket para enviar los datos en modo broadcast
        broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   
        # Habilitar el modo broadcast en el socket de transmisión
        broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        # Enviar los datos a todos los dispositivos en la red (broadcast)
        broadcast_socket.sendto(json.dumps(broadcast_message).encode("utf-8"), (BROADCAST_IP, PORT))
        
        # Cerrar el socket de transmisión
        broadcast_socket.close()

        print(f"Datos transmitidos en broadcast: {broadcast_message}")   
        
    except Exception as e:
        print(f"Error al procesar los datos: {e}")
    
    # Se reduce la espera para permitir procesamiento continuo
    time.sleep(100)
