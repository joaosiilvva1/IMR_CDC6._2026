import numpy as np


def processar_scan(leituras_lidar):
    leituras = np.asarray(leituras_lidar, dtype=float)

    if leituras.size != 360:
        raise ValueError("O LiDAR deve possuir exatamente 360 leituras.")

    validas = np.where((leituras >= 0.1) & (leituras <= 5.0), leituras, np.nan)

    frente = np.concatenate((validas[345:360], validas[0:16]))
    esquerda = validas[45:136]
    direita = validas[225:316]

    def menor_valida(setor):
        return float(np.nanmin(setor)) if np.any(~np.isnan(setor)) else float("inf")

    return {
        "frente": menor_valida(frente),
        "esquerda": menor_valida(esquerda),
        "direita": menor_valida(direita),
    }


if __name__ == "__main__":
    leituras = np.full(360, 2.5)
    leituras[0] = 0.0
    leituras[350] = 0.35
    leituras[90] = 0.80
    leituras[270] = 0.60
    leituras[100] = 9.0

    resultado = processar_scan(leituras)
    print("Menores distâncias válidas por setor:")
    for setor, distancia in resultado.items():
        print(f"{setor.capitalize():8s}: {distancia:.2f} m")
