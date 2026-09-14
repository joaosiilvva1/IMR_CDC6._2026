import math
import pygame

SCALE = 100.0          
DT = 0.02              
WIDTH, HEIGHT = 900, 700
ORIGIN = (150, 550)    

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
BLUE = (40, 90, 200)
RED = (200, 40, 40)
GRAY = (180, 180, 180)

SEGMENTS = [
    (4.0, 0.5, 0.0),
    (2.0, 0.0, math.pi / 4.0),
    (3.0, 0.4, 0.0),
]

def pose_teorica_segmento(x0, y0, theta0, v, w, t):
    if abs(w) < 1e-9:
        x = x0 + v * math.cos(theta0) * t
        y = y0 + v * math.sin(theta0) * t
        theta = theta0
    else:
        theta = theta0 + w * t
        x = x0 + (v / w) * (math.sin(theta) - math.sin(theta0))
        y = y0 - (v / w) * (math.cos(theta) - math.cos(theta0))
    return x, y, theta

def calcular_pose_teorica_final(segments):
    x, y, theta = 0.0, 0.0, 0.0
    trajeto = [(x, y, theta)]
    for t, v, w in segments:
        x, y, theta = pose_teorica_segmento(x, y, theta, v, w, t)
        trajeto.append((x, y, theta))
    return (x, y, theta), trajeto

def to_screen(x, y):
    return ORIGIN[0] + x * SCALE, ORIGIN[1] - y * SCALE

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Lab1 - Pose em malha aberta (Cinematica Diferencial)")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 18)

    pose_teorica_final, marcos_teoricos = calcular_pose_teorica_final(SEGMENTS)

    x, y, theta = 0.0, 0.0, 0.0
    caminho_simulado = [(x, y)]

    seg_idx = 0
    t_no_segmento = 0.0
    simulando = True
    pose_simulada_final = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if simulando:
            duracao, v, w = SEGMENTS[seg_idx]
            x += v * math.cos(theta) * DT
            y += v * math.sin(theta) * DT
            theta += w * DT
            t_no_segmento += DT
            caminho_simulado.append((x, y))

            if t_no_segmento >= duracao:
                seg_idx += 1
                t_no_segmento = 0.0
                if seg_idx >= len(SEGMENTS):
                    simulando = False
                    pose_simulada_final = (x, y, theta)
                    print("=" * 60)
                    print(f"Pose TEORICA final : x={pose_teorica_final[0]:.4f} m, "
                          f"y={pose_teorica_final[1]:.4f} m, "
                          f"theta={math.degrees(pose_teorica_final[2]):.2f} deg")
                    print(f"Pose SIMULADA final: x={pose_simulada_final[0]:.4f} m, "
                          f"y={pose_simulada_final[1]:.4f} m, "
                          f"theta={math.degrees(pose_simulada_final[2]):.2f} deg")
                    erro = math.hypot(pose_teorica_final[0] - pose_simulada_final[0],
                                       pose_teorica_final[1] - pose_simulada_final[1])
                    print(f"Erro de posicao: {erro * 1000:.3f} mm")
                    print("=" * 60)

        screen.fill(WHITE)

        for gx in range(0, WIDTH, 50):
            pygame.draw.line(screen, GRAY, (gx, 0), (gx, HEIGHT), 1)
        for gy in range(0, HEIGHT, 50):
            pygame.draw.line(screen, GRAY, (0, gy), (WIDTH, gy), 1)

        if len(caminho_simulado) > 1:
            pts = [to_screen(px, py) for px, py in caminho_simulado]
            pygame.draw.lines(screen, BLUE, False, pts, 2)

        for mx, my, mtheta in marcos_teoricos:
            sx, sy = to_screen(mx, my)
            pygame.draw.circle(screen, RED, (int(sx), int(sy)), 6, 2)

        rx, ry = to_screen(x, y)
        pygame.draw.circle(screen, BLACK, (int(rx), int(ry)), 10)
        heading_len = 25
        hx = rx + heading_len * math.cos(-theta)
        hy = ry + heading_len * math.sin(-theta)
        pygame.draw.line(screen, BLACK, (rx, ry), (hx, hy), 3)

        info = [
            f"Segmento: {min(seg_idx + 1, len(SEGMENTS))}/{len(SEGMENTS)}"
            + (" (concluido)" if not simulando else ""),
            f"Pose atual (sim): x={x:.3f} y={y:.3f} theta={math.degrees(theta):.1f} deg",
            f"Pose teorica final: x={pose_teorica_final[0]:.3f} y={pose_teorica_final[1]:.3f} "
            f"theta={math.degrees(pose_teorica_final[2]):.1f} deg",
        ]
        for i, line in enumerate(info):
            txt = font.render(line, True, BLACK)
            screen.blit(txt, (10, 10 + i * 22))

        pygame.display.flip()
        clock.tick(1.0 / DT)

    pygame.quit()

if __name__ == "__main__":
    main()