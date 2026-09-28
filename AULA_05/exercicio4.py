import math


def normalizar_angulo(angulo):
    return (angulo + math.pi) % (2 * math.pi) - math.pi


def calcular_orientacao_alvo(x, y, theta, x_alvo, y_alvo, Kp=1.5):
    theta_alvo = math.atan2(y_alvo - y, x_alvo - x)
    e_theta = normalizar_angulo(theta_alvo - theta)
    omega = Kp * e_theta
    return omega


if __name__ == "__main__":
    x, y, theta = 0.0, 0.0, 0.0
    x_alvo, y_alvo = 1.0, 1.0

    theta_alvo = math.atan2(y_alvo - y, x_alvo - x)
    erro = normalizar_angulo(theta_alvo - theta)
    omega = calcular_orientacao_alvo(x, y, theta, x_alvo, y_alvo)

    print(f"Pose atual: ({x:.1f}, {y:.1f}, theta={theta:.3f} rad)")
    print(f"Alvo: ({x_alvo:.1f}, {y_alvo:.1f})")
    print(f"Theta alvo: {theta_alvo:.3f} rad")
    print(f"Erro normalizado: {erro:.3f} rad")
    print(f"Omega (Kp=1.5): {omega:.3f} rad/s")
