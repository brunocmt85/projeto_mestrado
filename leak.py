#!/usr/bin/env python3
"""
Sistema de Processamento de Dados com Vazamentos de Memória Intencionais
Este programa simula um sistema complexo com múltiplos tipos de vazamentos
para testar ferramentas de monitoramento de memória.
"""

import threading
import time
import json
import random
import string
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from collections import defaultdict
import weakref
import gc

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Variáveis globais que causam vazamentos
GLOBAL_CACHE = {}  # Vazamento 1: Cache que nunca é limpo
EVENT_LISTENERS = []  # Vazamento 2: Listeners que se acumulam
THREAD_POOL = []  # Vazamento 3: Threads que não são limpas adequadamente

@dataclass
class DataRecord:
    """Classe para representar registros de dados"""
    id: str
    timestamp: datetime
    data: Dict[str, Any]
    metadata: Dict[str, Any]
    
    def __post_init__(self):
        # Vazamento 4: Referências circulares
        self.parent = None
        self.children = []

class EventListener:
    """Classe que simula listeners de eventos"""
    def __init__(self, name: str, callback):
        self.name = name
        self.callback = callback
        self.data_buffer = []  # Vazamento 5: Buffer que cresce indefinidamente
        
    def handle_event(self, event):
        self.data_buffer.append(event)  # Nunca limpa o buffer
        self.callback(event)

class DataProcessor:
    """Processador principal de dados com vazamentos intencionais"""
    
    def __init__(self):
        self.processed_records = {}  # Vazamento 6: Registros processados nunca removidos
        self.temp_files = []  # Vazamento 7: Referências a arquivos temporários
        self.connections = []  # Vazamento 8: Conexões não fechadas
        self.memory_intensive_data = []  # Vazamento 9: Dados grandes acumulados
        
    def process_data_batch(self, batch_size: int = 1000):
        """Processa um lote de dados criando vazamentos"""
        logger.info(f"Processando lote de {batch_size} registros")
        
        for i in range(batch_size):
            # Gera dados aleatórios grandes
            record_id = f"record_{datetime.now().timestamp()}_{i}"
            large_data = self._generate_large_data()
            
            # Cria registro com referências circulares
            record = DataRecord(
                id=record_id,
                timestamp=datetime.now(),
                data=large_data,
                metadata={"processed": True, "size": len(str(large_data))}
            )
            
            # Vazamento: Armazena no cache global sem limpeza
            GLOBAL_CACHE[record_id] = record
            
            # Vazamento: Mantém referências locais
            self.processed_records[record_id] = record
            
            # Vazamento: Adiciona a estruturas que crescem indefinidamente
            self.memory_intensive_data.append(large_data)
            
            # Simula processamento
            self._simulate_processing(record)
            
    def _generate_large_data(self) -> Dict[str, Any]:
        """Gera dados grandes para simular uso real de memória"""
        return {
            "payload": ''.join(random.choices(string.ascii_letters + string.digits, k=10000)),
            "matrix": [[random.random() for _ in range(100)] for _ in range(100)],
            "nested_data": {
                f"key_{i}": {
                    "value": random.random(),
                    "description": ''.join(random.choices(string.ascii_letters, k=500))
                } for i in range(50)
            }
        }
    
    def _simulate_processing(self, record: DataRecord):
        """Simula processamento complexo"""
        # Vazamento: Cria objetos temporários que ficam em memória
        temp_objects = []
        for _ in range(100):
            temp_obj = {
                "id": record.id,
                "data": record.data.copy(),  # Cópia profunda desnecessária
                "processing_time": time.time()
            }
            temp_objects.append(temp_obj)
        
        # Vazamento: Adiciona aos arquivos temporários sem limpeza
        self.temp_files.extend(temp_objects)

class ConnectionManager:
    """Gerenciador de conexões com vazamentos"""
    
    def __init__(self):
        self.active_connections = {}
        self.connection_history = []  # Vazamento: Histórico nunca limpo
        
    def create_connection(self, connection_id: str):
        """Cria uma nova conexão"""
        connection = {
            "id": connection_id,
            "created_at": datetime.now(),
            "data_buffer": [],
            "status": "active"
        }
        
        # Vazamento: Armazena sem limpeza
        self.active_connections[connection_id] = connection
        self.connection_history.append(connection)
        
        return connection
    
    def send_data(self, connection_id: str, data: Any):
        """Envia dados através da conexão"""
        if connection_id in self.active_connections:
            # Vazamento: Buffer cresce indefinidamente
            self.active_connections[connection_id]["data_buffer"].append(data)

