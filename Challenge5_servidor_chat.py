import socket
import select

HOST = 'localhost' # 127.0.0.1
PUERTO = 8000 # para desarrollo local aunque es conocido como puerto utilizado por malware, podria utilizarse el piuerto 8000

# socket afinet sirve para conexiones IPV4 como puertos de 192.168.0.1  y el socket sock stream indica conexion de protocolo tipo TCP 
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# af inet capa internet investigar y socksteream app inves
# configura la opcion interna del socket, sol socket nivel donde se aplica la opcion a nivel de socket no del protoclo, en el servidor para reutilizar el host y puerto 
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

servidor.bind((HOST, PUERTO))
# asigna el socket a una direccion y puerto especifico es basicamente decir que este socket va a recibir conexiones localhost:12345
servidor.listen()
# basicamente le dice al sistema, estoy listo para recibir conexiones, empieza a escuchar modo servidor pasivo, pero aun no acepta ninguna conexion


print(f"[🎧] Servidor escuchando en {HOST}:{PUERTO}")


clientes = [servidor]

while True:
    try:
        # select.select basicamente le pregunta al sistema cuando un socket este listo para hacer algo
        sockets_listos, _, excepciones = select.select(clientes, [], clientes)

        for sock in sockets_listos:
            if sock == servidor:
                cliente_socket, direccion = servidor.accept()
                 # acepts acepta la conexion y se crea un nuevo socket exclusivo para este cliente (cliente socket) y se guarda su direccion IP en la variable direccion
      
                clientes.append(cliente_socket)
                print(f"[+] Nuevo cliente conectado desde {direccion}")
            else:
                try:
                    mensaje = sock.recv(1024).decode()
                    # recibe datos binarios de tipo bytes desde el socket y lo decodifica a string 
                    if not mensaje:
                        raise Exception("Cliente desconectado")
                    print(f"[SMS] Mensaje recibido: {mensaje}")
                    for c in clientes:
                        if c != servidor and c != sock:
                            c.send(mensaje.encode())
                            # porque los sockets solo pueden enviar bytes y los convierte a string
                except Exception:
                    print("[!] Cliente desconectado")
                    clientes.remove(sock)
                    sock.close()

        for sock in excepciones:
            clientes.remove(sock)
            sock.close()
           
            
    except KeyboardInterrupt:
        print("\n[🔚] Servidor apagado por el usuario.")
        break
  