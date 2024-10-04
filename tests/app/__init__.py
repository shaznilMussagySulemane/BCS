from flask import Flask
from .blockchain import BlockchainPoS

def create_app():
    """Cria e configura a aplicação Flask."""
    app = Flask(__name__)

    # Inicializando a blockchain PoS
    blockchain = BlockchainPoS()

    # Cria uma instância de Node, mas aqui não usa blueprint
    # node = Node(blockchain)  # Caso você queira usar esta abordagem dentro de `run.py`

    return app
