
#Importamos modulos de python, nativos o instalados, e importamos las clases que necesitamos de otros python file de nuestro proyecto
import socket
from _thread import *
import pickle
from juego import Game

#Nombre de nuestro servidor local o global, y eleccion de un puerto para realizar esta conexion
servidor = "192.168.0.16"
puerto = 5555
#Asignamos el metodo socket de conexion a una varibale, es muy util para reducir codigo
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((servidor, puerto)) #recibimos un servidor y puerto para conectar
except socket.error as e:
    str(e)

s.listen(2) #cuantas conexiones en paralelo se aceptan
print("Esperando conexion, Servidor iniciado") #mensaje de la consola al correr el servidor

connected = set() #metodo set
games = {} #arreglo de juegos, aqui iran todas las partidas en simultaneo que sean ejecutadas
contadorId = 0 #Contabiliza el id del jugador que corre la partida, para que cuando se desconecte pueda ser borrado de la partida


def threaded_client(conn, p, juegoId): #Utilizamos hilos para recibir una conexion con un id de juego
    global contadorId #variable global para contar ids
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            if juegoId in games: #si nuestro id de juegos esta en el arreglo de juegos en simultaneo, lo ejecuta
                game = games[juegoId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetMovs()
                    elif data != "get":
                        game.play(p, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Conexión pérdida") #mensaje en consola cuando un jugador decide dejar de jugar y cierra
    try:
        del games[juegoId]
        print("Cerrando partida", juegoId)
    except:
        pass
    contadorId -= 1
    conn.close()



while True:
    conn, addr = s.accept()
    print("Conectado a:", addr) #mensaje en consola cuando el jugador logra conectarse a un servidor e iniciar partida

    contadorId += 1
    p = 0
    gameId = (contadorId - 1) // 2
    if contadorId % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creando partida...")
    else:
        games[gameId].listo = True
        p = 1


    start_new_thread(threaded_client, (conn, p, gameId))
