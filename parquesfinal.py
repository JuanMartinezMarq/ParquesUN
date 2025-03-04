import pygame
import random

# Se debe inicializar pygame
pygame.init()

# Definir constantes
ANCHO, ALTO = 900, 900
FONDO_COLOR = (240, 240, 240)
COLORES_EQUIPO = [
    (255, 0, 0),    # Rojo
    (0, 0, 255),    # Azul
    (0, 180, 0),    # Verde
    (255, 255, 0)   # Amarillo
]
NOMBRES_EQUIPO = ["ROJO", "AZUL", "VERDE", "AMARILLO"]
NUM_EQUIPOS = 4
NUM_FICHAS = 4
NUM_CASILLAS_EXTERNAS = 68
NUM_CASILLAS_INTERNAS = 8

FUENTE_PEQUEÑA = pygame.font.SysFont('Arial', 16)
FUENTE_MEDIA = pygame.font.SysFont('Arial', 22)
FUENTE_GRANDE = pygame.font.SysFont('Arial', 30)

class Ficha: #Se van a usar clases para la modularidad y organizacion
    def __init__(self, equipo, numero):
        self.equipo = equipo  
        self.numero = numero  
        self.en_carcel = True
        self.en_llegada = False
        self.posicion_externa = None
        self.posicion_interna = None
        self.radio = 18

    def esta_en_casilla_externa(self, casilla):
        return self.posicion_externa == casilla and not self.en_carcel and not self.en_llegada

    def esta_en_casilla_interna(self, casilla):
        return self.posicion_interna == casilla and not self.en_carcel and self.en_llegada
    
    def reset(self):
        self.en_carcel = True
        self.en_llegada = False
        self.posicion_externa = None
        self.posicion_interna = None

