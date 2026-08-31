import pygame
import math
import numpy as np

LARGURA_TELA = 800
ALTURA_TELA = 600
FPS = 60
COR_FUNDO = (30, 30, 30)
COR_ROBO = (0, 180, 255)
COR_DIRECAO = (255, 50, 50)
COR_TRAJETORIA = (100, 200, 100)
COR_ALVO = (255, 220, 0)

VEL_LINEAR = 100.0        # px/s
VEL_ANGULAR = math.pi / 2  # rad/s
TEMPO_RETO = 2.0           # s
TEMPO_GIRO = 1.0           # s
REPETICOES = 4


class DiffDriveRobot:
    def __init__(self, x, y, theta=0.0, wheelbase=30.0, radius=15.0):
        self.x = float(x)
        self.y = float(y)
        self.theta = float(theta)

        self.L = float(wheelbase)
        self.radius = float(radius)

        self.v = 0.0
        self.omega = 0.0

        self.history = []

    def set_direct_velocity(self, v, omega):
        self.v = v
        self.omega = omega

    def update(self, dt):
        self.theta += self.omega * dt
        self.theta = (self.theta + math.pi) % (2 * math.pi) - math.pi

        self.x += self.v * math.cos(self.theta) * dt
        self.y += self.v * math.sin(self.theta) * dt

        if len(self.history) == 0 or np.hypot(self.x - self.history[-1][0], self.y - self.history[-1][1]) > 5:
            self.history.append((self.x, self.y))
            if len(self.history) > 800:
                self.history.pop(0)

    def draw(self, surface):
        if len(self.history) > 1:
            pygame.draw.lines(surface, COR_TRAJETORIA, False, self.history, 2)

        pos_int = (int(self.x), int(self.y))
        pygame.draw.circle(surface, COR_ROBO, pos_int, int(self.radius))

        linha_frente_x = self.x + (self.radius + 10) * math.cos(self.theta)
        linha_frente_y = self.y + (self.radius + 10) * math.sin(self.theta)
        pygame.draw.line(surface, COR_DIRECAO, pos_int, (int(linha_frente_x), int(linha_frente_y)), 3)


def constroi_sequencia_quadrado():
    sequencia = []
    for _ in range(REPETICOES):
        sequencia.append((VEL_LINEAR, 0.0, TEMPO_RETO))   # anda reto
        sequencia.append((0.0, VEL_ANGULAR, TEMPO_GIRO))  # gira 90 graus
    return sequencia


def main():
    pygame.init()
    screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Exercício 2: Quadrado em Malha Aberta")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 14)

    x0, y0 = LARGURA_TELA // 2, ALTURA_TELA // 2
    robot = DiffDriveRobot(x=x0, y=y0, theta=0.0)

    sequencia = constroi_sequencia_quadrado()
    indice_estado = 0
    tempo_no_estado = 0.0
    concluido = False

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not concluido:
            v_atual, omega_atual, duracao_atual = sequencia[indice_estado]
            robot.set_direct_velocity(v_atual, omega_atual)
            robot.update(dt)

            tempo_no_estado += dt
            if tempo_no_estado >= duracao_atual:
                tempo_no_estado = 0.0
                indice_estado += 1
                if indice_estado >= len(sequencia):
                    concluido = True
                    robot.set_direct_velocity(0.0, 0.0)

        screen.fill(COR_FUNDO)
        pygame.draw.circle(screen, COR_ALVO, (int(x0), int(y0)), 4, width=2)
        robot.draw(screen)

        erro_x = robot.x - x0
        erro_y = robot.y - y0
        erro_dist = math.hypot(erro_x, erro_y)
        erro_theta_deg = math.degrees(robot.theta)  # deveria ser ~0 se fechasse perfeitamente

        estado_txt = "CONCLUÍDO" if concluido else f"Estado {indice_estado + 1}/{len(sequencia)}"
        info_txt = [
            f"{estado_txt} | Pose X: {robot.x:.1f} | Y: {robot.y:.1f} | Theta: {erro_theta_deg:.1f} deg",
            f"Erro em relação ao início: dx={erro_x:.1f} dy={erro_y:.1f} dist={erro_dist:.1f} px",
            "Círculo amarelo = pose inicial. Compare com a posição final do robô.",
        ]
        for i, txt in enumerate(info_txt):
            rendered = font.render(txt, True, (220, 220, 220))
            screen.blit(rendered, (15, 15 + i * 20))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()