from tools import compute_hash

class Block:
    def __init__(self, nonce, transactions: list, previous_hash, timestamp):
        self.nonce = nonce
        self.timestamp = timestamp
        self.transactions = [tx.toString() for tx in transactions]  # Processa uma lista de transações
        self.previous_hash = previous_hash
        self.hash = compute_hash(nonce, self.transactions, previous_hash, timestamp)