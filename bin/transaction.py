import os
import uuid
import json
import hashlib
import base64

class Transaction:
    def __init__(self, _from, _to, _amount, _tax):
        self._id = str(uuid.uuid4())
        self._from = _from
        self._to = _to
        self._amount = _amount
        self._tax = _tax
        self.signature = None  # Adicione a assinatura

    def toString(self):
        return json.dumps({  # Converte o dicionário em string JSON
            'id': self._id,
            'from': self._from,
            'to': self._to,
            'amount': self._amount,
            'tax': self._tax,
            'signature': self.signature
        })