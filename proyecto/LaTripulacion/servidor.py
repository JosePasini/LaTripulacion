import socket
from _thread import *
import pickle

from juego import Juego
from configuracion import *


# Este es el script del servidor, tiene que estar siempre en ejecución, pero necesitamos primero ejecutar el servidor.
# Deberíamos intentar conectar clientes al servidor
# esto es para el IPV4 direccion socket.AF_INET el del tipo que todos usaremos y SOCK_STREAM es como el String del server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Hacemos un try /  catch para intentar entrar al server, y evitar la interrupcion del codigo en tiempo de ejecucion
try:
    s.bind((DIRECCION_SERVIDOR, PUERTO))  # enlazar la dirección IP (servidor) a este puerto dado
except socket.error as e:
    str(e)

# el parámetro es el número de clientes habilitados para conectarse al servidor
s.listen(3)
print("Esperando para comenzar, Servidor iniciado")

juego = Juego(0)

# definiendo una funcion con hilos
def threaded_client(conn, jugador):
    # Enviando un mensaje al cliente que contenta el número de player
    global juego
    conn.send(str.encode(str(jugador)))

    while True:
        try:
            # metemos 2048 bits, la cantidad que necesitamos
            data = pickle.loads(conn.recv(2048))
            """ 
            Necesitamos decodificar la información recibida, ya que está codificada en un sistema cliente-servidor
            el formato trabajado es utf8
            reply = data.decode("utf-8")
            """
            if not data:
                print("Desconectado del servidor")
                break
            else:
                if data == 'ping':
                    reply = juego
                else:
                    juego.agregar_carta(data)
                    if juego.fin_ronda:
                        print('PERDISTE LA MISIÓN, REINTENTALO. ¡TÚ PUEDES!')
                        juego = Juego(juego.mision)
                    if juego.fin_ronda_mision:
                        print(f"FIN MISIÓN {juego.mision + 1}, FELICITACIONES, AHORA PASAREMOS A LA SIGUIENTE MISIÓN.")
                        juego = Juego(juego.mision + 1)

                    reply = juego

                    print(f'La baza actual es: {juego.baza_actual}')
            # Esto es solo para codificarlo en un objeto de bites
            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Conexión perdida")
    conn.close()


jugador_actual = 0
while True:
    conexion, direccion = s.accept() #acepta la conexion y la almacena junto a la direccion
    print("Conectado a: ", direccion)
    # Un hilo es otro proceso que se ejecuta en segundo plano
    # no queremos finalizar el threadded_client anterior cuando ejecutamos otro
    # queremos que threadded_client se ejecute en segundo plano
    start_new_thread(threaded_client, (conexion, jugador_actual))
    jugador_actual += 1