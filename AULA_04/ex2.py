import math
import pygame

SCALE = 40.0            
WIDTH, HEIGHT = 1000, 750
L = 2.0                  
PHI_MAX = math.radians(30.0)
V_MAX = 2.0
V_STEP = 0.05
PHI_STEP = math.radians(1.0)
DT = 0.02

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
BLUE = (40, 90, 200)
GREEN = (30, 150, 60)
GRAY = (190, 190, 190)
RED = (200, 40, 40)

def to_screen(x, y, origin):
    return origin[0] + x * SCALE, origin[1] - y * SCALE

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Lab2 - Ackermann vs Diferencial")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 18)

    origin = (WIDTH // 2, HEIGHT // 2)

    v = 0.0
    phi = 0.0         
    modo_ackermann = True

    x, y, theta = 0.0, 0.0, 0.0
    trilha = [(x, y)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    x, y, theta = 0.0, 0.0, 0.0
                    trilha = [(x, y)]
                elif event.key == pygame.K_d:
                    modo_ackermann = not modo_ackermann

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            v = min(V_MAX, v + V_STEP)
        if keys[pygame.K_DOWN]:
            v = max(-V_MAX, v - V_STEP)
        if keys[pygame.K_LEFT]:
            phi = min(PHI_MAX, phi + PHI_STEP) if modo_ackermann else phi
        if keys[pygame.K_RIGHT]:
            phi = max(-PHI_MAX, phi - PHI_STEP) if modo_ackermann else phi

        if modo_ackermann:
            w = (v / L) * math.tan(phi)
            if abs(phi) > 1e-6:
                raio = L / math.tan(phi)   
            else:
                raio = math.inf
        else:
            w = phi * 2.0  
            raio = 0.0 if v == 0.0 else (v / w if abs(w) > 1e-6 else math.inf)

        x += v * math.cos(theta) * DT
        y += v * math.sin(theta) * DT
        theta += w * DT
        trilha.append((x, y))
        if len(trilha) > 4000:
            trilha.pop(0)

        screen.fill(WHITE)
        for gx in range(0, WIDTH, 40):
            pygame.draw.line(screen, GRAY, (gx, 0), (gx, HEIGHT), 1)
        for gy in range(0, HEIGHT, 40):
            pygame.draw.line(screen, GRAY, (0, gy), (WIDTH, gy), 1)

        if len(trilha) > 1:
            pts = [to_screen(px, py, origin) for px, py in trilha]
            cor = BLUE if modo_ackermann else GREEN
            pygame.draw.lines(screen, cor, False, pts, 2)

        rx, ry = to_screen(x, y, origin)
        pygame.draw.circle(screen, BLACK, (int(rx), int(ry)), 9)
        hx = rx + 22 * math.cos(-theta)
        hy = ry + 22 * math.sin(-theta)
        pygame.draw.line(screen, BLACK, (rx, ry), (hx, hy), 3)

        raio_txt = "infinito (reto)" if math.isinf(raio) else f"{raio:.2f} m"
        info = [
            f"Modo: {'ACKERMANN' if modo_ackermann else 'DIFERENCIAL'}  (D para alternar)",
            f"v = {v:.2f} m/s   phi = {math.degrees(phi):.1f} deg (limite +-30)",
            f"w calculado = {w:.4f} rad/s",
            f"Raio de curvatura R = {raio_txt}",
            "Ackermann NUNCA zera o raio (R->inf so quando phi->0, mas R>0 sempre que phi!=0).",
            "Diferencial consegue R=0 (giro sobre o proprio eixo).",
            "Setas: v (cima/baixo), phi (esq/dir) | R: reset | D: alternar modo",
        ]
        for i, line in enumerate(info):
            txt = font.render(line, True, BLACK if i < 4 else RED if i < 6 else BLACK)
            screen.blit(txt, (10, 10 + i * 22))

        pygame.display.flip()
        clock.tick(1.0 / DT)

    pygame.quit()

if __name__ == "__main__":
    main()