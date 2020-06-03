#Importamos los modulos de pygame y pickle. Pickle viene por default en el lenguaje python, y pygame se instala
# escribiendo el siguiente comando: "pip install pygame" en windows-simbolo del sistema- digitas el comando y presionas enter

# El modulo pickle nos permite enviar y recibir objetos del servidor

import pygame
from conexion import Network #Llamamos una clase que esta presente en un python file, usando el formato: from( python file) import (que clase)
import pickle
pygame.font.init() #inicializamos el paquete de fuentes de escritura disponible en el modulo pygame

width = 700 #Definimos la variable ancho
height = 700 #Definimos la variable alto
ventana = pygame.display.set_mode((width, height)) #Creamos una ventana en python usando las herramientas del modulo pygame (lo equivalente a un frame en java)
pygame.display.set_caption("PIEDRAS, PAPEL O TIJERA || INTERFAZ DE USUARIO") #Le ponemos un titulo a nuestra ventana en la parte superior#


class Boton: #Creamos la clase botón
    def __init__(self, text, x, y, color): #Definimos los parametros de mi boton, tendrá un texto, una ubicacion x, y , y un color  de fondo
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150  #Asignamos el tamaño de los botones
        self.height = 100

    def pintar(self, win):  #Definimos un metodo pintar(dibujar) que tiene como parametro la ventana del juego
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height)) #Dibujamos un rectangulo dentro de ese frame que creamos
        font = pygame.font.SysFont("comicsans", 40)  #A la variable font le asignamos el estilo de letra comic sans de tamaño 40, para crear despues titulos y textos
        text = font.render(self.text, 1, (255,255,255)) #A la variable texto le asignamos color, en python los colores se establecen dentro de parentesis y separados por coma
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2))) #Nos aseguramos de que quede centrado

    def click(self, pos): #El juego funciona haciendo click en botones ó opciones de respuesta, necesitamos un metodo click que reciba una posicion
        x1 = pos[0]  #Jugador o cliente 1, es decir el que corre primero el juego
        y1 = pos[1]  #Jugador o cliente 2, es decir el que corre despues el juego
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height: #Chequea si la coordenada que vamos a pasar, la cual sera una tupla
            # de valores x,y (acerca de la posicion de nuestro mouse); está en el botón, esto lo hacemos yendo a la x, mirando si es mayor que ese valor de x, si es menor
            # que la x + ancho (en medio de una caja pequeña), con la Y hacemos lo mismo pero chequeamos verticalmente si esta en la caja. Son soluciones a problemas de colisiones...
            return True
        else:
            return False


def repintarVentana(win, game, p): #Metodo repintar ventana que recibe la ventana,una variable juego, un jugador p (de player)
    win.fill((128,128,128)) #Metodo fill llena la ventana de color

    if not(game.conectado()): #Si no ha habido una conexión..
        font = pygame.font.SysFont("comicsans", 80) #Se genera la fuente comic sans de tamaño X
        text = font.render("Esperando oponente...", 1, (255,0,0), True) #Escribimos el texto que se ve en pantalla mientras no haya conexión del otro jugador
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2)) #Ubica ese texto en el centro
    else:
        font = pygame.font.SysFont("comicsans", 60) #Si por el contrario hubo conexión, creo la fuente x de tamaño x
        text = font.render("TÚ", 1, (0, 255,255))  #Asigno una especie de titulo a cada jugador
        win.blit(text, (80, 200))  #Ubicacion

        text = font.render("OPONENTE", 1, (0, 255, 255))  #Asigno una especie de titulo a cada jugador
        win.blit(text, (380, 200)) #Ubicacion

        move1 = game.get_mov_jugador(0) #Definimos los movimientos de cada jugador
        move2 = game.get_mov_jugador(1) #Definimos los movimientos de cada jugador
        if game.ambosMovieron(): # Si ambos jugadores se movieron
            text1 = font.render(move1, 1, (0,0,0))
            text2 = font.render(move2, 1, (0, 0, 0)) #Actualiza el texto y su color
        else:
            if game.Jug1Movs and p == 0: #Si el jugador 1 se movió
                text1 = font.render(move1, 1, (0,0,0)) #Actualiza posicion del texto y color
            elif game.Jug1Movs:  #para saber que significa elif ... https://www.mclibre.org/consultar/python/lecciones/python-if-else.html
                text1 = font.render("Elegido", 1, (0, 0, 0)) #Actualiza lo que dice el texto del jugador 1 cuando hace una elección
            else:
                text1 = font.render("Esperando...", 1, (0, 0, 0)) #Esperando que el jugador oponente haga su elección

            if game.Jug2Movs and p == 1:
                text2 = font.render(move2, 1, (0,0,0))
            elif game.Jug2Movs:
                text2 = font.render("Elegido", 1, (0, 0, 0))
            else:
                text2 = font.render("Esperando...", 1, (0, 0, 0))

        if p == 1:  #Si el player ó jugador es el oponente...
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))

        for btn in btns: #recorremos una lista de botones y dibujamos en la ventana
            btn.pintar(win)

    pygame.display.update() #Actualizamos


