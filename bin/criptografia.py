import json
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import uuid
import hashlib
import platform

def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    return private_key, public_key

def encrypt_aes(data, key):
    iv = os.urandom(16)  # Vetor de inicialização (IV)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(data) + encryptor.finalize()
    return iv, ciphertext

def decrypt_aes(iv, ciphertext, key):
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
    return decrypted_data

def encrypt_aes_key_with_rsa(public_key, aes_key):
    encrypted_key = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_key

def decrypt_aes_key_with_rsa(private_key, encrypted_key):
    aes_key = private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return aes_key

def read_json_file(filepath):
    with open(filepath, 'r') as file:
        json_data = json.load(file)
        return json.dumps(json_data).encode('utf-8')  # Converte para bytes

def save_encrypted_file(filepath, iv, ciphertext, encrypted_key):
    with open(filepath, 'wb') as file:
        file.write(iv)  # Armazena o IV no início
        file.write(encrypted_key)  # Armazena a chave AES criptografada
        file.write(ciphertext)  # Armazena os dados criptografados

def read_encrypted_file(filepath):
    with open(filepath, 'rb') as file:
        iv = file.read(16)  # O IV é sempre de 16 bytes
        encrypted_key = file.read(256)  # O RSA com chave de 2048 bits gera 256 bytes de dados criptografados
        ciphertext = file.read()  # O resto é o conteúdo criptografado
        return iv, encrypted_key, ciphertext

def save_decrypted_json(filepath, decrypted_data):
    json_data = json.loads(decrypted_data.decode('utf-8'))  # Converte bytes para string, depois para JSON
    with open(filepath, 'w') as file:
        json.dump(json_data, file, indent=4)
        
        
def get_unique_computer_info():
    # 1. Obter o endereço MAC
    mac_address = hex(uuid.getnode())

    # 2. Obter informações do sistema (como nome do SO, versão, etc.)
    system_info = platform.platform()

    # 3. Concatenar as informações únicas
    unique_info = mac_address + system_info

    return unique_info

def generate_computer_specific_hash():
    # 4. Obter informações únicas do computador
    unique_info = get_unique_computer_info()

    # 5. Gerar o hash SHA-256 a partir das informações únicas
    hash_object = hashlib.sha256(unique_info.encode('utf-8'))
    hash_hex = hash_object.hexdigest()

    return hash_hex

from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode
import secrets

def gerar_chave_aleatoria():
    """Gera uma chave de criptografia aleatória."""
    return Fernet.generate_key()

def gerar_chave_com_parametro(key = str):
    """Gera uma chave de criptografia baseada na key passada como argumento."""
    hash_string = hashlib.sha256(key.encode('utf-8')).digest()
    encoded_key = urlsafe_b64encode(hash_string[:32]).decode('utf-8')
    return Fernet(encoded_key)

def criptografar_e_salvar(arquivo, dados, chave):
    """Criptografa um arquivo."""
    fernet = Fernet(chave)
    encrypted = fernet.encrypt(dados)
    print(dados)
    with open(arquivo + '.encrypted', 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

def descriptografar(arquivo, chave):
    """Descriptografa um arquivo."""
    fernet = Fernet(chave)
    with open(arquivo + '.encrypted', 'rb') as encrypted_file:
        encrypted = encrypted_file.read()
    decrypted = fernet.decrypt(encrypted)
    with open(arquivo, 'wb') as file:
        file.write(decrypted)

def descriptografar_data(dados):
    """Descriptografa um arquivo."""
    unica = generate_computer_specific_hash()
    chave = gerar_chave_com_parametro(unica)
    decrypted = chave.decrypt(dados)
    data = json.loads(decrypted.decode().removeprefix('b"'))
    print(data[12:103])
    pass

if __name__ == "__main__":
    private_key, public_key = generate_keys()

    input_json_path = 'input.json'
    encrypted_file_path = 'encrypted_data.bin'
    decrypted_json_path = 'output.json'
    
    json_data = read_json_file(input_json_path)

    aes_key = os.urandom(32)

    iv, ciphertext = encrypt_aes(json_data, aes_key)

    encrypted_key = encrypt_aes_key_with_rsa(public_key, aes_key)

    save_encrypted_file(encrypted_file_path, iv, ciphertext, encrypted_key)

    print(f"Arquivo {input_json_path} criptografado e salvo em {encrypted_file_path}")

    iv, encrypted_key_from_file, ciphertext_from_file = read_encrypted_file(encrypted_file_path)

    aes_key_from_file = decrypt_aes_key_with_rsa(private_key, encrypted_key_from_file)

    decrypted_data = decrypt_aes(iv, ciphertext_from_file, aes_key_from_file)

    save_decrypted_json(decrypted_json_path, decrypted_data)

    print(f"Arquivo criptografado foi descriptografado e salvo em {decrypted_json_path}")
