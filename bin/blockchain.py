import time
import threading
from queue import Queue
import os
import json
from transaction import Transaction
from tools import compute_hash, generate_keys, bytes_to_hex
from block import Block
from wallet import Wallet


class BlockChain:
    def __init__(self, block_pathname = './../data/blockChain.json') -> None:
        self.block_pathname = block_pathname
        print("Blockchain inicializada com sucesso.")
        self.blocks = []
        self.wallet = Wallet()
        self.transaction_queue = Queue()
        self.lock = threading.Lock()  # Para garantir segurança em acessos concorrentes

        if os.path.exists(self.block_pathname):
            with open(self.block_pathname, 'r') as arquivo:
                try:
                    self.blocks = json.load(arquivo)
                    self._verify_and_repair_chain()
                except json.JSONDecodeError:
                    print(f"Erro ao carregar {self.block_pathname}. Iniciando nova blockchain.")
                    self.blocks = []
                    self._create_genesis_block()
            print(f"{self.block_pathname} file exists.")       
        else:
            with open(self.block_pathname, 'w') as arquivo:
                json.dump([], arquivo, indent=4)
            print(f"{self.block_pathname} file created successfully.")
            self._create_genesis_block()

        # Inicia um thread para processar as transações na fila
        threading.Thread(target=self.process_transactions, daemon=True).start()

    def _verify_and_repair_chain(self):
        for block in self.blocks:
            if 'hash' not in block or 'nonce' not in block:
                transaction_data = block.get('transactions', [{}])
                transactions = [Transaction(
                    tx.get('from', ''),
                    tx.get('to', ''),
                    tx.get('amount', 0),
                    tx.get('tax', 0),
                    tx.get('signature', None)
                ) for tx in transaction_data]
                block['hash'] = compute_hash(
                    block.get('nonce', 0),
                    transactions,
                    block.get('previous_hash', '0'),
                    block.get('timestamp', time.time_ns())
                )

    def add_transaction(self, data: Transaction):
        self.transaction_queue.put(data)

    def process_transactions(self):
        while True:
            transaction_batch = []
            while not self.transaction_queue.empty() and len(transaction_batch) < 100:  # Processa até 100 transações por vez
                transaction_batch.append(self.transaction_queue.get())
                # print(Fore.RED + Style.BRIGHT+"Transaction added"+Style.RESET_ALL)

            if transaction_batch:
                with self.lock:  # Garante que o acesso à blockchain seja seguro
                    previous_hash = self.blocks[-1]['hash'] if self.blocks else '0'
                    new_block = Block(
                        len(self.blocks),
                        transaction_batch,  # Passa a lista de transações
                        previous_hash,
                        time.time_ns()
                    )
                    self.blocks.append(new_block.__dict__)  # Salva o bloco na blockchain
                    self._save_chain()  # Salva a blockchain após adicionar o bloco
                    print(f'Block added!')

    def _save_chain(self):
        
        organized_chain = [
            {
                'nonce': block['nonce'],
                'timestamp': block['timestamp'],
                'transactions': block['transactions'],  # Manter como lista de dicionários
                'previous_hash': block['previous_hash'],
                'hash': block['hash']
            } for block in self.blocks
        ]
        # # Salva a representação organizada em um arquivo JSON
        with open(self.block_pathname, 'w') as arquivo:
            json.dump(organized_chain, arquivo, indent=4)

    def create_account(self):
        
        private_key, public_key = generate_keys()
        self.add_transaction(Transaction('', bytes_to_hex(public_key), 0, 0))  # Adiciona a criação da conta como transação
        return {
            "address": bytes_to_hex(public_key), 
            "private_key": bytes_to_hex(private_key)
        }

    def _create_genesis_block(self):
        print("Creating genesis block...")
        private_key, public_key = generate_keys()
        with open("deposit_account.json", 'w') as arquivo:
            json.dump([{"public_key": bytes_to_hex(public_key)}], arquivo, indent=4)
        self.add_transaction(Transaction('Genesis', bytes_to_hex(public_key), 1000000000000, 0))

    def deposit(self, address, amount):
        if( not self.account_exist(address) ):
            return "Endereço não encontrado", 403
        deposit_account = self._deposit_account()
        self.add_transaction(Transaction(deposit_account, address, amount, 0))
        return "Deposito realizado com sucesso.", 200

    def transfer(self, public_key, to_address, amount):
        print(f"Transferindo {amount} BSS de {public_key} para {to_address}.")
        # Criar a transação
        balance, key = self.get_balance(public_key)
        if( not self.account_exist(public_key) ):
            return "Endereço não encontrado", 403
        
        if( not self.account_exist(to_address) ):
            return "Endereço não encontrado", 403
        if( float(balance['balance']) < amount ):
            return "Saldo insuficiente " + str(float(balance['balance'])), 403
        
        transaction = Transaction(public_key, to_address, amount, 0)  # O valor do imposto pode ser zero ou calculado
        self.add_transaction(transaction)
        return "Transfer sucessfully.", 200

    def get_blocks(self):
        return self.blocks
    
    def account_exist(self, address):
        exist = False
        for block in self.blocks:
            transactions = block.get('transactions', [])
            for tx in transactions:
                tx = json.loads(tx)
                
                if tx['from'] == address:
                    exist = True
                    break
                if tx['to'] == address:                    
                    exist = True
                    break
        return exist
    
    def get_balance(self, public_key):
        if( not self.account_exist(public_key)): return "Endereço não encontrado.", 400
        balance = 0
        for block in self.blocks:
            transactions = block.get('transactions', [])
            # print(transactions)
            for tx in transactions:
                tx = json.loads(tx)
                
                if tx['from'] == public_key:
                    balance -= tx['amount']  # Deduzir o valor se for uma transação de saída
                if tx['to'] == public_key:                    
                    balance += tx['amount']  # Adicionar o valor se for uma transação de entrada
        return {"balance": balance, "public_key": public_key}, 200
    
    def _deposit_account(self):
        with open('deposit_account.json', 'r') as arquivo:
            return json.load(arquivo)[0]['public_key']