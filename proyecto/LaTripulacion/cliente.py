import pygame

import juego
from red import Red
from configuracion import *
pygame.init()
pygame.mixer.init()

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("La Tripulación")
pygame.font.init()
fuente = pygame.font.SysFont('couriernew', 20, (74, 98, 234))
fuente2 = pygame.font.SysFont('couriernew', 15)
fuente3 = pygame.font.SysFont('couriernew', 30, (74, 98, 234))
fondo = pygame.image.load('images/fondo.jpg')
fondo2 = pygame.image.load('images/fondo2.png')
fondo_misiones = pygame.image.load('images/mision.png')
fondo_final = pygame.image.load('images/fondo_final.jpg')
icono=pygame.image.load('images/nave.png')
pygame.display.set_icon(icono)
class Boton:
    def __init__(self, texto, arriba_izquierda, boton_derecha, visible):
        self.texto = texto
        self.arriba_izquierda = arriba_izquierda
        self.boton_derecha = boton_derecha
        self.visible = visible
        self.ancho = self.boton_derecha[0] - self.arriba_izquierda[0]
        self.alto = self.boton_derecha[1] - self.arriba_izquierda[1]

    # Botón "VER PUNTUACIÓN"
    def dibujar_boton(self, pantalla):

        boton_de_pantalla = pygame.Surface((self.ancho, self.alto))
        boton_de_pantalla.fill((74, 98, 234))
        textofuente = fuente.render(self.texto, False, (255, 255, 255))
        boton_de_pantalla.blit(textofuente, (round(self.ancho / 2) - round(textofuente.get_width() / 2),
                                             round(self.alto / 2) - round(textofuente.get_height() / 2)))
        pantalla.blit(boton_de_pantalla, self.arriba_izquierda)

    def posicion_de_boton(self, pos):
        if self.arriba_izquierda[0] <= pos[0] <= (self.arriba_izquierda[0] + self.ancho) and \
                (self.boton_derecha[1] - self.alto) <= pos[1] <= self.boton_derecha[1]:
            return True
        else:
            return False


#########################################################################################
# Funciones de dibujo
#########################################################################################
def despliega_texto(oracion, tupla):
    fuente = pygame.font.SysFont("couriernew", 40)
    x, y = tupla
    y = y * 80  # interlineado
    caracter = ''
    letra = 0
    contador = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    for i in range(len(oracion)):
        pygame.time.wait(50)
        caracter = caracter + oracion[letra]
        texto = fuente.render(caracter, 1, (74, 98, 234))
        textorecto = texto.get_rect(topleft=(x, y))
        pantalla.blit(texto, textorecto)
        pygame.display.update(textorecto)
        contador += 1
        letra += 1


def mostrar_texto(pantalla, texto, pos, fuente, color):
    palabras = [palabra.split(' ') for palabra in
                texto.splitlines()]  # arreglo donde cada linea es una lista de de palabras.
    espacio = fuente.size(' ')[0]  # el ancho del espacio.
    max_ancho, max_alto = pantalla.get_size()
    x, y = pos
    for linea in palabras:
        for palabra in linea:
            superficie_palabra = fuente.render(palabra, 0, color)
            ancho_palabra, palabra_alto = superficie_palabra.get_size()
            if x + ancho_palabra >= max_ancho:
                x = pos[0]  # Resetea la x.
                y += palabra_alto  # empieza una nueva linea.
            pantalla.blit(superficie_palabra, (x, y))
            x += ancho_palabra + espacio
        x = pos[0]  # Resetea la x.
        y += palabra_alto  # empieza nueva linea.


def texto_inicial():
#    pygame.mixer.music.set_volume(0.04)
#    pygame.mixer.music.load("musica.mp3")
#    pygame.mixer.music.play(loops=-1, start=0.0)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    despliega_texto("Los científicos hablan de un misterioso planeta que se ", (0, 0))
    despliega_texto("supone que está en el borde de nuestro sistema solar.", (0, 1))
    despliega_texto("Pero a pesar de todos los esfuerzos, no han sido capaces", (0, 2))
    despliega_texto("de proporcionar pruebas sólidas de su existencia...", (0, 3))
    despliega_texto("Unánse a esta excitante aventura espacial para descubrirán", (0, 4))
    despliega_texto("si las teorías son solo ciencia ficción o si descubrirán", (0, 5))
    despliega_texto("el noveno planeta.", (0, 6))

    pygame.display.update()

