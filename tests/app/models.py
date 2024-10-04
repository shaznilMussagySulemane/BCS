import hashlib
import ecdsa
import binascii

class Bloco:
    def __init__(self, indice, transacoes, timestamp, hash_anterior):
        self.indice = indice
        self.transacoes = transacoes
        self.timestamp = timestamp
        self.hash_anterior = hash_anterior
        self.hash = self.calcular_hash()

    def calcular_hash(self):
        conteudo = f"{self.indice}{self.transacoes}{self.timestamp}{self.hash_anterior}"
        return hashlib.sha256(conteudo.encode()).hexdigest()

    def __repr__(self):
        return (
            f"Bloco #{self.indice}\n"
            f"Timestamp: {self.timestamp}\n"
            f"Transações: {self.transacoes}\n"
            f"Hash Anterior: {self.hash_anterior}\n"
            f"Hash: {self.hash}\n"
        )

    def toJson(self):
        return {
            "indice": self.indice,
            "transacoes": self.transacoes,
            "timestamp": self.timestamp,
            "hash_anterior": self.hash_anterior,
            "hash": self.hash,
        }

class Accounts:    
    def create(self):
        chave_privada = ecdsa.SigningKey.generate(curve=ecdsa.SECP128r1)
        chave_publica = chave_privada.get_verifying_key()     
        return chave_privada.to_string().hex(), chave_publica.to_string().hex()   

class Transacao:
    def __init__(self, endereco_remetente, nome_remetente, endereco_destinatario, quantidade):
        self.endereco_remetente = endereco_remetente
        self.nome_remetente = nome_remetente
        self.endereco_destinatario = endereco_destinatario
        self.quantidade = quantidade
        self.assinatura_remetente = None
        
    def calcular_hash(self):
        transacao_conteudo = (str(self.endereco_remetente) +str(self.nome_remetente) + str(self.endereco_remetente) + str(self.quantidade))
        return hashlib.sha256(transacao_conteudo.encode()).hexdigest()
        
    def assinar_transacao(self, chave_privada):
        if self.endereco_remetente == "Sistema":
            return True

        chave_privada_bytes = bytes.fromhex(chave_privada)
        sk = ecdsa.SigningKey.from_string(chave_privada_bytes, curve=ecdsa.SECP128r1)
        self.assinatura_remetente = sk.sign(self.calcular_hash().encode()).hex()
        
    def verificar_assinatura(self):
        if self.endereco_remetente == "Sistema":  # Transações de geração não precisam de verificação
            return True
        
        if not self.assinatura_remetente:
            raise Exception("A transação não está assinada.")
        
        chave_publica_bytes = bytes.fromhex(self.endereco_remetente)
        vk = ecdsa.VerifyingKey.from_string(chave_publica_bytes, curve=ecdsa.SECP128r1)
        
        try:
            valid = vk.verify(bytes.fromhex(self.assinatura_remetente), self.calcular_hash().encode())
            return valid
        except:
            return False

    def toJson(self):
        return {
            "address": self.endereco_remetente,
            "address_name": self.nome_remetente,
            "to": self.endereco_destinatario,
            "amount": self.quantidade
        }
