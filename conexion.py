import socket #Importamos la clase socket de python para poder conectarnos a un servidor
import pickle #Clase pickle que permite enviar objetos y recibir objetos de un servidor


class Network: #Clase red
    def __init__(self):
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Necesitamos un cliente que se conecta gracias a los socket al servidor
        self.servidor = "192.168.0.16" #Aqui va el servidor local de tu casa o global al que te quieres unir para jugar en paralelo
        self.puerto = 5555 #Este puerto casi siempre esta disponible, y es muy utilizado en creacion de videojuegos
        self.addr = (self.servidor, self.puerto) #una direccion que contiene dos variables
        self.p = self.connect() #p representa el metodo de conectar al servidor

    def getP(self): #obtener la conexion
        return self.p

    def connect(self): #define conectar
        try:
            self.cliente.connect(self.addr) #conectamos un cliente a una direccion que contiene el servidor y su puerto
            return self.cliente.recv(2048).decode() #estamos constantemente decodificando bits que nos envia el servidor, 2048 es la cantidad de informacion que se envia
        except:
            pass

    def send(self, data): #se envian datos
        try:
            self.cliente.send(str.encode(data)) #codificamos la informacion que le vamos a mandar al servidor, al hacer clicks y demas
            return pickle.loads(self.cliente.recv(2048 * 2))
        except socket.error as e:
            print(e)
