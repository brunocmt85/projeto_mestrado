import gc

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
        
        # Limpa variáveis que não são mais necessárias
        del processed_chunk
        gc.collect()  # Força a coleta de lixo para liberar memória

if __name__ == "__main__":
    main()