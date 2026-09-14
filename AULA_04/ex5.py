import math
import pygame

WIDTH, HEIGHT = 1000, 700
CORREDOR_Y_TOPO = 200
CORREDOR_LARGURA = 260
CORREDOR_Y_PAREDE_SUP = CORREDOR_Y_TOPO
CORREDOR_Y_PAREDE_INF = CORREDOR_Y_TOPO + CORREDOR_LARGURA

KP = 0.01
V_CONST = 40.0
DT = 0.02

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (120, 120, 120)
BLUE = (40, 90, 200)
RED = (200, 40, 40)
GREEN = (30, 150, 60)

def medir_lateral(pos_y, parede_sup, parede_inf):
    d_esq = pos_y - parede_sup
    d_dir = parede_inf - pos_y
    return d_esq, d_dir

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Ex5 - Centralizacao em corredor (P-control)")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 18)

    x, y, theta = 50.0, CORREDOR_Y_TOPO + 60.0, 0.0
    trilha = [(x, y)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                x, y, theta = 50.0, CORREDOR_Y_TOPO + 60.0, 0.0
                trilha = [(x, y)]

        d_esq, d_dir = medir_lateral(y, CORREDOR_Y_PAREDE_SUP, CORREDOR_Y_PAREDE_INF)
        erro = d_esq - d_dir
        w = KP * erro

        x += V_CONST * math.cos(theta) * DT
        y += V_CONST * math.sin(theta) * DT
        theta += w * DT

        if x > WIDTH - 30:
            x = 30.0

        trilha.append((x, y))
        if len(trilha) > 4000:
            trilha.pop(0)

        screen.fill(WHITE)
        pygame.draw.line(screen, GRAY, (0, CORREDOR_Y_PAREDE_SUP), (WIDTH, CORREDOR_Y_PAREDE_SUP), 4)
        pygame.draw.line(screen, GRAY, (0, CORREDOR_Y_PAREDE_INF), (WIDTH, CORREDOR_Y_PAREDE_INF), 4)
        centro_y = (CORREDOR_Y_PAREDE_SUP + CORREDOR_Y_PAREDE_INF) / 2
        pygame.draw.line(screen, GREEN, (0, centro_y), (WIDTH, centro_y), 1)

        if len(trilha) > 1:
            pygame.draw.lines(screen, BLUE, False, trilha, 2)

        pygame.draw.circle(screen, BLACK, (int(x), int(y)), 9)
        pygame.draw.line(screen, RED, (x, y), (x, CORREDOR_Y_PAREDE_SUP), 1)
        pygame.draw.line(screen, RED, (x, y), (x, CORREDOR_Y_PAREDE_INF), 1)

        info = [
            f"d_esq = {d_esq:6.1f} px   d_dir = {d_dir:6.1f} px   erro e = {erro:6.1f} px",
            f"w = Kp * e = {w:.4f} rad/s   v = {V_CONST:.1f} px/s (constante)",
            "R: reinicia desalinhado | linha verde = centro do corredor",
        ]
        for i, line in enumerate(info):
            txt = font.render(line, True, BLACK)
            screen.blit(txt, (10, 10 + i * 22))

        pygame.display.flip()
        clock.tick(1.0 / DT)

    pygame.quit()

if __name__ == "__main__":
    main()