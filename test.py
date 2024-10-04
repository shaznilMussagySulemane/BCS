# import os
# import hashlib

# # Função para converter bytes para hex, iniciando com '0x'
# def bytes_to_hex(byte_data):
#     return '0x' + byte_data.hex()

# # Função para gerar uma chave privada e uma chave pública
# def generate_keys():
#     # Gerar uma chave privada (64 bytes aleatórios)
#     private_key = os.urandom(64)

#     # Gerar uma chave pública a partir da chave privada (apenas um exemplo simples)
#     public_key = hashlib.sha256(private_key).digest()  # Hash da chave privada

#     return private_key, public_key

# # Função para assinar uma mensagem
# def sign_message(private_key, message):
#     # Concatenar a mensagem com a chave privada
#     message_bytes = message.encode() + private_key
#     # Criar uma assinatura usando SHA-256
#     signature = hashlib.sha256(message_bytes).digest()
#     return signature  # Retornar a assinatura em bytes

# # Função para verificar a assinatura
# def verify_signature(public_key, message, signature):
#     # Recriar a assinatura a partir da mensagem e da chave pública
#     expected_signature = sign_message(public_key, message)
#     return expected_signature == signature

# # Exemplo de uso
# if __name__ == "__main__":
#     # Gerar chaves
#     private_key, public_key = generate_keys()
    
#     print("Private Key:", bytes_to_hex(private_key))
#     print("Public Key:", bytes_to_hex(public_key))

#     # Mensagem a ser assinada
#     message = "Hello, this is a secret message!"

#     # Assinar a mensagem
#     signature = sign_message(private_key, message)
#     print("Signature:", bytes_to_hex(signature))

#     # Verificar a assinatura
#     is_valid = verify_signature(private_key, message, signature)
#     print("Is the signature valid?", is_valid)

from BlockChainSystem import BlockChain, Transaction
import time

# Exemplo de uso
blockchain = BlockChain()
# Adicione algumas transações para testar
# Dê algum tempo para que as transações sejam processadas
# time.sleep(0.001)  # Aguarde um pouco para permitir que o thread processe as transações

# blockchain.add_transaction(Transaction('Alice', 'Bob', 100, 0))
# blockchain.add_transaction(Transaction('Bob', 'Charlie', 50, 0))
# print(blockchain.get_balance('0xc96f9e60f6172bf65db51101aed80dcce29566316b3348ea88d8501179da4243aded0e71975a40d0483766b44851f4fbad3337cfe3ae8cd3beb5d7f7176648ce'))

# blockchain.transfer('shaznil', 'antonio', 500000)
# blockchain.deposit("0xc96f9e60f6172bf65db51101aed80dcce29566316b3348ea88d8501179da4243aded0e71975a40d0483766b44851f4fbad3337cfe3ae8cd3beb5d7f7176648ce", 20)
# blockchain.account_exist('Genesiss')

blockchain.deposit_account()

# time.sleep(1)