def dibujar_pantalla_principal(pantalla, juego, jugador):
    pantalla.blit(fondo, (0, 0))
    pantalla.blit(fondo_misiones, (1050, 380))
    color = pygame.Color('white')

    string_texto_pantalla_jugador = f'Jugador {jugador + 1} '  # texto de pantalla jugador
    if juego.jugador_actual == jugador:
        string_texto_pantalla_jugador += '- Es tu turno'
    texto_pantalla_jugador = fuente.render(string_texto_pantalla_jugador, False, (255, 255, 255))
    pantalla.blit(texto_pantalla_jugador, (5, 5))

    for i, carta in enumerate(juego.jugadores[jugador].mano):
        pantalla.blit(carta.dibujar(), (i * 100 + 15, 500))
    dibujar_bazas(pantalla, jugador, juego.baza_actual.cartas)

    ################################################################################################################################################
    if juego.mision == 0:
        texto = """¡Felicidades! Han sido seleccionados entre una amplia cantidad de solicitantes para participar en la aventura más emocionante, más grande y más peligrosa de la humanidad: la Búsqueda del Desconocido 9º Planeta. Tan pronto como lleguen al campo de entrenamiento para las últimas pruebas, ya estarán en su primera fase de entrenamiento: Trabajo en equipo.
    [1 carta de tarea]"""
        mostrar_texto(pantalla, texto, (1070, 395), fuente2, color)
        texto_mision_aux = str('MISION 1')
        texto_mision = fuente.render(texto_mision_aux, False, (255, 255, 255))
        pantalla.blit(juego.dibujar_tarea(0), (ANCHO - 80, 5))
        texto_tarea_aux = 'Jugador ' + str(juego.jugador_cohete.numero_jugador + 1) + ' debe ganar: ' + str(
            juego.tarea_elegida[0])
        texto_tarea = fuente.render(texto_tarea_aux, False, (255, 255, 255))
        pantalla.blit(texto_tarea, (900, 25))
        pantalla.blit(texto_mision, (500, 5))
    ################################################################################################################################################
    elif juego.mision == 1:
        texto = """Resulta que están perfectamente coordinados. Sobre todo, su conexión mental, la llamada compatibilidad de deriva, indica una cooperación exitosa. Ahora se enfrentan a las fases de entrenamiento 2 y 3: Tecnología de control e Ingravidez.
    [2 cartas de tareas]"""
        mostrar_texto(pantalla, texto, (1070, 395), fuente2, color)
        texto_mision_aux = str('MISION 2')
        texto_mision = fuente.render(texto_mision_aux, False, (255, 255, 255))
        texto_tarea_aux1 = 'Jugador ' + str(juego.jugador_cohete.numero_jugador + 1) + ' debe ganar: ' + str(
            juego.tarea_elegida[0])

        if juego.jugador_cohete.numero_jugador == 3:
            texto_tarea_aux2 = 'Jugador ' + str(1) + ' debe ganar: ' + str(juego.tarea_elegida[1])
        else:
            texto_tarea_aux2 = 'Jugador ' + str(juego.jugador_cohete.numero_jugador + 2) + ' debe ganar: ' + str(
                juego.tarea_elegida[1])
        pantalla.blit(juego.dibujar_tarea(0), (ANCHO - 80, 5))
        pantalla.blit(juego.dibujar_tarea(1), (ANCHO - 80, 100))
        texto_tarea1 = fuente.render(texto_tarea_aux1, False, (255, 255, 255))
        texto_tarea2 = fuente.render(texto_tarea_aux2, False, (255, 255, 255))

        pantalla.blit(texto_tarea1, (900, 25))
        pantalla.blit(texto_tarea2, (900, 120))
        pantalla.blit(texto_mision, (500, 5))

        if juego.parte_mision_1:
            pantalla.blit(juego.dibujar_tarea_tachada(0), (ANCHO-80, 5))
        if juego.parte_mision_2:
            pantalla.blit(juego.dibujar_tarea_tachada(1), (ANCHO - 80, 100))
    ################################################################################################################################################
    elif juego.mision == 2:
        texto = """Las fases de entrenamiento se suceden. El curso combinado de suministro de energía y la priorización de emergencias requiere un alto grado de pensamiento lógico para comprender y aplicar las lecciones. Su educación matemática aquí es útil.
    [2 cartas de tareas][1][2]"""
        mostrar_texto(pantalla, texto, (1070, 395), fuente2, color)
        texto_mision_aux = str('MISION 3')
        texto_mision = fuente.render(texto_mision_aux, False, (255, 255, 255))
        texto_tarea_aux1 = 'Jugador ' + str(juego.jugador_cohete.numero_jugador + 1) + ' primero: ' + str(
            juego.tarea_elegida[0])

        if juego.jugador_cohete.numero_jugador == 3:
            texto_tarea_aux2 = 'Jugador ' + str(1) + ' segundo: ' + str(juego.tarea_elegida[1])
        else:
            texto_tarea_aux2 = 'Jugador ' + str(juego.jugador_cohete.numero_jugador + 2) + ' segundo: ' + str(
                juego.tarea_elegida[1])
        pantalla.blit(juego.dibujar_tarea(0), (ANCHO - 80, 5))
        pantalla.blit(juego.dibujar_tarea(1), (ANCHO - 80, 100))
        texto_tarea1 = fuente.render(texto_tarea_aux1, False, (255, 255, 255))
        texto_tarea2 = fuente.render(texto_tarea_aux2, False, (255, 255, 255))

        pantalla.blit(texto_tarea1, (900, 25))
        pantalla.blit(texto_tarea2, (900, 120))
        pantalla.blit(juego.dibujar_posicion_tarea(1), (1210, 20))
        pantalla.blit(juego.dibujar_posicion_tarea(2), (1210, 110))
        pantalla.blit(texto_mision, (500, 5))

        if juego.parte_mision_1:
            pantalla.blit(juego.dibujar_tarea_tachada(0), (ANCHO - 80, 5))
        if juego.parte_mision_2:
            pantalla.blit(juego.dibujar_tarea_tachada(1), (ANCHO - 80, 100))

    ##################################################################################################################################################
