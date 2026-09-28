def converter_cmd_vel(v, omega, L=0.3, max_wheel_speed=1.5):
    v_e = v - (omega * L / 2.0)
    v_d = v + (omega * L / 2.0)

    maior_modulo = max(abs(v_e), abs(v_d))

    if maior_modulo > max_wheel_speed:
        fator = max_wheel_speed / maior_modulo
        v_e *= fator
        v_d *= fator

    return v_e, v_d


if __name__ == "__main__":
    entrada = (1.2, 3.0)
    v_e, v_d = converter_cmd_vel(*entrada)
    print(f"Entrada: v={entrada[0]:.2f} m/s, omega={entrada[1]:.2f} rad/s")
    print(f"Velocidade roda esquerda: {v_e:.3f} m/s")
    print(f"Velocidade roda direita:  {v_d:.3f} m/s")
    print(f"Maior módulo após saturação: {max(abs(v_e), abs(v_d)):.3f} m/s")
