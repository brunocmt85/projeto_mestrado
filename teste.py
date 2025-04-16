import time
vazamento[]

def vazamento_de_memoria():
    while True:
        vazamento.append("A" * 10**6)  
        print(f"Objetos armazenados: {len(vazamento)}")
        time.sleep(0.5)

if __name__ == "__main__":
    vazamento_de_memoria()
    