##################################################################################################################################################

    elif juego.mision == 3:
        texto = """Están a punto de completar su entrenamiento. Las últimas fases de entrenamiento tratan sobre la calibración de los módulos de control, la realineación de los comunicadores y los sistemas auxiliares avanzados de los trajes espaciales. Una vez hecho esto, ¡su verdadera misión puede comenzar!
    [3 cartas de tareas]"""
        mostrar_texto(pantalla, texto, (1070, 395), fuente2, color)
        texto_mision_aux = str('MISION 4')
        texto_mision = fuente.render(texto_mision_aux, False, (255, 255, 255))
        texto_tarea_aux1 = 'Jugador ' + str(juego.jugador_cohete.numero_jugador + 1) + ' debe ganar: ' + str(
            juego.tarea_elegida[0])

        if juego.jugador_cohete.numero_jugador == 1:
            texto_tarea_aux2 = 'Jugador ' + str(3) + ' debe ganar: ' + str(juego.tarea_elegida[1])
            texto_tarea_aux3 = 'Jugador ' + str(4) + ' debe ganar: ' + str(juego.tarea_elegida[2])
        elif juego.jugador_cohete.numero_jugador == 2:
            texto_tarea_aux2 = 'Jugador ' + str(4) + ' debe ganar:' + str(juego.tarea_elegida[1])
            texto_tarea_aux3 = 'Jugador ' + str(1) + ' debe ganar:' + str(juego.tarea_elegida[2])
        elif juego.jugador_cohete.numero_jugador == 3:
            texto_tarea_aux2 = 'Jugador ' + str(1) + ' debe ganar:' + str(juego.tarea_elegida[1])
            texto_tarea_aux3 = 'Jugador ' + str(2) + ' debe ganar:' + str(juego.tarea_elegida[2])

        else:
            texto_tarea_aux2 = 'Jugador ' + str(2) + ' debe ganar:' + str(
                juego.tarea_elegida[1])
            texto_tarea_aux3 = 'Jugador ' + str(3) + ' debe ganar:' + str(
                juego.tarea_elegida[2])

        pantalla.blit(juego.dibujar_tarea(0), (ANCHO - 80, 5))
        pantalla.blit(juego.dibujar_tarea(1), (ANCHO - 80, 100))
        pantalla.blit(juego.dibujar_tarea(2), (ANCHO - 80, 195))
        texto_tarea1 = fuente.render(texto_tarea_aux1, False, (255, 255, 255))
        texto_tarea2 = fuente.render(texto_tarea_aux2, False, (255, 255, 255))
        texto_tarea3 = fuente.render(texto_tarea_aux3, False, (255, 255, 255))

        pantalla.blit(texto_tarea1, (900, 25))
        pantalla.blit(texto_tarea2, (900, 120))
        pantalla.blit(texto_tarea3, (900, 225))
        pantalla.blit(texto_mision, (500, 5))

        if juego.parte_mision_1:
            pantalla.blit(juego.dibujar_tarea_tachada(0), (ANCHO - 80, 5))
        if juego.parte_mision_2:
            pantalla.blit(juego.dibujar_tarea_tachada(1), (ANCHO - 80, 100))
        if juego.parte_mision_3:
            pantalla.blit(juego.dibujar_tarea_tachada(2), (ANCHO - 80, 195))
