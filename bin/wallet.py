import os
import json
from tools import generate_keys, bytes_to_hex
from transaction import Transaction

class Wallet:
    def __init__(self, path = "./../data/wallet.json"):
        self._path = path
        self.accounts = []
        if not os.path.exists(path):
            
            with open(path, 'w') as f:
                f.write("[{}]")
                
            with open(path, 'r') as f:
                self.accounts = json.loads(f.read())
                
    def create_master_account(self, transaction, balance = 100000000):
        private_key, public_key = generate_keys()
        with open(self._path, 'w') as f:
            json.dump([ {"public_key": bytes_to_hex(public_key), "private_key": bytes_to_hex(private_key) }], f, indent=4)
        
        with open(self._path, 'r') as f:
            self.accounts = json.loads(f.read())
            
        transaction.add_transaction(Transaction('Genesis', bytes_to_hex(public_key), balance, 0))