import time
vazamento2[]   
 
def vazamento_de_memoria():
    while True:
        vazamento2.append("A" * 10**6)  
        print(f"Objetos armazenados: {len(vazamento2)}")
        time.sleep(0.5)

if __name__ == "__main__":
    vazamento_de_memoria()
    
