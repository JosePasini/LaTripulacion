import pygame
import random

import configuracion

pygame.font.init()
my_font = pygame.font.SysFont('calibri', 35)

class Carta:
    def __init__(self, color, numero, jugador):
        self.color = color
        self.numero = numero
        self.jugador = jugador

    def __str__(self):
        return self.numero + self.color #+ '-P' + str(self.jugador)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, Carta):
            return self.color == other.color and self.numero == other.numero and self.jugador == other.jugador
        else:
            return False


    #retorna una superficie de pygame con la informacion de las cartas que deben ser dibujadas en el cliente
    def dibujar(self):
        fondo = pygame.Surface((100, 150))
        if self.color == 'R':
                fondo = pygame.image.load('images/rosa.png')
                superficie_texto = my_font.render(self.numero, False, (235, 157, 227))
        elif self.color == 'V':
                fondo = pygame.image.load('images/verde.png')
                superficie_texto = my_font.render(self.numero, False, (136, 199, 138))
        elif self.color == 'Y':
                fondo = pygame.image.load('images/amarilla.png')
                superficie_texto = my_font.render(self.numero, False, (233, 226, 76))
        elif self.color == "A":
                fondo = pygame.image.load('images/azul.png')
                superficie_texto = my_font.render(self.numero, False, (76, 88, 233))
        elif self.color == 'C':
                fondo = pygame.image.load("images/cohete.png")
                superficie_texto = my_font.render(self.numero, False, (0, 0, 0))

        fondo.blit(superficie_texto, (7, 5))
        return fondo

    def obtener_valor_cartas(self):
        orden_valores = {'1':1, '2':2 , '3':3 , '4':4, '5':5 , '6':6 , '7':7 ,
                        '8':8 , '9':9, '10':10, '11':11, '12':12, '13':13}
        return orden_valores[self.numero]

class Baza:
    def __init__(self, jugador_inicial):
        self.jugador_inicial = jugador_inicial
        self.cartas = []
        self.color = False

    #chequea si la carta es valida para ser jugada y si es asi la añade a la baza
    def agregar_carta(self, carta):
        if len(self.cartas) == 0:
            self.color = carta.color
        self.cartas.append(carta)

    def ganador_baza(self):
        if len(self.cartas) < 4:
            return 'no hay ganador'
        elif [carta for carta in self.cartas if carta.color == 'C']:
            cartas_color_inicial = [carta for carta in self.cartas if carta.color == 'C']
            #cartas_color_inicial = [carta for carta in self.cartas if carta.color == self.color]
            return max(cartas_color_inicial, key=lambda p: p.obtener_valor_cartas()).jugador
        else:
            cartas_color_inicial = [carta for carta in self.cartas if carta.color == self.color]
            jugador_ganador= max(cartas_color_inicial, key=lambda p: p.obtener_valor_cartas()).jugador
            return jugador_ganador

    def dibujar(self, numero_jugador):
        posicion_dibujo_baza = [(50, 150), (0, 50), (50, 0), (100, 50)]
        fondo = pygame.Surface((150, 150))
        fondo.fill((255, 255, 255))
        offset = self.jugador_inicial - numero_jugador
        for carta in self.cartas:
            fondo.blit(carta.dibujar(), posicion_dibujo_baza[offset % 4])
        return fondo


    def __str__(self):
        cadena_color = self.color if self.color else 'No suit'
        return str(self.cartas)

def ordenar_mano(mano):
    def orden(carta):  #Rosado, Verde, Y Amarillo, Azul, Cohete

        orden_color = {'R': 1, 'V': 2, 'Y': 3, 'A': 4,'C': 5}

        orden_numero = {'1':1, '2':2 , '3':3 , '4':4, '5':5 , '6':6 , '7':7,
                        '8':8 , '9':9,'10': 10, '11': 11, '12': 12, '13': 13}

        if orden_color != 'C' and orden_numero != '10' and orden_numero != '11'and orden_numero != '12' and orden_numero != '13':
            return orden_color[carta.color] * 9 + orden_numero[carta.numero]
        elif orden_color == 'C' and orden_numero == '10' and orden_numero == '11' and orden_numero == '12' and orden_numero == '13':
            return  orden_color[carta.color] * 4 + orden_numero[carta.numero]

    return sorted(mano, key=orden)

