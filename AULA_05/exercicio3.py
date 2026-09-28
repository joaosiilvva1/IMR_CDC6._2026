def controle_reativo(distancias, distancia_critica=0.4, ganho=1.0):
    frente = distancias["frente"]
    esquerda = distancias["esquerda"]
    direita = distancias["direita"]

    if frente < distancia_critica:
        v = 0.0
        omega = 1.0 if esquerda >= direita else -1.0
    else:
        v = 0.5
        omega = ganho * (direita - esquerda)

    return v, omega


if __name__ == "__main__":
    casos = {
        "obstaculo_frontal": {"frente": 0.30, "esquerda": 1.20, "direita": 0.60},
        "frente_livre": {"frente": 1.50, "esquerda": 0.80, "direita": 1.10},
    }

    for nome, distancias in casos.items():
        v, omega = controle_reativo(distancias)
        print(f"{nome}:")
        print(f"  distâncias = {distancias}")
        print(f"  comando -> v={v:.2f} m/s, omega={omega:.2f} rad/s")
