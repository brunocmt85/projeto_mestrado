import time

def vazamento_de_memoria():
    vazamento = []
    try:
        while True:
            vazamento.append("A" * 10**6)
            print(f"Objetos armazenados: {len(vazamento)}")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Processo interrompido.")
    finally:
        del vazamento
        print("Memória liberada.")

if __name__ == "__main__":
    print("39")
    vazamento_de_memoria()
