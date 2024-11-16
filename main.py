import pygame
import numpy as np
import matplotlib.pyplot as plt

# ------------------------ Constantes ------------------------ #

# Dimensiones de la pantalla
ANCHO_PANTALLA = 700
ALTO_PANTALLA = 700

# Número de personas en la simulación
N = 200

# Parámetros del modelo SIR
RADIO_INFECCION = 5        
TASA_RECUPERACION = 0.001

# Colores para Pygame
COLOR_FONDO = (200, 200, 200)
COLOR_SUSCEPTIBLE = (0, 0, 200)
COLOR_INFECTADO = (200, 0, 0)
COLOR_RECUPERADO = (100, 100, 100)

# Colores para Matplotlib
COLOR_GRAFICA_SUSCEPTIBLE = tuple(c / 255 for c in COLOR_SUSCEPTIBLE)
COLOR_GRAFICA_INFECTADO = tuple(c / 255 for c in COLOR_INFECTADO)
COLOR_GRAFICA_RECUPERADO = tuple(c / 255 for c in COLOR_RECUPERADO)

# Parámetros de movimiento de la persona
ATRACCION_CENTRO = 0.3
VELOCIDAD_MEDIA = 1.5
VELOCIDAD_STD = 0.5
PERSISTENCIA_VELOCIDAD = 0.9

# ---------------------------------------------------------- #

class Persona:
    def __init__(self, x, y):
        # Estado:
        # 0 - Susceptible
        # 1 - Infectado
        # 2 - Recuperado

        self.pos = pygame.math.Vector2(x, y)
        self.ultima_vel = pygame.math.Vector2(0, 0)
        self.estado = 0

    def dibujar(self, pantalla):
        if self.estado == 0:
            color = COLOR_SUSCEPTIBLE
        elif self.estado == 1:
            color = COLOR_INFECTADO
        else:
            color = COLOR_RECUPERADO

        pygame.draw.circle(pantalla, color, (int(self.pos.x), int(self.pos.y)), 5)

    def mover(self):
        # Mover hacia el centro con algo de aleatoriedad
        centro = pygame.math.Vector2(ANCHO_PANTALLA / 2, ALTO_PANTALLA / 2)
        direccion_al_centro = (centro - self.pos).normalize()

        # Actualizar velocidad con persistencia
        if self.ultima_vel.x != 0 and np.random.uniform(0, 1) < PERSISTENCIA_VELOCIDAD:
            vel_x = self.ultima_vel.x
        else:
            vel_x = np.random.normal(VELOCIDAD_MEDIA, VELOCIDAD_STD) * np.random.choice((1, -1, 0))

        if self.ultima_vel.y != 0 and np.random.uniform(0, 1) < PERSISTENCIA_VELOCIDAD:
            vel_y = self.ultima_vel.y
        else:
            vel_y = np.random.normal(VELOCIDAD_MEDIA, VELOCIDAD_STD) * np.random.choice((1, -1, 0))

        self.ultima_vel = pygame.math.Vector2(vel_x, vel_y)
        self.pos += self.ultima_vel + direccion_al_centro * ATRACCION_CENTRO

        # Mantener a la persona dentro de los límites
        self.pos.x = max(0, min(self.pos.x, ANCHO_PANTALLA))
        self.pos.y = max(0, min(self.pos.y, ALTO_PANTALLA))


class Ciudad:
    def __init__(self, n):
        self.personas = []
        self.n = n

        self.S = n
        self.I = 0
        self.R = 0

        self.radio = RADIO_INFECCION
        self.tasa_recuperacion = TASA_RECUPERACION

    def generar_personas(self):
        X = np.random.normal(ANCHO_PANTALLA / 2, ANCHO_PANTALLA / 6, self.n)
        Y = np.random.normal(ALTO_PANTALLA / 2, ALTO_PANTALLA / 6, self.n)

        for i in range(self.n):
            x = X[i]
            y = Y[i]

            # Mantener a las personas dentro de los límites
            x = np.clip(x, 10, ANCHO_PANTALLA - 10)
            y = np.clip(y, 10, ALTO_PANTALLA - 10)

            persona = Persona(x, y)
            self.personas.append(persona)

        # Infectar a una persona al azar para comenzar
        infectado_inicial = np.random.choice(self.personas)
        infectado_inicial.estado = 1
        self.S -= 1
        self.I += 1

    def actividad(self, pantalla):
        for persona in self.personas:
            persona.dibujar(pantalla)
            persona.mover()

    def infectar(self):
        personas_infectadas = [p for p in self.personas if p.estado == 1]
        personas_susceptibles = [p for p in self.personas if p.estado == 0]

        for infectado in personas_infectadas:
            for susceptible in personas_susceptibles:
                if distancia_euclidiana(infectado, susceptible) < self.radio:
                    susceptible.estado = 1
                    self.S -= 1
                    self.I += 1

    def recuperar(self):
        for persona in self.personas:
            if persona.estado == 1 and np.random.uniform(0, 1) < self.tasa_recuperacion:
                persona.estado = 2
                self.I -= 1
                self.R += 1


def distancia_euclidiana(p1, p2):
    return p1.pos.distance_to(p2.pos)


def graficar_SIR(historial_S, historial_I, historial_R):
    pasos_tiempo = range(len(historial_S))
    porcentaje_S = [s / N * 100 for s in historial_S]
    porcentaje_I = [i / N * 100 for i in historial_I]
    porcentaje_R = [r / N * 100 for r in historial_R]

    plt.figure(figsize=(10, 6))
    plt.stackplot(pasos_tiempo, porcentaje_S, porcentaje_I, porcentaje_R,
                  labels=['Susceptibles', 'Infectados', 'Recuperados'],
                  colors=[COLOR_GRAFICA_SUSCEPTIBLE, COLOR_GRAFICA_INFECTADO, COLOR_GRAFICA_RECUPERADO])

    plt.xlabel('Pasos de Tiempo')
    plt.ylabel('Porcentaje de la Población')
    plt.title('Simulación del Modelo SIR a lo Largo del Tiempo')
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.show()


def main():
    pygame.init()

    ciudad = Ciudad(N)
    ciudad.generar_personas()

    pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
    pygame.display.set_caption("Simulación del Modelo SIR")

    reloj = pygame.time.Clock()

    # Listas para almacenar S, I, R a lo largo del tiempo
    historial_S = []
    historial_I = []
    historial_R = []

    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

        pantalla.fill(COLOR_FONDO)

        ciudad.actividad(pantalla)
        ciudad.infectar()
        ciudad.recuperar()

        # Registrar el estado actual de S, I, R
        historial_S.append(ciudad.S)
        historial_I.append(ciudad.I)
        historial_R.append(ciudad.R)

        pygame.display.flip()
        reloj.tick(60)  # Limitar a 60 FPS

    pygame.quit()

    # Graficar los datos SIR
    graficar_SIR(historial_S, historial_I, historial_R)


if __name__ == "__main__":
    main()
