import requests
import json
import random
import threading

url = 'http://localhost:5070/transacao'

def gerar_transacao():
    de = f'usuario_{random.randint(1, 100)}'
    para = f'usuario_{random.randint(1, 100)}'
    quantidade = random.randint(1, 1000)
    return {
        'de': de,
        'para': para,
        'quantidade': quantidade
    }

def enviar_transacao():
    transacao = gerar_transacao()  # Gera uma nova transação
    response = requests.post(url, json=transacao)  # Envia a transação
    if response.status_code == 201:  # Status 201 indica sucesso
        print(f'Transação enviada: {transacao}')
    else:
        print(f'Erro ao enviar transação: {response.json()}')

def enviar_transacoes_em_threads(num_transacoes, num_threads):
    threads = []
    
    for _ in range(num_transacoes):
        t = threading.Thread(target=enviar_transacao)  # Cria uma nova thread para enviar a transação
        threads.append(t)  # Adiciona a thread à lista
        t.start()  # Inicia a thread
        
        # Limita o número de threads ativas
        if len(threads) >= num_threads:
            for thread in threads:  # Aguarda que todas as threads terminem
                thread.join()
            threads = []  # Reseta a lista de threads

    # Aguarda qualquer thread restante
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    num_transacoes = 50  # Número total de transações a serem enviadas
    num_threads = 75  # Número de threads simultâneas permitidas
    enviar_transacoes_em_threads(num_transacoes, num_threads)