class Jugador:
    def __init__(self, numero_jugador, mano_jugador):
        self.numero_jugador = numero_jugador
        self.mano = ordenar_mano(mano_jugador)
        self.bazas = []

    def __str__(self):
        return 'Jugador ' + str(self.numero_jugador)

    #determina si el jugador tiene una carta del color en su mano
    def tiene_color(self, color):
        for carta in self.mano:
            if carta.color == color:
                return True
        return False
    def tiene_cohete_4(self):
        for c in self.mano:
            if c.numero=='4' and c.color =='C':
                return True
                
class Juego:
    def __init__(self, mision):
        numeros = ['1','2','3', '4', '5', '6', '7', '8', '9']
        colores = ['R', 'Y', 'V', 'A'] # Rosado, Y-Amarillo, Verde, Azul, Cohete
        self.mision = mision

        numeros_cohete = ['1','2','3','4']
        color_cohete = ['C']

        valores_cartas = []
        for i in numeros:
            for j in colores:
                valores_cartas.append((j, i))

        for i in numeros_cohete:
            for j in color_cohete:
                valores_cartas.append((j,i))

        random.shuffle(valores_cartas)

        mazo0 = []
        mazo1 = []
        mazo2 = []
        mazo3 = []
        for i, carta_val in enumerate(valores_cartas):
            if i % 4 == 0:
                mazo0.append(Carta(carta_val[0], carta_val[1], 0))
            elif i % 4 == 1:
                mazo1.append(Carta(carta_val[0], carta_val[1], 1))
            elif i % 4 == 2:
                mazo2.append(Carta(carta_val[0], carta_val[1], 2))
            else:
                mazo3.append(Carta(carta_val[0], carta_val[1], 3))


        self.p0 = Jugador(0, mazo0)
        self.p1 = Jugador(1, mazo1)
        self.p2 = Jugador(2, mazo2)
        self.p3 = Jugador(3, mazo3)

        self.jugadores = [self.p0, self.p1, self.p2, self.p3]

        tareas = []
        for i in numeros:
            for j in colores:
                tareas.append((j, i))
        random.shuffle(tareas)
        tareas1 = []
        for carta_val in tareas[0:4]:
            tareas1.append(Tarea(carta_val[0], carta_val[1]))
        self.tarea_elegida = [tareas1.pop(), tareas1.pop(), tareas1.pop(), tareas1.pop()]
        print("TAREAS1: " , tareas1)
        print("TAREAS ELEGIDAS: " , self.tarea_elegida)

        self.contador_baza = 0
        self.cohetes_jugados = False
        self.fin_ronda = False
        self.fin_ronda_mision = False
        self.jugador_actual = 0
        self.baza_actual = Baza(0)
        self.ganador = 'no hay ganador'
        self.listo = False
        self.parte_mision_1 = False
        self.parte_mision_2 = False
        self.parte_mision_3 = False
        self.mision_fallida = True

        for i in range(5):
            if self.jugadores[i].tiene_cohete_4():
                self.jugador_cohete = self.jugadores[i]
                break



    def dibujar_tarea(self, indice):
        fondo = pygame.Surface((50, 71))
        fondo.blit(self.tarea_elegida[indice].dibujar(), (0, 0))
        return fondo

    def dibujar_tarea_tachada(self, indice):
        fondo = pygame.Surface((50,71))
        fondo.blit(self.tarea_elegida[indice].dibujar_tarea_tachada(), (0,0))
        return fondo


    def dibujar_posicion_tarea(self, ind):

        posicion1 = pygame.image.load('images/CartasTareas/orden1.png')
        posicion2 = pygame.image.load('images/CartasTareas/orden2.png')

        if ind == 1:
            return posicion1
        elif ind == 2:
            return posicion2

    def conectado(self):
        return self.listo

    #revisa si la carta tirada está perimita para tirar en la baza, es decir corrobarndo si el jugador tiene esa carta
    #si la baza yatiene las 4 cartas y si el color es correcto
    def carta_valida(self, carta):
        if self.jugador_actual == carta.jugador and any(
                [carta == mano_carta for mano_carta in self.jugadores[carta.jugador].mano]):
            if len(self.baza_actual.cartas) == 0:
                if carta.color != 'g':
                    return True
                else:
                    if self.cohetes_jugados:
                        return True
                    else:
                        return False
            elif len(self.baza_actual.cartas) < 4:
                if carta.color == self.baza_actual.color:
                    return True
                else:
                    if self.jugadores[self.jugador_actual].tiene_color(self.baza_actual.color):
                        return False
                    else:
                        return True
            else:
                return False
        return False

    #agrega la carta a la baza despues de corroborar si es adecuada para ser añadida
    def agregar_carta(self, carta):
        if self.carta_valida(carta):
            # Agrega las cartas a la baza
            self.baza_actual.agregar_carta(carta)
            # Identifica la carta correspondiente de la mano del jugador y la elimina

            carta_servidor = [carta_mano for carta_mano in self.jugadores[self.jugador_actual].mano if carta_mano == carta].pop()
            self.jugadores[self.jugador_actual].mano.remove(carta_servidor)
            # Cambia el turno
            self.cambiar_turno()

            # Si la carta que acaba de jugar es un cohete, asignarle verdadero a cohete_jugados

            if carta.color == 'C':
                self.cohetes_jugados = True
            print(self.baza_actual)
        # revisa si la baza tiene un ganador

        ganador_baza = self.baza_actual.ganador_baza()

