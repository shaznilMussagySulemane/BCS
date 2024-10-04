import time
import random
import threading
from queue import Queue
from .models import Bloco, Transacao
import sys
import json

class BlockchainPoS:
    def __init__(self):
        self.cadeia = [self.criar_bloco_genesis()]
        self.carregar()
        print(self.cadeia)
        self.transacoes_queue = Queue()
        self.recompensa = 50
        self.lock = threading.Lock()        
        threading.Thread(target=self.processar_transacoes, daemon=True).start()
        
    def criar_bloco_genesis(self):
        return Bloco(0, [], time.time(), "0").toJson()
        
    def processar_transacoes(self):
        while True:
            transaction_batch = []
            while not self.transacoes_queue.empty() and len(transaction_batch) < 100:  # Processa até 100 transações por vez
                transaction_batch.append(self.transacoes_queue.get())
                print(f'\rLoading... {len(transaction_batch)}', end='\n', flush=True)
                # print(Fore.RED + Style.BRIGHT+"Transaction added"+Style.RESET_ALL)

            if transaction_batch:
                with self.lock:  # Garante que o acesso à blockchain seja seguro
                    previous_hash = self.cadeia[-1]['hash'] if self.cadeia else '0'
                    new_block = Bloco(
                        len(self.cadeia),
                        transaction_batch,  # Passa a lista de transações
                        previous_hash,
                        time.time_ns()
                    )
                    self.cadeia.append(new_block.toJson())  # Salva o bloco na blockchain
                    self.salvar()  # Salva a blockchain após adicionar o bloco
                    print(f'Block added!')
                    
    def adicionar_transacao(self, data: Transacao):
        try:
            data.verificar_assinatura()
            result, code = self.calcular_saldo(data.endereco_remetente)
                
            if result['balance'] < data.quantidade:
                return "Saldo insuficiete", 402
            self.transacoes_queue.put(data.toJson())
            return "Transação criada.", 201
        except:
            return "Assinatura inválida. Transação rejeitada.", 403
        
    def salvar(self):
        with open("Blockchain.json", "w") as f:
            json.dump(self.cadeia, f, indent=4)

    def carregar(self):
        try:
            with open('Blockchain.json', 'r') as f:
                self.cadeia = json.load(f)  # Carrega a blockchain do arquivo
        except FileNotFoundError:
            self.cadeia = []
            
    def mostrar(self):
        return self.cadeia
    
    def calcular_saldo(self, endereco):
        saldo = 0
        
        print(self.cadeia)

        for bloco in self.cadeia:
            for transacao in bloco['transacoes']:
                if transacao['address'] == endereco:
                    saldo -= transacao['amount']
                if transacao['to'] == endereco:
                    saldo += transacao['amount']

        return { "endereço": endereco, "balance": saldo }, 200