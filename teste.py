import time

# Simulação1
def memory_leak_simulation():
    leaked_list = []  # Lista que vai crescer indefinidamente
    while True:
        leaked_list.append('A' * 10**6)  # Adiciona 1 MB de dados a cada iteração
        time.sleep(0.1)  # Pequeno atraso para observar o consumo gradual de memória

if __name__ == "__main__":
    memory_leak_simulation()