# Hasta acá llegaría la clase Juego


        if ganador_baza != 'no hay ganador':
            print(f'Jugador {ganador_baza + 1} ganó la baza!')
            self.jugadores[ganador_baza].bazas.append(self.baza_actual)

##################################################################################################################################################################
            if self.mision ==0:
                if self.tarea_elegida[0].__str__() in self.baza_actual.cartas.__str__() and ganador_baza != self.jugador_cohete.numero_jugador:
                    print("GANÓ LA CARTA EL JUGADOR EQUIVOCADO")
                    self.fin_ronda = True
                if self.tarea_elegida[0].__str__() in self.baza_actual.cartas.__str__() and ganador_baza == self.jugador_cohete.numero_jugador:
                    print("MISIÓN 1 COMPLETADA, AHORA PASAREMOS A LA SIGUIENTE MISIÓN")
                    self.fin_ronda_mision = True
            if sum([len(self.jugadores[i].bazas) for i in range(4)]) == 10:
                self.fin_ronda = True
###################################################################################################################################################################
            elif self.mision == 1:

                if self.jugador_cohete.numero_jugador == 3: # Condicion que cambia el numero de jugador en el caso de ser el primero el 4

                    if self.tarea_elegida[0].__str__() in self.baza_actual.cartas.__str__() and ganador_baza != self.jugador_cohete.numero_jugador:
                        print("GANÓ LA CARTA EL JUGADOR EQUIVOCADO")
                        self.fin_ronda = True

                    if self.tarea_elegida[1].__str__() in self.baza_actual.cartas.__str__() and ganador_baza != (0):
                        print("GANÓ LA CARTA EL JUGADOR EQUIVOCADO")
                        self.fin_ronda = True


                    if self.tarea_elegida[0].__str__() in self.baza_actual.cartas.__str__() and ganador_baza == (### OPCION EN CASO DE QUE EL PRIMER JUGADOR SEA EL 4
                    self.jugador_cohete.numero_jugador):
                        self.baza_actual = Baza(ganador_baza)
                        self.jugador_actual = ganador_baza
                        self.parte_mision_1 = True
                        print("PARTE 1 DE MISIÓN 2 COMPLETADA")
                    elif self.tarea_elegida[1].__str__() in self.baza_actual.cartas.__str__() and ganador_baza == (0):
                        self.baza_actual = Baza(ganador_baza)
                        self.jugador_actual = ganador_baza
                        self.parte_mision_2 = True
                        print("PARTE 2 DE MISION 2 COMPLETADA")
                else: ### OPCION EN CASO DE QUE EL PRIMER JUGADOR NO SEA EL 4

                    if self.tarea_elegida[0].__str__() in self.baza_actual.cartas.__str__() and ganador_baza != self.jugador_cohete.numero_jugador:
                        print("GANÓ LA CARTA EL JUGADOR EQUIVOCADO")
                        self.fin_ronda = True

                    if self.tarea_elegida[1].__str__() in self.baza_actual.cartas.__str__() and ganador_baza != self.jugador_cohete.numero_jugador+1:
                        print("GANÓ LA CARTA EL JUGADOR EQUIVOCADO")
                        self.fin_ronda = True

                    if self.tarea_elegida[0].__str__() in self.baza_actual.cartas.__str__() and ganador_baza == (
                    self.jugador_cohete.numero_jugador):
                        self.baza_actual = Baza(ganador_baza)
                        self.jugador_actual = ganador_baza
                        self.parte_mision_1 = True
                        print("PARTE 1 DE MISIÓN 2 COMPLETADA")
                    elif self.tarea_elegida[1].__str__() in self.baza_actual.cartas.__str__() and ganador_baza == (
                            self.jugador_cohete.numero_jugador + 1):
                        self.baza_actual = Baza(ganador_baza)
                        self.jugador_actual = ganador_baza
                        self.parte_mision_2 = True
                        print("PARTE 2 DE MISIÓN 2 COMPLETADA")
            if self.parte_mision_1 and self.parte_mision_2:
                self.fin_ronda_mision = True
                print("MISIÓN 2 COMPLETADA, REINICIO DE BANDERAS")
