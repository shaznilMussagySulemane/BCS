import ecdsa


mensagem = f'Shaznil'

chave_privada = ecdsa.SigningKey.generate(curve=ecdsa.SECP128r1)
chave_publica = chave_privada.get_verifying_key()     
cprhex, cpuhex = chave_privada.to_string().hex(), chave_publica.to_string().hex()   

print(cprhex, cpuhex)

chave_privada_bytes = bytes.fromhex(cprhex[:32]+"")
sk = ecdsa.SigningKey.from_string(chave_privada_bytes, curve=ecdsa.SECP128r1)
assinatura_remetente = sk.sign(mensagem.encode()).hex()

chave_publica_bytes = bytes.fromhex(cpuhex)
vk = ecdsa.VerifyingKey.from_string(chave_publica_bytes, curve=ecdsa.SECP128r1)
        
done = False
try:
    done =  vk.verify(bytes.fromhex(assinatura_remetente), mensagem.encode())
except ecdsa.BadSignatureError:
    pass

print(done)