class BackgroundWorker:
    """Worker que roda em background com vazamentos"""
    
    def __init__(self, name: str):
        self.name = name
        self.is_running = True
        self.work_queue = []  # Vazamento: Fila de trabalho nunca limpa
        self.results = {}  # Vazamento: Resultados acumulados
        self.thread = None
        
    def start(self):
        """Inicia o worker"""
        self.thread = threading.Thread(target=self._work_loop, daemon=False)
        self.thread.start()
        THREAD_POOL.append(self.thread)  # Vazamento: Threads acumuladas
        
    def _work_loop(self):
        """Loop principal do worker"""
        while self.is_running:
            # Vazamento: Cria dados desnecessários a cada iteração
            work_data = {
                "timestamp": datetime.now(),
                "random_data": [random.random() for _ in range(1000)],
                "worker_name": self.name
            }
            
            self.work_queue.append(work_data)
            
            # Simula trabalho
            result = self._process_work(work_data)
            self.results[time.time()] = result  # Vazamento: Resultados nunca removidos
            
            time.sleep(0.1)  # Simula trabalho
    
    def _process_work(self, work_data: Dict) -> Dict:
        """Processa trabalho"""
        # Vazamento: Cria objetos grandes desnecessários
        large_result = {
            "processed_data": work_data.copy(),
            "additional_data": ''.join(random.choices(string.ascii_letters, k=5000)),
            "computation_result": [random.random() for _ in range(500)]
        }
        
        return large_result

class MemoryLeakSimulator:
    """Classe principal que orquestra todos os vazamentos"""
    
    def __init__(self):
        self.data_processor = DataProcessor()
        self.connection_manager = ConnectionManager()
        self.workers = []
        self.event_listeners = []
        self.running = True
        
    def setup_event_listeners(self):
        """Configura listeners de eventos"""
        for i in range(5):
            listener = EventListener(
                name=f"listener_{i}",
                callback=lambda event: self._handle_event(event)
            )
            self.event_listeners.append(listener)
            EVENT_LISTENERS.append(listener)  # Vazamento global
    
    def _handle_event(self, event):
        """Manipula eventos"""
        # Vazamento: Processa eventos sem limpeza
        processed_event = {
            "original": event,
            "processed_at": datetime.now(),
            "handler_data": [random.random() for _ in range(100)]
        }
        
        # Adiciona a todas as estruturas de dados
        for listener in self.event_listeners:
            listener.data_buffer.append(processed_event)
    
    def start_background_workers(self, num_workers: int = 3):
        """Inicia workers em background"""
        for i in range(num_workers):
            worker = BackgroundWorker(f"worker_{i}")
            worker.start()
            self.workers.append(worker)
    
    def simulate_connections(self, num_connections: int = 10):
        """Simula conexões ativas"""
        for i in range(num_connections):
            conn_id = f"conn_{i}_{time.time()}"
            connection = self.connection_manager.create_connection(conn_id)
            
            # Envia dados para cada conexão
            for j in range(50):
                large_data = {
                    "message_id": j,
                    "payload": ''.join(random.choices(string.ascii_letters, k=2000)),
                    "metadata": {"size": 2000, "type": "simulation"}
                }
                self.connection_manager.send_data(conn_id, large_data)
    
    def run_simulation(self, duration_minutes: int = 5):
        """Executa a simulação por um período determinado"""
        logger.info(f"Iniciando simulação de vazamentos por {duration_minutes} minutos")
        
        # Configura componentes
        self.setup_event_listeners()
        self.start_background_workers()
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        iteration = 0
        while time.time() < end_time and self.running:
            iteration += 1
            logger.info(f"Iteração {iteration} - Tempo restante: {int(end_time - time.time())}s")
            
            # Processa dados (cria vazamentos)
            self.data_processor.process_data_batch(random.randint(500, 1500))
            
            # Simula conexões (cria vazamentos)
            self.simulate_connections(random.randint(5, 15))
            
            # Dispara eventos (cria vazamentos)
            for _ in range(random.randint(10, 50)):
                event = {
                    "type": "data_event",
                    "timestamp": datetime.now(),
                    "data": [random.random() for _ in range(200)]
                }
                self._handle_event(event)
            
            # Relatório de uso de memória
            self._log_memory_usage()
            
            # Aguarda antes da próxima iteração
            time.sleep(random.uniform(1, 3))
        
        logger.info("Simulação finalizada")
    
    def _log_memory_usage(self):
        """Registra uso de memória"""
        try:
            import psutil
            import os
            
            process = psutil.Process(os.getpid())
            memory_info = process.memory_info()
            
            logger.info(f"Uso de memória: {memory_info.rss / 1024 / 1024:.2f} MB")
            logger.info(f"Cache global: {len(GLOBAL_CACHE)} itens")
            logger.info(f"Registros processados: {len(self.data_processor.processed_records)}")
            logger.info(f"Conexões ativas: {len(self.connection_manager.active_connections)}")
            logger.info(f"Threads ativas: {len(THREAD_POOL)}")
            
        except ImportError:
            logger.warning("psutil não disponível para monitoramento de memória")
    
    def stop(self):
        """Para a simulação"""
        self.running = False
        for worker in self.workers:
            worker.is_running = False

def main():
    """Função principal"""
    simulator = MemoryLeakSimulator()
    
    try:
        # Executa por 5 minutos por padrão
        simulator.run_simulation(duration_minutes=5)
    except KeyboardInterrupt:
        logger.info("Simulação interrompida pelo usuário")
    finally:
        simulator.stop()
        logger.info("Limpeza finalizada")

if __name__ == "__main__":
    main()
