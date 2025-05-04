# Teste de memória em Python 04

leak_list = []  # Lista global que acumula dados desnecessariamente

def process_data(data_chunk):
    # Simula o processamento de dados
    result = [x**2 for x in data_chunk]
    return result

def main():
    # Simula um grande conjunto de dados dividido em chunks
    data = [list(range(1000)) for _ in range(100)]
    
    for chunk in data:
        # Processa o chunk atual
        processed_chunk = process_data(chunk)
        
        # Simula o uso do resultado
        print(f"Processed chunk with {len(processed_chunk)} items.")
        
        # Acumula os dados processados desnecessariamente em uma lista global
        leak_list.append(processed_chunk)

if __name__ == "__main__":
    main()