###################################################################################################################################################################
            elif self.mision == 2:
                if self.jugador_cohete.numero_jugador == 3:
                    if self.tarea_elegida[0].__str__() in self.baza_actual.cartas.__str__() and ganador_baza != (
                    self.jugador_cohete.numero_jugador):
                        print("Ganó la tarea 1 el jugador equivocado")
                        self.fin_ronda = True
                    if self.tarea_elegida[1].__str__() in self.baza_actual.cartas.__str__() and ganador_baza != (0):
                        print("Ganó la tarea 2 el jugador equivocado")
                        self.fin_ronda = True
                    if self.mision_fallida:
                        if self.tarea_elegida[1].__str__() in self.baza_actual.cartas.__str__() and ganador_baza == (0):
                            print("Ganó el segundo antes que el primero")
                            self.fin_ronda = True
                    if self.tarea_elegida[0].__str__() in self.baza_actual.cartas.__str__() and ganador_baza == (self.jugador_cohete.numero_jugador):
                        self.baza_actual = Baza(ganador_baza)
                        self.jugador_actual = ganador_baza
                        self.parte_mision_1 = True
                        self.mision_fallida=False
                        print("PARTE 1 DE MISIÓN 3 COMPLETADA")
                    elif self.parte_mision_1 == True and self.tarea_elegida[
                        1].__str__() in self.baza_actual.cartas.__str__() and ganador_baza == (0):
                        self.baza_actual = Baza(ganador_baza)
                        self.jugador_actual = ganador_baza
                        self.parte_mision_2 = True
                        print("PARTE 2 DE MISIÓN 3 COMPLETADA")
                if self.parte_mision_1 and self.parte_mision_2:
                    print("MISIÓN 3 COMPLETADA, REINICIO DE BANDERAS")
                    self.fin_ronda_mision = True
                else:
                    if self.tarea_elegida[0].__str__() in self.baza_actual.cartas.__str__() and ganador_baza != (
                    self.jugador_cohete.numero_jugador):
                        print("Ganó la tarea 1 el jugador equivocado")
                        self.fin_ronda = True
                    if self.tarea_elegida[1].__str__() in self.baza_actual.cartas.__str__() and ganador_baza != (
                            self.jugador_cohete.numero_jugador + 1):
                        print("Ganó la tarea 2 el jugador equivocado")
                        self.fin_ronda = True
                    if self.mision_fallida:
                        if self.tarea_elegida[1].__str__() in self.baza_actual.cartas.__str__() and ganador_baza == (self.jugador_cohete.numero_jugador + 1):
                            print("Ganó el segundo antes que el primero")
                            self.fin_ronda = True
                    if self.tarea_elegida[0].__str__() in self.baza_actual.cartas.__str__() and ganador_baza == (
                    self.jugador_cohete.numero_jugador):
                        self.baza_actual = Baza(ganador_baza)
                        self.jugador_actual = ganador_baza
                        self.parte_mision_1 = True
                        self.mision_fallida = False
                        print("PARTE 1 DE MISIÓN 3 COMPLETADA")
                    elif self.parte_mision_1 == True and self.tarea_elegida[
                        1].__str__() in self.baza_actual.cartas.__str__() and ganador_baza == (
                            self.jugador_cohete.numero_jugador + 1):
                        self.baza_actual = Baza(ganador_baza)
                        self.jugador_actual = ganador_baza
                        self.parte_mision_2 = True
                        print("PARTE 2 DE MISIÓN 3 COMPLETADA")
                if self.parte_mision_1 and self.parte_mision_2:
                    print("MISIÓN 3 COMPLETADA, REINICIO DE BANDERAS")
                    self.fin_ronda_mision = True
                    
