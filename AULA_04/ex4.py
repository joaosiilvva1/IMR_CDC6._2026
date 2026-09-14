import math
import pygame

WIDTH, HEIGHT = 1000, 700
V0 = 20.0
ALPHA = 60.0
D_MAX = 200.0
EIXO_RODAS = 30.0
DT = 0.02

OBSTACLE_CENTER = (800, 200)
OBSTACLE_RADIUS = 40

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (170, 170, 170)
BLUE = (40, 90, 200)
GREEN = (30, 150, 60)
RED = (200, 40, 40)

def distancia_sensor(origem, angulo_global, obstaculo_centro, obstaculo_raio, d_max):
    ox, oy = origem
    cx, cy = obstaculo_centro
    dx, dy = math.cos(angulo_global), math.sin(angulo_global)
    fx, fy = ox - cx, oy - cy
    a = dx * dx + dy * dy
    b = 2 * (fx * dx + fy * dy)
    c = fx * fx + fy * fy - obstaculo_raio * obstaculo_raio
    disc = b * b - 4 * a * c
    if disc < 0:
        return d_max
    disc_sqrt = math.sqrt(disc)
    t1 = (-b - disc_sqrt) / (2 * a)
    t2 = (-b + disc_sqrt) / (2 * a)
    candidatos = [t for t in (t1, t2) if t >= 0]
    if not candidatos:
        return d_max
    return min(min(candidatos), d_max)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Lab4 - Braitenberg conexao direta (atracao)")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 18)

    x, y, theta = 150.0, 500.0, -0.3 
    trilha = [(x, y)]

    ANG_SENSOR_ESQ = math.radians(30)   
    ANG_SENSOR_DIR = math.radians(-30)  

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        d_esq = distancia_sensor((x, y), theta + ANG_SENSOR_ESQ, OBSTACLE_CENTER, OBSTACLE_RADIUS, D_MAX)
        d_dir = distancia_sensor((x, y), theta + ANG_SENSOR_DIR, OBSTACLE_CENTER, OBSTACLE_RADIUS, D_MAX)

        vL = V0 + ALPHA * (1.0 - d_esq / D_MAX)
        vR = V0 + ALPHA * (1.0 - d_dir / D_MAX)

        v = (vL + vR) / 2.0
        w = (vR - vL) / EIXO_RODAS

        x += v * math.cos(theta) * DT
        y += v * math.sin(theta) * DT
        theta += w * DT
        trilha.append((x, y))
        if len(trilha) > 3000:
            trilha.pop(0)

        screen.fill(WHITE)
        pygame.draw.circle(screen, GRAY, OBSTACLE_CENTER, OBSTACLE_RADIUS)

        if len(trilha) > 1:
            pygame.draw.lines(screen, BLUE, False, trilha, 2)

        for ang, d, cor in ((theta + ANG_SENSOR_ESQ, d_esq, GREEN),
                             (theta + ANG_SENSOR_DIR, d_dir, RED)):
            ex = x + d * math.cos(ang)
            ey = y + d * math.sin(ang)
            pygame.draw.line(screen, cor, (x, y), (ex, ey), 1)

        pygame.draw.circle(screen, BLACK, (int(x), int(y)), 9)
        hx = x + 20 * math.cos(theta)
        hy = y + 20 * math.sin(theta)
        pygame.draw.line(screen, BLACK, (x, y), (hx, hy), 3)

        info = [
            f"d_esq (sensor E) = {d_esq:6.1f} px    vL = {vL:6.2f} px/s",
            f"d_dir (sensor D) = {d_dir:6.1f} px    vR = {vR:6.2f} px/s",
            "Conexao DIRETA: obstaculo a direita -> vR sobe -> robo VIRA em direcao a ele.",
        ]
        for i, line in enumerate(info):
            txt = font.render(line, True, BLACK)
            screen.blit(txt, (10, 10 + i * 22))

        pygame.display.flip()
        clock.tick(1.0 / DT)

    pygame.quit()

if __name__ == "__main__":
    main()