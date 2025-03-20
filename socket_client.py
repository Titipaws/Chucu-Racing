import socket
import json
import zlib

SERVER_IP = "localhost"
PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    ignition_time = input("Tiempo de ignición (ms): ")
    boost_pressure = input("Boost pressure (psi): ")
    afr = input("AFR (Relación aire-combustible): ")
    final_time = input("Tiempo final del carro (segundos): ")

    data = {
        "Ignition Time": ignition_time,
        "Boost Pressure": boost_pressure,
        "AFR": afr,
        "Final Time": final_time
    }
    #para reducir el tama;o y comprimir el mensaje.
    json_data = json.dumps(data, separators=(",", ":"))
    compressed_data = zlib.compress(json_data.encode("utf-8"))
    #envio de datos al servidor

    client_socket.sendto(compressed_data, (SERVER_IP, PORT))
    print("Datos enviados al servidor.")

    received_compressed_data, addr = client_socket.recvfrom(4096)
    received_json = zlib.decompress(received_compressed_data).decode("utf-8")
    received_data = json.loads(received_json)
    #recibe los datos del servidor y los imprime en pantalla
    
    print("Broadcast recibido:")
    if "datos" in received_data:
        print("Datos enviados:", received_data["datos"])
    if "analisis" in received_data:
        print("Análisis de los datos:", received_data["analisis"])
