import socket
import pickle
from configuracion import *


# codificado esta clase para que podamos reutilizar esta clase en el futuro
#  inicializando clientes
class Red:
    def __init__(self):
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor = DIRECCION_SERVIDOR
        self.puerto = PUERTO
        self.direccion = (self.servidor, self.puerto)
        self.jugador = self.conectar()

    def obtenerJugador(self):
        return self.jugador

    def conectar(self):
        try:
            self.cliente.connect(self.direccion)
            return int(self.cliente.recv(2048*8).decode())
        except:
            pass

    def enviar(self, data):
        try:
            self.cliente.send(pickle.dumps(data))
            return pickle.loads(self.cliente.recv(2048 * 8))
        except socket.error as e:
            str(e)

    def ping_server(self):
        return self.enviar('ping')