##################################################################################################################################################################
            #Mision 3
##################################################################################################################################################################
            elif self.mision == 3:

                if self.jugador_cohete.numero_jugador == 3: # Condicion que cambia el numero de jugador en el caso de ser el primero el 4

                    if self.tarea_elegida[0].__str__() in self.baza_actual.cartas.__str__() and ganador_baza != self.jugador_cohete.numero_jugador:
                        print("GANÓ LA CARTA EL JUGADOR EQUIVOCADO")
                        self.fin_ronda = True

                    if self.tarea_elegida[1].__str__() in self.baza_actual.cartas.__str__() and ganador_baza != (0):
                        print("GANÓ LA CARTA EL JUGADOR EQUIVOCADO")
                        self.fin_ronda = True

                    if self.tarea_elegida[2].__str__() in self.baza_actual.cartas.__str__() and ganador_baza != (1):
                        print("GANÓ LA CARTA EL JUGADOR EQUIVOCADO")
                        self.fin_ronda = True

                    if self.tarea_elegida[0].__str__() in self.baza_actual.cartas.__str__() and ganador_baza == (### OPCION EN CASO DE QUE EL PRIMER JUGADOR SEA EL 4
                    self.jugador_cohete.numero_jugador):
                        self.baza_actual = Baza(ganador_baza)
                        self.jugador_actual = ganador_baza
                        self.parte_mision_1 = True
                        print("PARTE 1 DE MISIÓN 4 COMPLETADA")
                    elif self.tarea_elegida[1].__str__() in self.baza_actual.cartas.__str__() and ganador_baza == (0):
                        self.baza_actual = Baza(ganador_baza)
                        self.jugador_actual = ganador_baza
                        self.parte_mision_2 = True
                        print("PARTE 2 DE MISIÓN 4 COMPLETADA")
                    elif self.tarea_elegida[2].__str__() in self.baza_actual.cartas.__str__() and ganador_baza == (1):
                        self.baza_actual = Baza(ganador_baza)
                        self.jugador_actual = ganador_baza
                        self.parte_mision_3 = True
                        print("PARTE 3 DE MISIÓN 4 COMPLETADA")
                else: ### OPCION EN CASO DE QUE EL PRIMER JUGADOR NO SEA EL 4

                    if self.tarea_elegida[0].__str__() in self.baza_actual.cartas.__str__() and ganador_baza != self.jugador_cohete.numero_jugador:
                        print("GANÓ LA CARTA EL JUGADOR EQUIVOCADO")
                        self.fin_ronda = True

                    if self.tarea_elegida[1].__str__() in self.baza_actual.cartas.__str__() and ganador_baza != self.jugador_cohete.numero_jugador+1:
                        print("GANÓ LA CARTA EL JUGADOR EQUIVOCADO")
                        self.fin_ronda = True
                    if self.tarea_elegida[2].__str__() in self.baza_actual.cartas.__str__() and ganador_baza != self.jugador_cohete.numero_jugador+2:
                        print("GANÓ LA CARTA EL JUGADOR EQUIVOCADO")
                        self.fin_ronda = True

                    if self.tarea_elegida[0].__str__() in self.baza_actual.cartas.__str__() and ganador_baza == (
                        self.jugador_cohete.numero_jugador):
                        self.baza_actual = Baza(ganador_baza)
                        self.jugador_actual = ganador_baza
                        self.parte_mision_1 = True
                        print("PARTE 1 DE MISIÓN 4 COMPLETADA")
                    elif self.tarea_elegida[1].__str__() in self.baza_actual.cartas.__str__() and ganador_baza == (
                            self.jugador_cohete.numero_jugador + 1):
                        self.baza_actual = Baza(ganador_baza)
                        self.jugador_actual = ganador_baza
                        self.parte_mision_2 = True
                        print("PARTE 2 DE MISIÓN 4 COMPLETADA")
                    elif self.tarea_elegida[2].__str__() in self.baza_actual.cartas.__str__() and ganador_baza == (
                            self.jugador_cohete.numero_jugador + 2):
                        self.baza_actual = Baza(ganador_baza)
                        self.jugador_actual = ganador_baza
                        self.parte_mision_3 = True
                        print("PARTE 3 DE MISIÓN 4 COMPLETADA")


            if self.parte_mision_1 and self.parte_mision_2 and self.parte_mision_3:
                self.fin_ronda_mision = True
                print("MISIÓN 4 COMPLETADA, REINICIO DE BANDERAS")


