import json
from cryptography.fernet import Fernet
import hashlib
from base64 import urlsafe_b64encode

def gerar_chave(senha, usuario):
  """Gera uma chave de criptografia a partir da senha e do usuário."""
  # Combina a senha e o usuário para criar uma string única
  texto_para_hash = senha + usuario
  # Cria um hash SHA-256 a partir da string
  hash_object = hashlib.sha256(texto_para_hash.encode('utf-8'))
  # Extrai 32 bytes do hash
  chave = hash_object.digest()[:32]
  # Converte a chave para URL-safe base64
  chave_encoded = urlsafe_b64encode(chave).decode('utf-8')
  return Fernet(chave_encoded)

def criptografar_arquivo_json(arquivo, senha, usuario):
  """Criptografa um arquivo JSON utilizando a senha e o usuário."""
  chave = gerar_chave(senha, usuario)
  with open(arquivo, "r") as f:
      dados_json = json.load(f)
  # Convertemos os dados JSON para bytes para criptografar
  dados_json_bytes = json.dumps(dados_json).encode('utf-8')
  encrypted_data = chave.encrypt(dados_json_bytes)
  with open(arquivo.split('.')[0] + ".gbcc", "wb") as f:
      f.write(encrypted_data)

def descriptografar_arquivo_json(arquivo, senha, usuario):
  """Descriptografa um arquivo JSON utilizando a senha e o usuário."""
  chave = gerar_chave(senha, usuario)
  with open(arquivo + ".gbcc", "rb") as f:
      encrypted_data = f.read()
  try:
      decrypted_data = chave.decrypt(encrypted_data)
      # Convertemos os bytes de volta para JSON
      dados_json = json.loads(decrypted_data.decode('utf-8'))
      with open(arquivo, "w") as f:
          json.dump(dados_json, f, indent=4)
  except Exception as e:
      print("Erro ao descriptografar:", e)

# Exemplo de uso
arquivo_original = "meu_arquivo"
senha = "minha_senha_forte"
usuario = "meu_usuario"

# criptografar_arquivo_json(arquivo_original, senha, usuario)
descriptografar_arquivo_json(arquivo_original, senha, usuario)