btns = [Boton("Roca", 50, 500, (0, 0, 0)), Boton("Tijeras", 250, 500, (255, 0, 0)), Boton("Papel", 450, 500, (0, 255, 0))]  #Lista de botones con sus respectivos atributos
def main():
    run = True
    clock = pygame.time.Clock()  #Un reloj interno de ejecución
    n = Network() # n equivale a la clase network que esta en el python file conexion
    player = int(n.getP()) #player recibe la posicion del jugador con getp en forma de entero
    print("Eres el jugador", player) #En consola muestra tu numero de jugador

    while run:
        clock.tick(60)
        try:
            game = n.send("get")  # Enviamos información al servidor constantemente
        except:
            run = False
            print("No se obtuvo partida") #Si no se recibe la información por algun motivo, en consola se escribe
            break

        if game.ambosMovieron(): #metodo para actualizar que pasa si ambos jugadores eligen
            repintarVentana(ventana, game, player)
            pygame.time.delay(500) #Cuanto tiempo esperamos luego de que termina la partida
            try:
                game = n.send("reset") #Que hacer despues que termina la partida, reinicia una nueva
            except:
                run = False
                print("No se obtuvo partida") #En consola si hubo algun error
                break

            font = pygame.font.SysFont("comicsans", 90)
            if (game.ganador() == 1 and player == 1) or (game.ganador() == 0 and player == 0):  #Simple condicional para asignar texto de quien ganó, empató o perdió
                text = font.render("GANO!", 1, (255,0,0)) #Los parentesis asignan su color
            elif game.ganador() == -1:
                text = font.render("EMPATE!", 1, (255,0,0))  #Los parentesis asignan su color
            else:
                text = font.render("DERROTA...", 1, (255, 0, 0)) #Los parentesis asignan su color

            ventana.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))  #La ubicacion en la pantalla
            pygame.display.update() #Actualiza
            pygame.time.delay(2000)

        for event in pygame.event.get(): #Manejamos eventos
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:  #Que pasa si hacemos click con el mouse en alguno de los botones
                pos = pygame.mouse.get_pos() #Obtenemos la posicion en la que se hizo click
                for btn in btns:  #recorremos el arreglo
                    if btn.click(pos) and game.conectado(): #si estamos conectados y se presionó en la posicion
                        if player == 0:
                            if not game.Jug1Movs:
                                n.send(btn.text) #se envia al servidor el boton con el texto respectivo que se seleccionó
                        else:
                            if not game.Jug2Movs:
                                n.send(btn.text)

        repintarVentana(ventana, game, player) #Repintar

def menu_screen(): #menu inicial
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        ventana.fill((128, 128, 128)) #Color o relleno de esa ventana
        font = pygame.font.SysFont("comicsans", 60) #Tipo de fuente y tamaño
        text = font.render("CLICK PARA JUGAR!", 1, (255,0,0)) #Texto inicial al correr cualquier jugador
        ventana.blit(text, (100, 200))
        pygame.display.update() #Actualiza

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

while True:
    menu_screen()
