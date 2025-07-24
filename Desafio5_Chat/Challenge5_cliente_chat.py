import socket # permite crear conexiones de tcp ip 
import threading # permite ejecutar varias cosas al mismo tiempo en este caso leer y escribir sin que una bloquee a la otra

HOST = 'localhost'# te conecta a la misma computadora en donde corre el servidor
PUERTO = 8000 # este es el canal de comunicacion 

# cliente es una variable que contiene un objeto socket es una variable de tipo objeto, de la clase socket.socket
#ipv4 192.168.0.1
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
cliente.connect((HOST, PUERTO))
# conectate a un servidor host en el puerto ...

def recibir_mensajes():
    while True:
        try:
            mensaje = cliente.recv(1024).decode()
            if not mensaje:
                break
            print(f"\n🎵 {mensaje}")
        except:
            print("\n[⚠️] Conexión perdida con el servidor.")
            cliente.close()
            break

def enviar_mensajes():
    while True:
        try:
            mensaje = input()
            cliente.send(mensaje.encode())
        except:
            break
# hilo demonio, es decir, que se va a ejecutar en segundo plano y no bloquea el cierre del programa.
# creando un nuevo hilo de ejecucion 
threading.Thread(target=recibir_mensajes, daemon=True).start()
enviar_mensajes()
