import time

print("Simulação0")
def memory_leak_simulation():
    leaked_list = []  
    while True:
        leaked_list.append('A' * 10**6)  
        time.sleep(0.1) 

if __name__ == "__main__":
    memory_leak_simulation()

