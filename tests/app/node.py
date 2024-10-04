from flask import Flask, request, jsonify
from .blockchain import BlockchainPoS, Transacao
from .models import Accounts

class Node:
    def __init__(self, blockchain = BlockchainPoS):
        self.blockchain = blockchain
        self.app = Flask(__name__)  # Inicializa a aplicação Flask

        # Define as rotas da API
        self.app.add_url_rule('/transfer', 'nova_transacao', self.nova_transacao, methods=['POST'])
        self.app.add_url_rule('/sync', 'sincronizar_cadeia', self.sincronizar_cadeia, methods=['GET'])
        self.app.add_url_rule('/chain', 'mostrar_cadeia', self.mostrar_cadeia, methods=['GET'])
        self.app.add_url_rule('/signup', 'criar_conta', self.criar_conta, methods=['POST'])
        self.app.add_url_rule('/balance', 'consultar_saldo', self.consultar_saldo, methods=['POST'])
    
    def criar_conta(self):
        privada, publica = Accounts().create()
        transacao = Transacao("Sistema", "Sistema", publica, 0)
        self.blockchain.adicionar_transacao(transacao)
        with open('users/' + publica + '.user', 'w') as f:
            f.write("")
        return jsonify({'mensagem': 'Conta criada com sucesso', 'endereco': publica, 'chave': privada}), 201

    def nova_transacao(self):
        
        dados = request.get_json()
        if (dados['quantidade'] <= 0):
            return "Valor inválido. Tente valores maiores que 0.", 403
        transacao = Transacao(dados['from'], dados['name'], dados['to'], dados['quantidade'])
        transacao.assinar_transacao(dados['chave'])
        print(transacao.assinatura_remetente)
        result, code = self.blockchain.adicionar_transacao(transacao)
        return jsonify({'mensagem': result}), code

    def sincronizar_cadeia(self):
        return jsonify({'mensagem': 'Sincronização realizada com sucesso'}), 200

    def mostrar_cadeia(self):
        chain = self.blockchain.mostrar()
        return jsonify({'mensagem': chain}), 200
    
    def consultar_saldo(self):
        dados = request.get_json()
        result, code = self.blockchain.calcular_saldo(dados['endereco'])
        return jsonify({'mensagem': result}), code