class Tablero:
    def __init__(self):
        self.casillas_externas = [(0, 0) for _ in range(NUM_CASILLAS_EXTERNAS)]
        self.casillas_internas = [[(0, 0) for _ in range(NUM_CASILLAS_INTERNAS)] for _ in range(NUM_EQUIPOS)]
        self.carceles = [(0, 0) for _ in range(NUM_EQUIPOS)]
        
        # Índices de las casillas importantes
        self.salidas = [0, 17, 34, 51]  # Salidas para cada equipo (rojo, azul, verde, amarillo)
        self.seguros = [0, 8, 17, 25, 34, 42, 51, 59]  # Casillas seguras
        self.inicios_casillas_internas = [63, 14, 31, 48]  
        
        self._calcular_posiciones()

    def _calcular_posiciones(self):
        self.casillas_externas = [(0, 0) for _ in range(NUM_CASILLAS_EXTERNAS)]
        
        centro_x, centro_y = 450, 450
        radio = 350
        
        # Casillas externas
        for i in range(NUM_CASILLAS_EXTERNAS):
            angulo = 2 * 3.14159 * i / NUM_CASILLAS_EXTERNAS
        
        # Casillas internas
        for e in range(NUM_EQUIPOS):
            for i in range(NUM_CASILLAS_INTERNAS):
                angulo = 2 * 3.14159 * self.salidas[e] / NUM_CASILLAS_EXTERNAS              
        
        # Posiciones de las cárceles (esquinas)
        self.carceles[0] = (150, 150)  # Rojo
        self.carceles[1] = (750, 150)  # Azul
        self.carceles[2] = (750, 750)  # Verde
        self.carceles[3] = (150, 750)  # Amarillo

    def es_seguro(self, posicion):
        return posicion in self.seguros

    def es_salida(self, posicion):
        return posicion in self.salidas

    def dibujar(self, pantalla):
        # Fondo del tablero
        pantalla.fill((255, 255, 255))
        tamano_total = min(ANCHO, ALTO) - 100
        cell_size = tamano_total // 15
        center_size = cell_size * 3
    
        # Borde del tablero
        board_rect = pygame.Rect(50, 50, tamano_total, tamano_total)
        pygame.draw.rect(pantalla, (0, 0, 0), board_rect, 5)
    
        for i in range(1, 15):
            pygame.draw.line(pantalla, (0, 0, 0), (50 + i * cell_size, 50), (50 + i * cell_size, 50 + tamano_total), 2)
            pygame.draw.line(pantalla, (0, 0, 0), (50, 50 + i * cell_size), (50 + tamano_total, 50 + i * cell_size), 2)
    
        # Zona central
        pygame.draw.polygon(pantalla, (0, 0, 0), [
            (50 + tamano_total//2 - center_size//2, 50 + tamano_total//2 - center_size//2),
            (50 + tamano_total//2 + center_size//2, 50 + tamano_total//2 - center_size//2),
            (50 + tamano_total//2 + center_size//2, 50 + tamano_total//2 + center_size//2),
            (50 + tamano_total//2 - center_size//2, 50 + tamano_total//2 + center_size//2)
        ], 5)

        pygame.draw.line(pantalla, (0, 0, 0), 
                     (50 + tamano_total//2 - center_size//2, 50 + tamano_total//2 - center_size//2), 
                     (50 + tamano_total//2 + center_size//2, 50 + tamano_total//2 + center_size//2), 5)
    
        pygame.draw.line(pantalla, (0, 0, 0), 
                     (50 + tamano_total//2 + center_size//2, 50 + tamano_total//2 - center_size//2), 
                     (50 + tamano_total//2 - center_size//2, 50 + tamano_total//2 + center_size//2), 5)
        
        # Color de las carceles
        cell_size = tamano_total // 15  
        carcel_size = cell_size * 6  

        for equipo, (x, y) in enumerate(self.carceles):
            # Posición de la cárcel en la esquina correspondiente
            if equipo == 0:  # Rojo (superior izquierda)
                carcel_x, carcel_y = 50, 50
            elif equipo == 1:  # Azul (superior derecha)
                carcel_x, carcel_y = 50 + 9 * cell_size, 50
            elif equipo == 2:  # Verde (inferior derecha)
                carcel_x, carcel_y = 50 + 9 * cell_size, 50 + 9 * cell_size
            else:  # Amarillo (inferior izquierda)
                carcel_x, carcel_y = 50, 50 + 9 * cell_size

            pygame.draw.rect(pantalla, COLORES_EQUIPO[equipo], 
                     (carcel_x, carcel_y, carcel_size, carcel_size))
    
            pygame.draw.rect(pantalla, (0, 0, 0), 
                     (carcel_x, carcel_y, carcel_size, carcel_size), 3)

            self.carceles[equipo] = (carcel_x + carcel_size // 2, carcel_y + carcel_size // 2)
    
class Juego:
    def __init__(self, num_equipos=4, modo_desarrollador=False):
        # Configuración de la pantalla
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Parqués UN")
        
        self.tablero = Tablero()
        self.equipos = num_equipos  
        self.modo_desarrollador = modo_desarrollador
        self.turno_actual = 0
        self.dado1 = 0
        self.dado2 = 0
        self.movimientos_extra = 0
        self.pares_consecutivos = 0
        self.ultima_ficha_movida = None
        self.mensaje = ""
        self.seleccionando_dados = False
        self.seleccionando_ficha = False
        self.movimiento_obligatorio = False
        self.movimiento_captura = False
        self.movimiento_llegada = False
        self.dados_lanzados = False
        self.terminado = False
        
        self.fichas = []
        for e in range(NUM_EQUIPOS):
            fichas_equipo = []
            for n in range(NUM_FICHAS):
                fichas_equipo.append(Ficha(e, n))
            self.fichas.append(fichas_equipo)
        

    def reiniciar_juego(self):
        self.turno_actual = 0
        self.dado1 = 0
        self.dado2 = 0
        self.movimientos_extra = 0
        self.pares_consecutivos = 0
        self.ultima_ficha_movida = None
        self.mensaje = "¡Juego reiniciado! Pulse ESPACIO para lanzar los dados."
        self.seleccionando_dados = False
        self.seleccionando_ficha = False
        self.movimiento_obligatorio = False
        self.movimiento_captura = False
        self.movimiento_llegada = False
        self.dados_lanzados = False
        self.terminado = False
        
        # Reiniciar fichas
        for equipo in self.fichas:
            for ficha in equipo:
                ficha.reset()
    
    def lanzar_dados(self):
        if self.modo_desarrollador and self.seleccionando_dados:
            return  
        else:
            self.dado1 = random.randint(1, 6)
            self.dado2 = random.randint(1, 6)
            
        self.dados_lanzados = True
        
        if self.dado1 == self.dado2:
            self.pares_consecutivos += 1
            self.mensaje = f"¡Par de {self.dado1}s! Tienes otro turno."
            if self.pares_consecutivos == 3:
                self.mensaje = "¡Tres pares consecutivos! La última ficha vuelve a la cárcel."
                if self.ultima_ficha_movida:
                    self.ultima_ficha_movida.reset()
                self.pares_consecutivos = 0
                self.pasar_turno()
        else:
            self.pares_consecutivos = 0
    
    def pasar_turno(self):
        self.turno_actual = (self.turno_actual + 1) % self.equipos
        self.dados_lanzados = False
        self.seleccionando_ficha = False
        self.movimiento_obligatorio = False
        self.movimiento_captura = False
        self.movimiento_llegada = False
        self.movimientos_extra = 0
    
    def hay_ficha_en_casilla(self, posicion, excluir_equipo=None, excluir_ficha=None):
        for e, equipo in enumerate(self.fichas):
            if excluir_equipo is not None and e == excluir_equipo:
                continue
            for ficha in equipo:
                if ficha == excluir_ficha:
                    continue
                if ficha.esta_en_casilla_externa(posicion):
                    return ficha
        return None
    
    def contar_fichas_en_casilla(self, posicion):
        count = 0
        equipos = set()
        for e, equipo in enumerate(self.fichas):
            for ficha in equipo:
                if ficha.esta_en_casilla_externa(posicion):
                    count += 1
                    equipos.add(e)
        return count, equipos
    
    def hay_bloqueo_en_camino(self, ficha, pasos):
        if ficha.en_carcel or ficha.en_llegada:
            return False
    
        pos_actual = ficha.posicion_externa
        for paso in range(1, pasos):
            pos_siguiente = (pos_actual + paso) % NUM_CASILLAS_EXTERNAS
        
            # Verificar si hay bloqueo
            count, equipos = self.contar_fichas_en_casilla(pos_siguiente)
        
            # Bloqueo: dos fichas del mismo equipo o diferentes equipos en un seguro/salida
            if count >= 2 and (len(equipos) == 1 or 
                          (self.tablero.es_seguro(pos_siguiente) or self.tablero.es_salida(pos_siguiente))):
                return True
    
        return False
    
    def puede_mover_ficha(self, ficha, pasos):
        # No se puede mover ficha en llegada
        if ficha.en_llegada:
            return False
        
        # Si está en la cárcel, sólo puede salir con un 5
        if ficha.en_carcel:
            return pasos == 5
        
        # No puede moverse si hay bloqueo en el camino
        if self.hay_bloqueo_en_camino(ficha, pasos):
            return False
        
        pos_actual = ficha.posicion_externa
        pos_siguiente = (pos_actual + pasos) % NUM_CASILLAS_EXTERNAS
        
        equipo = ficha.equipo
        entrada_interna = self.tablero.inicios_casillas_internas[equipo]
        
        if (pos_actual <= entrada_interna < pos_actual + pasos) or \
        (pos_actual > entrada_interna and pos_actual + pasos >= NUM_CASILLAS_EXTERNAS + entrada_interna):
            # Necesita número exacto para entrar
            return pos_siguiente == entrada_interna
        
        return True
    
    def mover_ficha(self, ficha, pasos):
        captura = False
        llegada = False
        
        if ficha.en_carcel:
            if pasos == 5:  # Salir de la cárcel
                ficha.en_carcel = False
                ficha.posicion_externa = self.tablero.salidas[ficha.equipo]
                self.ultima_ficha_movida = ficha
        
                # Captura en la slalida
                otra_ficha = self.hay_ficha_en_casilla(ficha.posicion_externa, ficha.equipo, ficha)
                if otra_ficha and otra_ficha.equipo != ficha.equipo:
                    otra_ficha.reset()
                    captura = True
            return captura, llegada
        
        pos_actual = ficha.posicion_externa
        equipo = ficha.equipo
        entrada_interna = self.tablero.inicios_casillas_internas[equipo]
        
        # Verificar si puede entrar a la llegada
        if (pos_actual <= entrada_interna < pos_actual + pasos) or \
        (pos_actual > entrada_interna and pos_actual + pasos >= NUM_CASILLAS_EXTERNAS + entrada_interna):
            ficha.en_llegada = True
            ficha.posicion_externa = None
            ficha.posicion_interna = 0
            self.ultima_ficha_movida = ficha
            llegada = True
            return captura, llegada
        
        pos_siguiente = (pos_actual + pasos) % NUM_CASILLAS_EXTERNAS
        ficha.posicion_externa = pos_siguiente
        self.ultima_ficha_movida = ficha
        
        # Captura
        otra_ficha = self.hay_ficha_en_casilla(pos_siguiente, ficha.equipo, ficha)
        if otra_ficha and not (self.tablero.es_seguro(pos_siguiente) or self.tablero.es_salida(pos_siguiente)):
            otra_ficha.reset()
            captura = True
        
        return captura, llegada
    
    def verificar_ganador(self):
        for e, equipo in enumerate(self.fichas):
            todas_en_llegada = True
            for ficha in equipo:
                if not ficha.en_llegada:
                    todas_en_llegada = False
                    break
            if todas_en_llegada:
                return e
        return None
    
    def manejar_evento(self, evento):
        if evento.type == pygame.QUIT:
            return False
        
        if self.terminado:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
                self.reiniciar_juego()
            return True
        
        if evento.type == pygame.KEYDOWN:
            # Para lanzar dados con espacio
            if evento.key == pygame.K_SPACE and not self.dados_lanzados:
                if self.modo_desarrollador:
                    self.seleccionando_dados = True
                    self.mensaje = "Modo desarrollador: Ingrese valor para los dados (1-6)."
                else:
                    self.lanzar_dados()
                    self.seleccionar_movimiento()
            
            # Selección de dados en modo desarrollador
            elif self.seleccionando_dados and self.modo_desarrollador:
                if evento.unicode.isdigit():
                    valor = int(evento.unicode)
                    if 1 <= valor <= 6:
                        if self.dado1 == 0:
                            self.dado1 = valor
                            self.mensaje = f"Primer dado: {valor}. Ingrese valor para el segundo dado."
                        else:
                            self.dado2 = valor
                            self.seleccionando_dados = False
                            self.dados_lanzados = True
                            self.mensaje = f"Dados: {self.dado1} y {self.dado2}"
                            self.seleccionar_movimiento()
            
            # Reiniciar juego
            elif evento.key == pygame.K_r:
                self.reiniciar_juego()
            
            # Cambiar modo
            elif evento.key == pygame.K_m:
                self.modo_desarrollador = not self.modo_desarrollador
                self.mensaje = f"Modo {'desarrollador' if self.modo_desarrollador else 'normal'} activado."
        
        elif evento.type == pygame.MOUSEBUTTONDOWN and self.seleccionando_ficha:
            pos_mouse = pygame.mouse.get_pos()
            self.seleccionar_ficha_por_posicion(pos_mouse)
        
        return True
    
    def seleccionar_movimiento(self):
        #Movimientos extra
        if self.movimiento_captura:
            self.seleccionando_ficha = True
            self.mensaje = f"Seleccione ficha para mover 20 casillas (captura)."
            return
        
        if self.movimiento_llegada:
            self.seleccionando_ficha = True
            self.mensaje = f"Seleccione ficha para mover 10 casillas (llegada)."
            return
        
        puede_mover = False
        
        # Regla 1: Es obligatorio sacar una ficha de la cárcel cuando un 5 lo permite
        if self.dado1 == 5 or self.dado2 == 5:
            for ficha in self.fichas[self.turno_actual]:
                if ficha.en_carcel:
                    salida = self.tablero.salidas[self.turno_actual]
                    count, _ = self.contar_fichas_en_casilla(salida)
                    
                    if count < 2:
                        captura, llegada = self.mover_ficha(ficha, 5)
                        puede_mover = True
                        
                        if captura:
                            self.movimiento_captura = True
                            self.mensaje = "¡Captura! Seleccione una ficha para mover 20 casillas."
                        elif llegada:
                            self.movimiento_llegada = True
                            self.mensaje = "¡Llegada! Seleccione una ficha para mover 10 casillas."
                        else:
                            otro_dado = self.dado2 if self.dado1 == 5 else self.dado1
                            if otro_dado > 0:
                                self.seleccionando_ficha = True
                                self.mensaje = f"Seleccione ficha para mover {otro_dado} casillas."
                            else:
                                self.pasar_turno()
                        
                        return
        
        self.seleccionando_ficha = True
        self.mensaje = f"Seleccione ficha para mover {self.dado1} o {self.dado2} casillas."
    
    def seleccionar_ficha_por_posicion(self, pos_mouse):
        x, y = pos_mouse
        distancia_minima = float('inf')
        ficha_seleccionada = None
        pasos_seleccionados = 0
        
        # Verificar si hay movimientos extra
        if self.movimiento_captura:
            pasos = 20
        elif self.movimiento_llegada:
            pasos = 10
        else:
            pasos = self.dado1  
        
        for ficha in self.fichas[self.turno_actual]:
            if ficha.en_carcel:
                cx, cy = self.tablero.carceles[ficha.equipo]
                # Distribucion de las fichas dentro de la cárcel
                offset_x = (ficha.numero % 2) * 30 - 15
                offset_y = (ficha.numero // 2) * 30 - 15
                pos_x, pos_y = cx + offset_x, cy + offset_y
            elif ficha.en_llegada:
                pos_x, pos_y = self.tablero.casillas_internas[ficha.equipo][ficha.posicion_interna]
            else:
                pos_x, pos_y = self.tablero.casillas_externas[ficha.posicion_externa]
            
            dist = ((x - pos_x) ** 2 + (y - pos_y) ** 2) ** 0.5
            
            if dist < distancia_minima and dist < 30:
                puede_mover = False
                
                if self.movimiento_captura:
                    puede_mover = self.puede_mover_ficha(ficha, 20)
                    pasos_seleccionados = 20
                elif self.movimiento_llegada:
                    puede_mover = self.puede_mover_ficha(ficha, 10)
                    pasos_seleccionados = 10
                else:
                    # Probar con el primer dado
                    if self.puede_mover_ficha(ficha, self.dado1):
                        puede_mover = True
                        pasos_seleccionados = self.dado1
                    # Probar con el segundo dado si el primero no sirve
                    elif self.puede_mover_ficha(ficha, self.dado2):
                        puede_mover = True
                        pasos_seleccionados = self.dado2
                    # Probar con la suma de los dados
                    elif self.puede_mover_ficha(ficha, self.dado1 + self.dado2):
                        puede_mover = True
                        pasos_seleccionados = self.dado1 + self.dado2
                
                if puede_mover:
                    distancia_minima = dist
                    ficha_seleccionada = ficha
        
        # Mover la ficha
        if ficha_seleccionada:
            captura, llegada = self.mover_ficha(ficha_seleccionada, pasos_seleccionados)
            
            if self.movimiento_captura:
                self.movimiento_captura = False
                self.pasar_turno()
            elif self.movimiento_llegada:
                self.movimiento_llegada = False
                self.pasar_turno()
            else:
                if captura:
                    self.movimiento_captura = True
                    self.mensaje = "¡Captura! Seleccione una ficha para mover 20 casillas."
                    return
                elif llegada:
                    self.movimiento_llegada = True
                    self.mensaje = "¡Llegada! Seleccione una ficha para mover 10 casillas."
                    return
                else:
                    # Si fue par, puede lanzar de nuevo
                    if self.dado1 == self.dado2:
                        self.dados_lanzados = False
                        self.mensaje = "¡Par! Presione ESPACIO para lanzar de nuevo."
                    else:
                        self.pasar_turno()
                        self.mensaje = f"Turno del equipo {NOMBRES_EQUIPO[self.turno_actual]}. Presione ESPACIO para lanzar dados."
        else:
            self.mensaje = "No hay movimientos posibles. Presione ESPACIO para continuar."
            self.pasar_turno()
        
        # Verificar ganador
        ganador = self.verificar_ganador()
        if ganador is not None:
            self.mensaje = f"¡El equipo {NOMBRES_EQUIPO[ganador]} ha ganado! Presione R para reiniciar."
            self.terminado = True

    def dibujar_dados(self):
        # Definir panel de los dados
        panel_x, panel_y = ANCHO - 150, 20  
        panel_ancho, panel_alto = 120, 140  

        pygame.draw.rect(self.pantalla, (220, 220, 220), (panel_x, panel_y, panel_ancho, panel_alto), 0, 10)
        pygame.draw.rect(self.pantalla, (0, 0, 0), (panel_x, panel_y, panel_ancho, panel_alto), 2, 10)

        texto_turno = pygame.font.SysFont('Arial', 18).render(f"{NOMBRES_EQUIPO[self.turno_actual]}", True, COLORES_EQUIPO[self.turno_actual])
        self.pantalla.blit(texto_turno, (panel_x + 30, panel_y + 10))

        dado_tamano = 40
        espaciado = 10

        pygame.draw.rect(self.pantalla, (255, 255, 255), (panel_x + espaciado, panel_y + 40, dado_tamano, dado_tamano), 0, 5)
        pygame.draw.rect(self.pantalla, (0, 0, 0), (panel_x + espaciado, panel_y + 40, dado_tamano, dado_tamano), 2, 5)
        texto_dado1 = pygame.font.SysFont('Arial', 22).render(str(self.dado1), True, (0, 0, 0))
        self.pantalla.blit(texto_dado1, (panel_x + espaciado + 12, panel_y + 50))

        pygame.draw.rect(self.pantalla, (255, 255, 255), (panel_x + espaciado + dado_tamano + espaciado, panel_y + 40, dado_tamano, dado_tamano), 0, 5)
        pygame.draw.rect(self.pantalla, (0, 0, 0), (panel_x + espaciado + dado_tamano + espaciado, panel_y + 40, dado_tamano, dado_tamano), 2, 5)
        texto_dado2 = pygame.font.SysFont('Arial', 22).render(str(self.dado2), True, (0, 0, 0))
        self.pantalla.blit(texto_dado2, (panel_x + espaciado + dado_tamano + espaciado + 12, panel_y + 50))

    def dibujar_mensaje(self):
        pygame.draw.rect(self.pantalla, (220, 220, 220), (20, ALTO - 70, ANCHO - 40, 50), 0, 10)
        pygame.draw.rect(self.pantalla, (0, 0, 0), (20, ALTO - 70, ANCHO - 40, 50), 2, 10)
        
        texto_mensaje = FUENTE_MEDIA.render(self.mensaje, True, (0, 0, 0))
        self.pantalla.blit(texto_mensaje, (40, ALTO - 55))
    
    def dibujar_fichas(self):
        # Dibujar todas las fichas
        for e, equipo in enumerate(self.fichas):
            for i, ficha in enumerate(equipo):
                if ficha.en_carcel:
                    cx, cy = self.tablero.carceles[e]
                    separacion = 35  
                    posiciones_carcel = [
                        (cx - separacion, cy - separacion), (cx + separacion, cy - separacion),
                        (cx - separacion, cy + separacion), (cx + separacion, cy + separacion)
                    ]
                    x, y = posiciones_carcel[i]
                elif ficha.en_llegada:
                    x, y = self.tablero.casillas_internas[e][ficha.posicion_interna]
                else:
                    x, y = self.tablero.casillas_externas[ficha.posicion_externa]
                
                # Dibujar ficha
                pygame.draw.circle(self.pantalla, COLORES_EQUIPO[e], (x, y), ficha.radio)
                pygame.draw.circle(self.pantalla, (0, 0, 0), (x, y), ficha.radio, 2)
                
                # Mostrar número de ficha
                texto_num = FUENTE_PEQUEÑA.render(str(i+1), True, (255, 255, 255))
                self.pantalla.blit(texto_num, (x - 5, y - 8))
    
    def actualizar(self):
        # Dibujar tablero
        self.tablero.dibujar(self.pantalla)
        
        # Dibujar fichas
        self.dibujar_fichas()
        
        # Dibujar dados e información del turno
        self.dibujar_dados()
        
        # Dibujar mensaje
        self.dibujar_mensaje()
        
        # Actualizar pantalla
        pygame.display.flip()

# Función principal
def main():
    juego = Juego(modo_desarrollador=False)
    juego.mensaje = "¡Bienvenido a Parqués UN! Presione ESPACIO para lanzar dados."
    
    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if not juego.manejar_evento(evento):
                corriendo = False
        
        juego.actualizar()
    
    pygame.quit()

if __name__ == "__main__":
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    main()