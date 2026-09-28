import math


def normalizar_angulo(angulo):
    return (angulo + math.pi) % (2 * math.pi) - math.pi


def calcular_orientacao_alvo(x, y, theta, x_alvo, y_alvo, Kp=1.5):
    theta_alvo = math.atan2(y_alvo - y, x_alvo - x)
    e_theta = normalizar_angulo(theta_alvo - theta)
    return Kp * e_theta


def controle_reativo(distancias, distancia_critica=0.4, ganho=1.0):
    frente = distancias["frente"]
    esquerda = distancias["esquerda"]
    direita = distancias["direita"]

    if frente < distancia_critica:
        return 0.0, (1.0 if esquerda >= direita else -1.0)

    return 0.5, ganho * (direita - esquerda)


def maquina_de_estados(x, y, theta, x_alvo, y_alvo,
                       dist_frente, dist_esq, dist_dir):
    distancia_alvo = math.hypot(x_alvo - x, y_alvo - y)

    if distancia_alvo < 0.2:
        estado_atual = "OBJETIVO_ALCANCADO"
        v_cmd = 0.0
        omega_cmd = 0.0

    elif dist_frente < 0.5:
        estado_atual = "DESVIAR_OBSTACULO"
        v_cmd, omega_cmd = controle_reativo({
            "frente": dist_frente,
            "esquerda": dist_esq,
            "direita": dist_dir,
        })

    else:
        estado_atual = "IR_PARA_ALVO"
        v_cmd = 0.5
        omega_cmd = calcular_orientacao_alvo(
            x, y, theta, x_alvo, y_alvo
        )

    return estado_atual, v_cmd, omega_cmd


if __name__ == "__main__":
    testes = [
        ("indo_para_alvo", (0.0, 0.0, 0.0, 2.0, 1.0, 1.5, 1.0, 1.0)),
        ("desviando",      (0.0, 0.0, 0.0, 2.0, 1.0, 0.3, 1.2, 0.5)),
        ("objetivo",       (1.95, 1.95, 0.0, 2.0, 2.0, 1.0, 1.0, 1.0)),
    ]

    for nome, args in testes:
        estado, v, omega = maquina_de_estados(*args)
        print(f"{nome}: estado={estado}, v={v:.2f} m/s, omega={omega:.3f} rad/s")
