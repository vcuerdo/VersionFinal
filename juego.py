class Game: #Clase juego
    def __init__(self, id):
        self.Jug1Movs = False  #booleano sobre movimientos del jugador 1
        self.Jug2Movs = False  #booleano sobre movimientos del jugador 2
        self.listo = False     #booleano sobre listo para iniciar o no
        self.id = id           #id
        self.movimientos = [None, None] #Movimientos, se reciben como tuplas de datos X,Y
        self.victorias = [0, 0]  #Numero de victorias
        self.empates = 0  #Numero de empates

    def get_mov_jugador(self, p):  #obtener los movimientos del jugador
        """
        :param p: [0,1]
        :return: Move
        """
        return self.movimientos[p] #Regresa un array de movimientos del jugador

    def play(self, player, move): #Jugar recibw un jugador con su movimiento
        self.movimientos[player] = move
        if player == 0:   #Si el jugador es el 1 entonces el booleano que lleva los movimientos de este jugador cambia a verdadero
            self.Jug1Movs = True
        else:
            self.Jug2Movs = True #Si no fue porque se movió el jugador 2

    def conectado(self):  #Regresa si hubo conexion y esta listo
        return self.listo

    def ambosMovieron(self): #Ambos movieron
        return self.Jug1Movs and self.Jug2Movs

    def ganador(self): #Definimos un metodo de ganador

        j1 = self.movimientos[0].upper()[0]  #Jugador 1
        j2 = self.movimientos[1].upper()[0]  #Jugador 2

        ganador = -1 #No sabemos quien va a ganar, y como los jugadores son representados por 0 ó 1, asignamos cualquier valor
        if j1 == "R" and j2 == "T":    #Si jugador 1 elije Roca y jugador 2 elije Tijeras  R=roca, T=tijeras
            ganador = 0 #asigna al jugador 1 como ganador
        elif j1 == "T" and j2 == "R":   #Si jugador 1 elije Roca y jugador 2 elije Tijeras  R=roca, T=tijeras
            ganador = 1 #asigna al jugador 2 como ganador
        elif j1 == "P" and j2 == "R":   #Si jugador 1 elije Roca y jugador 2 elije Tijeras  R=roca, T=tijeras
            ganador = 0 #asigna al jugador 1 como ganador
        elif j1 == "R" and j2 == "P":    #Si jugador 1 elije Roca y jugador 2 elije Tijeras  R=roca, T=tijeras
            ganador = 1 #asigna al jugador 2 como ganador
        elif j1 == "T" and j2 == "P":    #Si jugador 1 elije Roca y jugador 2 elije Tijeras  R=roca, T=tijeras
            ganador = 0 #asigna al jugador 1 como ganador
        elif j1 == "P" and j2 == "T":    #Si jugador 1 elije piedra y jugador 2 elije Tijeras  R=roca, T=tijeras
            ganador = 1 #asigna al jugador 2 como ganador

        return ganador #Regresa quien ganó la partida

    def resetMovs(self):  #Resetar movimientos
        self.Jug1Movs = False
        self.Jug2Movs = False