###################################################################################################################################################
    elif juego.mision == 4:
        dibujar_pantalla_juego_terminado(pantalla, juego)


###################################################################################################################################################


def dibujar_bazas(pantalla, jugador, cartas):
    # posiciones_bazas = [(285, 315), (255, 285), (285, 255), (315, 285)]
    posiciones_bazas = [(255, 315), (225, 285), (285, 225), (315, 255)]

    # posiciones_bazas = [((ANCHO/2-220), ALTO/2), (((ANCHO/2-110)), ALTO/2), ((ANCHO/2), ALTO/2), (ANCHO/2+110, ALTO/2)]

    if len(cartas) > 0:
        jugador_inicial = cartas[0].jugador
        offset = jugador_inicial - jugador
        for i, carta in enumerate(cartas):
            pantalla.blit(carta.dibujar(), posiciones_bazas[(offset + i) % 4])


def pantalla_historia(texto_gana):
    pantalla.blit(fondo, (0, 0))

    texto = []
    texto.append()
    for i in range(len(texto)):
        despliega_texto(texto[i], (0, i * 2))

    pygame.display.update()


def dibujar_pantalla_juego_terminado(pantalla, juego):
    pantalla.blit(fondo_final, (0, 0))
    texto_juego_terminado = f"¡Felicitaciones! Han aterrizado a salvo en la Tierra. Su regreso sorpresa ha creado una respuesta mediática sin precedentes. " \
                            f"El salto a través del agujero de gusano se está extendiendo como un incendio por todos los continentes, es el tema de conversación." \
                            f" El reencuentro con vuestra familia y amigos os hace olvidar casi todos vuestros esfuerzos y después de un largo tiempo en el espacio" \
                            f" disfrutáis de la sensación de estar finalmente de nuevo en casa."
    mostrar_texto(pantalla,texto_juego_terminado, (0,0), fuente3, (255,255,255))
    mostrar_texto(pantalla, texto_juego_terminado, (0, 0), fuente3, (255, 255, 255))

#########################################################################################
# Funciones auxiliares
#########################################################################################


def posicion_en_cuadrado(pos, cuadrado):
    if cuadrado[0][0] <= pos[0] <= cuadrado[1][0] and cuadrado[0][1] <= pos[1] <= cuadrado[1][1]:
        return True
    else:
        return False