##################################################################################################################################################################
            else:
                self.baza_actual = Baza(ganador_baza)
                self.jugador_actual = ganador_baza
                for i in range(4):
                    print(f'Jugador {i + 1} ha ganado estas bazas: {[str(baza) for baza in self.jugadores[i].bazas]}')
##################################################################################################################################################################
##################################################################################################################################################################
    def cambiar_turno(self):
        self.jugador_actual += 1
        self.jugador_actual = self.jugador_actual % 4

    def round_over(self):
        if self.ganador != 'no hay ganador':
            self.fin_juego()

    def fin_juego(self):
        pass

    def __str__(self):
        return str(self.jugador_actual)

class Tarea:
    def __init__(self, color, numero):
            self.color = color
            self.numero = numero


    def __str__(self):
        return self.numero + self.color

    def __repr__(self):
        return self.__str__()


    def __eq__(self, other):
        if isinstance(other, Carta):
            return self.color == other.color and self.numero == other.numero
        else:
            return False

    def dibujar(self):
        fondo = pygame.Surface((50, 71))

        if self.color == 'R':
            if self.numero=='1':
                fondo = pygame.image.load('images/CartasTareas/rosa1.png')
            elif self.numero=='2':
                fondo = pygame.image.load('images/CartasTareas/rosa2.png')
            elif self.numero=='3':
                fondo = pygame.image.load('images/CartasTareas/rosa3.png')
            elif self.numero=='4':
                fondo = pygame.image.load('images/CartasTareas/rosa4.png')
            elif self.numero=='5':
                fondo = pygame.image.load('images/CartasTareas/rosa5.png')
            elif self.numero=='6':
                fondo = pygame.image.load('images/CartasTareas/rosa6.png')
            elif self.numero=='7':
                fondo = pygame.image.load('images/CartasTareas/rosa7.png')
            elif self.numero=='8':
                fondo = pygame.image.load('images/CartasTareas/rosa8.png')
            elif self.numero=='9':
                fondo = pygame.image.load('images/CartasTareas/rosa9.png')

        elif self.color == 'V':
            if self.numero == '1':
                fondo = pygame.image.load('images/CartasTareas/verde1.png')
            elif self.numero == '2':
                fondo = pygame.image.load('images/CartasTareas/verde2.png')
            elif self.numero == '3':
                fondo = pygame.image.load('images/CartasTareas/verde3.png')
            elif self.numero == '4':
                fondo = pygame.image.load('images/CartasTareas/verde4.png')
            elif self.numero == '5':
                fondo = pygame.image.load('images/CartasTareas/verde5.png')
            elif self.numero == '6':
                fondo = pygame.image.load('images/CartasTareas/verde6.png')
            elif self.numero == '7':
                fondo = pygame.image.load('images/CartasTareas/verde7.png')
            elif self.numero == '8':
                fondo = pygame.image.load('images/CartasTareas/verde8.png')
            elif self.numero == '9':
                fondo = pygame.image.load('images/CartasTareas/verde9.png')
        elif self.color == 'Y':
            if self.numero == '1':
                fondo = pygame.image.load('images/CartasTareas/amarilla1.png')
            elif self.numero == '2':
                fondo = pygame.image.load('images/CartasTareas/amarilla2.png')
            elif self.numero == '3':
                fondo = pygame.image.load('images/CartasTareas/amarilla3.png')
            elif self.numero == '4':
                fondo = pygame.image.load('images/CartasTareas/amarilla4.png')
            elif self.numero == '5':
                fondo = pygame.image.load('images/CartasTareas/amarilla5.png')
            elif self.numero == '6':
                fondo = pygame.image.load('images/CartasTareas/amarilla6.png')
            elif self.numero == '7':
                fondo = pygame.image.load('images/CartasTareas/amarilla7.png')
            elif self.numero == '8':
                fondo = pygame.image.load('images/CartasTareas/amarilla8.png')
            elif self.numero == '9':
                fondo = pygame.image.load('images/CartasTareas/amarilla9.png')

        elif self.color == "A":
            if self.numero == '1':
                fondo = pygame.image.load('images/CartasTareas/azul1.png')
            elif self.numero == '2':
                fondo = pygame.image.load('images/CartasTareas/azul2.png')
            elif self.numero == '3':
                fondo = pygame.image.load('images/CartasTareas/azul3.png')
            elif self.numero == '4':
                fondo = pygame.image.load('images/CartasTareas/azul4.png')
            elif self.numero == '5':
                fondo = pygame.image.load('images/CartasTareas/azul5.png')
            elif self.numero == '6':
                fondo = pygame.image.load('images/CartasTareas/azul6.png')
            elif self.numero == '7':
                fondo = pygame.image.load('images/CartasTareas/azul7.png')
            elif self.numero == '8':
                fondo = pygame.image.load('images/CartasTareas/azul8.png')
            elif self.numero == '9':
                fondo = pygame.image.load('images/CartasTareas/azul9.png')

        return fondo
        
    def dibujar_tarea_tachada(self):
        fondo = pygame.Surface((50, 71))

        if self.color == 'R':
            if self.numero=='1':
                fondo = pygame.image.load('images/CartasTachadas/rosa1_tachada.png')
            elif self.numero=='2':
                fondo = pygame.image.load('images/CartasTachadas/rosa2_tachada.png')
            elif self.numero=='3':
                fondo = pygame.image.load('images/CartasTachadas/rosa3_tachada.png')
            elif self.numero=='4':
                fondo = pygame.image.load('images/CartasTachadas/rosa4_tachada.png')
            elif self.numero=='5':
                fondo = pygame.image.load('images/CartasTachadas/rosa5_tachada.png')
            elif self.numero=='6':
                fondo = pygame.image.load('images/CartasTachadas/rosa6_tachada.png')
            elif self.numero=='7':
                fondo = pygame.image.load('images/CartasTachadas/rosa7_tachada.png')
            elif self.numero=='8':
                fondo = pygame.image.load('images/CartasTachadas/rosa8_tachada.png')
            elif self.numero=='9':
                fondo = pygame.image.load('images/CartasTachadas/rosa9_tachada.png')

        elif self.color == 'V':
            if self.numero == '1':
                fondo = pygame.image.load('images/CartasTachadas/verde1_tachada.png')
            elif self.numero == '2':
                fondo = pygame.image.load('images/CartasTachadas/verde2_tachada.png')
            elif self.numero == '3':
                fondo = pygame.image.load('images/CartasTachadas/verde3_tachada.png')
            elif self.numero == '4':
                fondo = pygame.image.load('images/CartasTachadas/verde4_tachada.png')
            elif self.numero == '5':
                fondo = pygame.image.load('images/CartasTachadas/verde5_tachada.png')
            elif self.numero == '6':
                fondo = pygame.image.load('images/CartasTachadas/verde6_tachada.png')
            elif self.numero == '7':
                fondo = pygame.image.load('images/CartasTachadas/verde7_tachada.png')
            elif self.numero == '8':
                fondo = pygame.image.load('images/CartasTachadas/verde8_tachada.png')
            elif self.numero == '9':
                fondo = pygame.image.load('images/CartasTachadas/verde9_tachada.png')
        elif self.color == 'Y':
            if self.numero == '1':
                fondo = pygame.image.load('images/CartasTachadas/amarilla1_tachada.png')
            elif self.numero == '2':
                fondo = pygame.image.load('images/CartasTachadas/amarilla2_tachada.png')
            elif self.numero == '3':
                fondo = pygame.image.load('images/CartasTachadas/amarilla3_tachada.png')
            elif self.numero == '4':
                fondo = pygame.image.load('images/CartasTachadas/amarilla4_tachada.png')
            elif self.numero == '5':
                fondo = pygame.image.load('images/CartasTachadas/amarilla5_tachada.png')
            elif self.numero == '6':
                fondo = pygame.image.load('images/CartasTachadas/amarilla6_tachada.png')
            elif self.numero == '7':
                fondo = pygame.image.load('images/CartasTachadas/amarilla7_tachada.png')
            elif self.numero == '8':
                fondo = pygame.image.load('images/CartasTachadas/amarilla8_tachada.png')
            elif self.numero == '9':
                fondo = pygame.image.load('images/CartasTachadas/amarilla9_tachada.png')

        elif self.color == "A":
            if self.numero == '1':
                fondo = pygame.image.load('images/CartasTachadas/azul1_tachada.png')
            elif self.numero == '2':
                fondo = pygame.image.load('images/CartasTachadas/azul2_tachada.png')
            elif self.numero == '3':
                fondo = pygame.image.load('images/CartasTachadas/azul3_tachada.png')
            elif self.numero == '4':
                fondo = pygame.image.load('images/CartasTachadas/azul4_tachada.png')
            elif self.numero == '5':
                fondo = pygame.image.load('images/CartasTachadas/azul5_tachada.png')
            elif self.numero == '6':
                fondo = pygame.image.load('images/CartasTachadas/azul6_tachada.png')
            elif self.numero == '7':
                fondo = pygame.image.load('images/CartasTachadas/azul7_tachada.png')
            elif self.numero == '8':
                fondo = pygame.image.load('images/CartasTachadas/azul8_tachada.png')
            elif self.numero == '9':
                fondo = pygame.image.load('images/CartasTachadas/azul9_tachada.png')

        return fondo
                    
