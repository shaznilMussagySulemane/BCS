import hashlib
import base64
import os

def compute_hash(nonce, transactions: list, previous_hash, timestamp):
    return hashlib.sha256(
        f'{timestamp}, {nonce}, {transactions}, {previous_hash}'.encode()
    ).hexdigest()
    
def sign_message(private_key, message):
    # Concatenar a chave privada e a mensagem
    message_bytes = message.encode() + private_key
    # Criar uma assinatura usando SHA-256
    signature = hashlib.sha256(message_bytes).digest()
    return base64.b64encode(signature).decode()

def generate_keys():
    private_key = os.urandom(64)
    public_key = hashlib.sha256(private_key).digest()
    return private_key, public_key    

def verify_signature(private_key, message, signature):
    # Recriar a assinatura a partir da mensagem e da chave pública
    expected_signature = sign_message(private_key, message)
    return expected_signature == signature

def bytes_to_hex(byte_data):
    return '0x' + byte_data.hex()