#########################################################################################
# Función principal
#########################################################################################
def principal():
    correr = True
    n = Red()
    numero_jugador = n.obtenerJugador()
    mostrar_historia = False
    boton_lista = [Boton('Ver historia', (1100, 645), (1350, 680), True),
                   Boton('Volver a juego', (1100, 645), (1350, 680), False)]

    juego = n.ping_server()
    longitud_mano = len(juego.jugadores[numero_jugador].mano)

    indice_clave = {pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3, pygame.K_4: 4, pygame.K_5: 5, pygame.K_6: 6,
                    pygame.K_7: 7, pygame.K_8: 8, pygame.K_9: 9, pygame.K_q: 10}

    indice_cartas = [[(i * 100 + 15, 500), (i * 100 + 115, 650)] for i in range(longitud_mano)]


    while correr:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr = False
                pygame.quit()

            if evento.type == pygame.KEYDOWN and evento.key in indice_clave:
                numero_carta = indice_clave[evento.key]

                juego = n.enviar(juego.jugadores[numero_jugador].mano[numero_carta - 1])

            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if 500 <= pos[1] <= 650:
                    for i, cuadrado in enumerate(indice_cartas):
                        if posicion_en_cuadrado(pos, cuadrado):
                            juego = n.enviar(juego.jugadores[numero_jugador].mano[i])
                            longitud_mano = len(juego.jugadores[numero_jugador].mano)
                            indice_cartas = [[(i * 100 + 15, 500), (i * 100 + 115, 650)] for i in range(longitud_mano)]
                            # [[(i * 35 + 15, 500), (i * 35 + 45, 650)]
                elif 645 <= pos[1] <= 680:
                    for i, boton in enumerate(boton_lista):
                        if i == 0:
                            if boton.visible and boton.posicion_de_boton(pos):
                                mostrar_historia = True
                        elif i == 1:
                            if boton.visible and boton.posicion_de_boton(pos):
                                mostrar_historia = False

        juego = n.ping_server()
        longitud_mano = len(juego.jugadores[numero_jugador].mano)
        indice_cartas = [[(i * 100 + 15, 500), (i * 100 + 115, 650)] for i in range(longitud_mano)]

        # esta seccion decide cual pantalla tiene que mostrarse
        if juego.ganador == 'no hay ganador':
            if mostrar_historia:
                pantalla.blit(fondo2, (0, 0))
                texto = """                         LA TRIPULACIÓN
Tras años de discusión, el 24 de agosto de 2006, la Unión Astronímica Internacional decidió retirarle a Plutón la categoría de noveno planeta de nuestro sistema solar. Desde entonces, nuestro sistema solar sólo contaba con ocho planetas, siendo Neptuno el octavo y el más alejado del Sol.

Años más tarde, sin embargo, surgió una teoría sensacional: que un cuerpo celeste enorme, hasta ahora desconocido, debe colocarse en el borde de nuestro sistema solar. El origen de estas teorías fueron los datos transmitidos por la nave espacial Voyager 2 y luego por New Horizons. Las distorsiones inusuales en sus mediciones y las interrupciones por fases en sus transmisiones dejaron a los científicos perplejos. Inicialmente descartado por sus compañeros como un producto de su imaginación, muchos escépticos finalmente se convencieron de la evidencia con el tiempo. Sin embargo, los datos finalmente resultaron inconclusos. A pesar de que un grupo de científicos lo había examinado a fondo, todavía no había proporcionado ninguna evidencia concreta de la teoría.

Sin opciones, el equipo de investigación organizado en torno al Dr. Markow creó el proyecto NAUTILUS: una misión tripulada que se enviaría para verificar la existencia del noveno Planeta. Tras años de investigación e incontables contratiempos, lograron por fin desarrollar la tecnología necesaria para llevar a cabo la misión. Y, ahora, la verdadera cuestión es: ¿con qué tripulación? ¿Estáis preparados para uniros al proyecto NAUTILUS? ¡Se necesitan voluntarios!"""
                mostrar_texto(pantalla, texto, (5, 5), fuente3, (255, 255, 255))
                boton_lista[0].visible = False
                boton_lista[1].visible = True

            else:
                dibujar_pantalla_principal(pantalla, juego, numero_jugador)
                boton_lista[0].visible = True
                boton_lista[1].visible = False
        else:
            dibujar_pantalla_juego_terminado(pantalla, juego)
            boton_lista[0].visible = False
            boton_lista[1].visible = False

        for boton in boton_lista:
            if boton.visible:
                boton.dibujar_boton(pantalla)

        pygame.display.update()



btns_menu = [Boton("Jugar", (170, 500), (370, 600), True), Boton("Créditos", (550, 500), (750, 600), True),
             Boton("Salir", (950, 500), (1150, 600), True)]


def pantalla_menu():
    correr = True
    reloj = pygame.time.Clock()
#    pygame.mixer.music.set_volume(0.09)
#    pygame.mixer.music.load("musica2.mp3")
#    pygame.mixer.music.play(loops=-1, start=0.0)

    while correr:
        reloj.tick(60)
        pantalla.blit(fondo, (0, 0))
        titulo = pygame.image.load('images/LaTripulacion2.png')
        pantalla.blit(titulo, (ANCHO / 2 - titulo.get_width() / 2, ALTO / 3 - titulo.get_height() / 3))
        for btn in btns_menu:
            btn.dibujar_boton(pantalla)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                # correr = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns_menu:
                    if btn.posicion_de_boton(pos) and btn.texto == "Jugar":
                        pantalla.blit(fondo, (0, 0))
                        texto_inicial()
                        pygame.display.update()
                        correr = False

                    elif btn.posicion_de_boton(pos) and btn.texto == "Salir":
                        pygame.quit()
                        # correr = False

    principal()


pantalla_menu()
