import time

# Lista que nunca é liberada da memória
vazamento = []

def vazamento_de_memoria():
    while True:
        # Cria muitos dados e armazena permanentemente
        vazamento.append("A" * 10**6)  # 1 MB de dados
        print(f"Objetos armazenados: {len(vazamento)}")
        time.sleep(0.5)

if __name__ == "__main__":
    vazamento_de_memoria()
    
