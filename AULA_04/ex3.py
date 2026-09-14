import math
import numpy as np
import pygame

WIDTH, HEIGHT = 1000, 700
ROBOT_POS = (250, 350)
NUM_FEIXES = 7
FOV = math.pi  
RANGE_MAX = 200.0
RANGE_MIN_VALID = 10.0
NOISE_STD = 5.0

OBSTACLE_CENTER = (650, 350)
OBSTACLE_RADIUS = 80

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (170, 170, 170)
RED = (200, 40, 40)
BLUE = (40, 90, 200)
GREEN = (30, 150, 60)

def distancia_real_feixe(origem, angulo_global, obstaculo_centro, obstaculo_raio, alcance_max):
    ox, oy = origem
    cx, cy = obstaculo_centro
    dx, dy = math.cos(angulo_global), math.sin(angulo_global)

    fx, fy = ox - cx, oy - cy
    a = dx * dx + dy * dy
    b = 2 * (fx * dx + fy * dy)
    c = fx * fx + fy * fy - obstaculo_raio * obstaculo_raio
    disc = b * b - 4 * a * c
    if disc < 0:
        return alcance_max
    disc_sqrt = math.sqrt(disc)
    t1 = (-b - disc_sqrt) / (2 * a)
    t2 = (-b + disc_sqrt) / (2 * a)
    candidatos = [t for t in (t1, t2) if t >= 0]
    if not candidatos:
        return alcance_max
    d = min(candidatos)
    return min(d, alcance_max)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Lab3 - Filtro de Alcance e Ruido")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 16)

    angulos_locais = [-FOV / 2 + i * (FOV / (NUM_FEIXES - 1)) for i in range(NUM_FEIXES)]
    ultimo_filtrado = [RANGE_MAX] * NUM_FEIXES
    theta_robo = 0.0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            theta_robo -= 0.02
        if keys[pygame.K_RIGHT]:
            theta_robo += 0.02

        leituras_brutas = []
        leituras_filtradas = []
        pontos_feixe = []

        for i, ang_local in enumerate(angulos_locais):
            ang_global = theta_robo + ang_local
            d_real = distancia_real_feixe(ROBOT_POS, ang_global, OBSTACLE_CENTER, OBSTACLE_RADIUS, RANGE_MAX)
            d_ruido = d_real + np.random.normal(0, NOISE_STD)
            d_ruido = max(0.0, d_ruido)

            if d_ruido < RANGE_MIN_VALID:
                d_filtrado = ultimo_filtrado[i]     
            elif d_ruido > RANGE_MAX:
                d_filtrado = RANGE_MAX               
            else:
                d_filtrado = d_ruido
            ultimo_filtrado[i] = d_filtrado

            leituras_brutas.append(d_ruido)
            leituras_filtradas.append(d_filtrado)

            end_x = ROBOT_POS[0] + d_filtrado * math.cos(ang_global)
            end_y = ROBOT_POS[1] + d_filtrado * math.sin(ang_global)
            pontos_feixe.append((end_x, end_y))

        screen.fill(WHITE)
        pygame.draw.circle(screen, GRAY, OBSTACLE_CENTER, OBSTACLE_RADIUS)
        pygame.draw.circle(screen, BLACK, ROBOT_POS, 10)

        for i, (end_x, end_y) in enumerate(pontos_feixe):
            pygame.draw.line(screen, BLUE, ROBOT_POS, (end_x, end_y), 1)
            pygame.draw.circle(screen, RED, (int(end_x), int(end_y)), 4)

        painel_x = 20
        titulo = font.render("Feixe |  Bruto (ruido)  |  Filtrado", True, BLACK)
        screen.blit(titulo, (painel_x, 20))
        for i in range(NUM_FEIXES):
            linha = (f"{i+1:>2}    |   {leituras_brutas[i]:7.2f} px    |   {leituras_filtradas[i]:7.2f} px")
            cor = GREEN if RANGE_MIN_VALID <= leituras_brutas[i] <= RANGE_MAX else RED
            txt = font.render(linha, True, cor)
            screen.blit(txt, (painel_x, 45 + i * 20))

        info = font.render("Setas esq/dir giram o robo. Vermelho = feixe fora do range valido.", True, BLACK)
        screen.blit(info, (painel_x, HEIGHT - 30))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()